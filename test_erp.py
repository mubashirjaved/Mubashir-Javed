"""
Enterprise Integration & Unit Test Suite
Covers security modules, encryption correctness, database signature-based tamper detection,
and transactional service layer inventory stock rules.
"""

import os
import pytest
from app import app, db
from models import User, Item, Supplier, PurchaseOrder, IssueRecord, InventoryLog
from security import encrypt_field, decrypt_field, hash_password, verify_password, generate_jwt, verify_jwt
from services import AuthService, InventoryService, SupplierService, BackupService, ReportService

@pytest.fixture(name="test_client")
def fixture_test_client():
    """Sets up a secure, clean database for testing in-memory."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_field_level_encryption(test_client):
    """Verify field AES-256 encryption and decryption are completely functional."""
    plain_text = "Highly Classified Technical Formula Specs"
    encrypted = encrypt_field(plain_text)

    assert encrypted != plain_text
    assert len(encrypted) > 10

    decrypted = decrypt_field(encrypted)
    assert decrypted == plain_text


def test_password_hashing(test_client):
    """Verify password secure hashing via bcrypt and integrity validations."""
    pword = "SuperSecurePassword123!"
    hashed = hash_password(pword)

    assert hashed != pword
    assert verify_password(pword, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_jwt_generation_and_validation(test_client):
    """Verify enterprise JWT token generation, sign claims and authentication decay."""
    token = generate_jwt(user_id=99, username="operator_tech", role="InventoryManager")
    assert token is not None

    claims = verify_jwt(token)
    assert claims is not None
    assert claims["sub"] == "99"
    assert claims["username"] == "operator_tech"
    assert claims["role"] == "InventoryManager"


def test_database_record_tamper_detection(test_client):
    """Verify dynamic record validation signatures detect unauthorized modifications."""
    with app.app_context():
        # Create user and sign
        auth = AuthService()
        auth.register_user("tech_user", "SecPassword!", "Viewer", "Tech User One", "tech@ent.com")

        # Verify initial integrity checks pass
        failures = BackupService.verify_db_tamper_state()
        assert len(failures) == 0

        # Manually alter user fields directly on DB level (bypass model properties and signing mechanism)
        db_user = User.query.filter_by(username="tech_user").first()
        db_user.role = "Admin"  # Unauthorized elevation
        db.session.commit()

        # Verify structural tamper integrity detector catches this elevation
        failures = BackupService.verify_db_tamper_state()
        assert len(failures) > 0
        assert failures[0]["table"] == "users"
        assert failures[0]["identifier"] == "tech_user"


def test_inventory_service_transactions(test_client):
    """Verify stock-in, stock-out business logic, and safety threshold alerts."""
    with app.app_context():
        # Setup testing roles
        auth = AuthService()
        auth.register_user("admin_test", "P@ss123!", "Admin", "Admin Test", "admin@ent.com")
        admin = User.query.filter_by(username="admin_test").first()

        # Register new mechanical item
        inv = InventoryService()
        success, msg, item = inv.create_item(
            sku="TEST-SKU-100",
            name="Testing Heavy Shaft",
            category="Shafts",
            location="Rack-X1",
            safety_threshold=10,
            unit_price=150.00,
            notes="Standard lab test notes",
            user_id=admin.id,
            username=admin.username
        )
        assert success is True
        assert item.quantity == 0

        # Perform Stock-In
        success, msg = inv.stock_in("TEST-SKU-100", 50, "REF-STK-01", admin.id, admin.username)
        assert success is True
        assert "50" in msg

        # Check current balance
        assert item.quantity == 50

        # Perform Stock-Out within limits
        success, msg = inv.stock_out("TEST-SKU-100", 20, "John Employee", "WO-01", admin.id, admin.username)
        assert success is True
        assert item.quantity == 30

        # Perform Stock-Out that triggers safety threshold alert
        success, msg = inv.stock_out("TEST-SKU-100", 25, "John Employee", "WO-02", admin.id, admin.username)
        assert success is True
        assert "falls below safety threshold" in msg
        assert item.quantity == 5

        # Perform Stock-Out beyond current quantity limits (must fail gracefully)
        success, msg = inv.stock_out("TEST-SKU-100", 10, "John Employee", "WO-03", admin.id, admin.username)
        assert success is False
        assert "Insufficient stock" in msg
        assert item.quantity == 5
