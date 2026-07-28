"""
Enterprise ERP Database Models with Field-Level Encryption and Tamper Protection
"""

import datetime
from flask_sqlalchemy import SQLAlchemy
from security import encrypt_field, decrypt_field, compute_record_signature

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="Viewer") # Admin, InventoryManager, ProcurementManager, Viewer
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Encrypted fields
    _full_name = db.Column(db.String(512), nullable=True) # Encrypted
    _contact_info = db.Column(db.String(512), nullable=True) # Encrypted

    # Tamper detection signature
    signature = db.Column(db.String(256), nullable=True)

    @property
    def full_name(self) -> str:
        return decrypt_field(self._full_name) if self._full_name else ""

    @full_name.setter
    def full_name(self, val: str):
        self._full_name = encrypt_field(val)

    @property
    def contact_info(self) -> str:
        return decrypt_field(self._contact_info) if self._contact_info else ""

    @contact_info.setter
    def contact_info(self, val: str):
        self._contact_info = encrypt_field(val)

    def sign(self):
        data = {
            "username": self.username,
            "role": self.role,
            "_full_name": self._full_name or "",
            "_contact_info": self._contact_info or ""
        }
        self.signature = compute_record_signature(data)

    def check_integrity(self) -> bool:
        if not self.signature:
            return True # Or False depending on policy; we return True for default system setup
        data = {
            "username": self.username,
            "role": self.role,
            "_full_name": self._full_name or "",
            "_contact_info": self._contact_info or ""
        }
        return compute_record_signature(data) == self.signature


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False) # Warehouse rack info
    quantity = db.Column(db.Integer, nullable=False, default=0)
    safety_threshold = db.Column(db.Integer, nullable=False, default=5)
    unit_price = db.Column(db.Float, nullable=False, default=0.0)

    _notes = db.Column(db.String(512), nullable=True) # Encrypted specifications/notes
    signature = db.Column(db.String(256), nullable=True)

    @property
    def notes(self) -> str:
        return decrypt_field(self._notes) if self._notes else ""

    @notes.setter
    def notes(self, val: str):
        self._notes = encrypt_field(val)

    def sign(self):
        data = {
            "sku": self.sku,
            "name": self.name,
            "category": self.category,
            "location": self.location,
            "quantity": self.quantity,
            "safety_threshold": self.safety_threshold,
            "unit_price": self.unit_price,
            "_notes": self._notes or ""
        }
        self.signature = compute_record_signature(data)

    def check_integrity(self) -> bool:
        if not self.signature:
            return True
        data = {
            "sku": self.sku,
            "name": self.name,
            "category": self.category,
            "location": self.location,
            "quantity": self.quantity,
            "safety_threshold": self.safety_threshold,
            "unit_price": self.unit_price,
            "_notes": self._notes or ""
        }
        return compute_record_signature(data) == self.signature


class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)

    _contact_person = db.Column(db.String(512), nullable=True) # Encrypted
    _phone = db.Column(db.String(512), nullable=True)          # Encrypted
    _email = db.Column(db.String(512), nullable=True)          # Encrypted
    _address = db.Column(db.String(512), nullable=True)        # Encrypted

    signature = db.Column(db.String(256), nullable=True)

    @property
    def contact_person(self) -> str:
        return decrypt_field(self._contact_person) if self._contact_person else ""

    @contact_person.setter
    def contact_person(self, val: str):
        self._contact_person = encrypt_field(val)

    @property
    def phone(self) -> str:
        return decrypt_field(self._phone) if self._phone else ""

    @phone.setter
    def phone(self, val: str):
        self._phone = encrypt_field(val)

    @property
    def email(self) -> str:
        return decrypt_field(self._email) if self._email else ""

    @email.setter
    def email(self, val: str):
        self._email = encrypt_field(val)

    @property
    def address(self) -> str:
        return decrypt_field(self._address) if self._address else ""

    @address.setter
    def address(self, val: str):
        self._address = encrypt_field(val)

    def sign(self):
        data = {
            "code": self.code,
            "name": self.name,
            "_contact_person": self._contact_person or "",
            "_phone": self._phone or "",
            "_email": self._email or "",
            "_address": self._address or ""
        }
        self.signature = compute_record_signature(data)

    def check_integrity(self) -> bool:
        if not self.signature:
            return True
        data = {
            "code": self.code,
            "name": self.name,
            "_contact_person": self._contact_person or "",
            "_phone": self._phone or "",
            "_email": self._email or "",
            "_address": self._address or ""
        }
        return compute_record_signature(data) == self.signature


class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(100), unique=True, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending") # Pending, Completed, Cancelled
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    supplier = db.relationship('Supplier', backref='orders')
    item = db.relationship('Item', backref='orders')

    signature = db.Column(db.String(256), nullable=True)

    def sign(self):
        data = {
            "order_number": self.order_number,
            "supplier_id": self.supplier_id,
            "item_id": self.item_id,
            "quantity": self.quantity,
            "unit_cost": self.unit_cost,
            "status": self.status
        }
        self.signature = compute_record_signature(data)

    def check_integrity(self) -> bool:
        if not self.signature:
            return True
        data = {
            "order_number": self.order_number,
            "supplier_id": self.supplier_id,
            "item_id": self.item_id,
            "quantity": self.quantity,
            "unit_cost": self.unit_cost,
            "status": self.status
        }
        return compute_record_signature(data) == self.signature


class IssueRecord(db.Model):
    """Stores items issued to employees/work orders."""
    __tablename__ = 'issue_records'
    id = db.Column(db.Integer, primary_key=True)
    issue_ticket = db.Column(db.String(100), unique=True, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    issued_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Encrypted employee identity information to safeguard GDPR / HR data
    _issued_to_employee = db.Column(db.String(512), nullable=False) # Encrypted
    _work_order_reference = db.Column(db.String(512), nullable=False) # Encrypted

    item = db.relationship('Item', backref='issues')
    signature = db.Column(db.String(256), nullable=True)

    @property
    def issued_to_employee(self) -> str:
        return decrypt_field(self._issued_to_employee) if self._issued_to_employee else ""

    @issued_to_employee.setter
    def issued_to_employee(self, val: str):
        self._issued_to_employee = encrypt_field(val)

    @property
    def work_order_reference(self) -> str:
        return decrypt_field(self._work_order_reference) if self._work_order_reference else ""

    @work_order_reference.setter
    def work_order_reference(self, val: str):
        self._work_order_reference = encrypt_field(val)

    def sign(self):
        data = {
            "issue_ticket": self.issue_ticket,
            "item_id": self.item_id,
            "quantity": self.quantity,
            "_issued_to_employee": self._issued_to_employee or "",
            "_work_order_reference": self._work_order_reference or ""
        }
        self.signature = compute_record_signature(data)

    def check_integrity(self) -> bool:
        if not self.signature:
            return True
        data = {
            "issue_ticket": self.issue_ticket,
            "item_id": self.item_id,
            "quantity": self.quantity,
            "_issued_to_employee": self._issued_to_employee or "",
            "_work_order_reference": self._work_order_reference or ""
        }
        return compute_record_signature(data) == self.signature


class InventoryLog(db.Model):
    """Logs stock changes (Stock In, Stock Out, Adjustments)."""
    __tablename__ = 'inventory_logs'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False) # "STOCK_IN", "STOCK_OUT", "ADJUSTMENT"
    quantity_changed = db.Column(db.Integer, nullable=False)
    balance_after = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reference_id = db.Column(db.String(100), nullable=True) # e.g., Purchase Order number or Issue Ticket
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    item = db.relationship('Item', backref='inventory_logs')
    user = db.relationship('User', backref='inventory_logs')
    signature = db.Column(db.String(256), nullable=True)

    def sign(self):
        data = {
            "item_id": self.item_id,
            "transaction_type": self.transaction_type,
            "quantity_changed": self.quantity_changed,
            "balance_after": self.balance_after,
            "user_id": self.user_id,
            "reference_id": self.reference_id or ""
        }
        self.signature = compute_record_signature(data)

    def check_integrity(self) -> bool:
        if not self.signature:
            return True
        data = {
            "item_id": self.item_id,
            "transaction_type": self.transaction_type,
            "quantity_changed": self.quantity_changed,
            "balance_after": self.balance_after,
            "user_id": self.user_id,
            "reference_id": self.reference_id or ""
        }
        return compute_record_signature(data) == self.signature


class ActivityLog(db.Model):
    """Tracks general application actions (Logins, Failed logins, Module actions)."""
    __tablename__ = 'activity_logs'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(200), nullable=False)
    ip_address = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class AuditLog(db.Model):
    """Deep structural and administrative action changes."""
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    admin_user = db.Column(db.String(100), nullable=False)
    operation = db.Column(db.String(200), nullable=False) # e.g., "INTEGRITY_VERIFICATION", "USER_ROLE_CHANGE", "BACKUP_RESTORE"
    details = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class BackupRecord(db.Model):
    """Tracks database backup history."""
    __tablename__ = 'backup_records'
    id = db.Column(db.Integer, primary_key=True)
    backup_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    file_size_kb = db.Column(db.Float, nullable=False)
    created_by = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="Successful")
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
