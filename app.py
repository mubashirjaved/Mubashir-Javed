"""
Main Flask Entrypoint
Registers blueprints, configures SQLite database with automatic instantiation,
creates default enterprise roles/users, and implements auto-launch desktop capability.
"""

import os
import sys
import threading
import time
import webbrowser
from flask import Flask, redirect, url_for, render_template, session
from models import db
from controllers import auth_bp, dashboard_bp, inventory_bp, supplier_bp, report_bp, backup_bp, api_bp
from services import AuthService, UserRepository, InventoryRepository, SupplierRepository, OrderRepository, LogRepository

app = Flask(__name__)

# Configure core Flask security and database pathways
app.config['SECRET_KEY'] = os.getenv("ERP_FLASK_SECRET", "enterprise_erp_flask_secret_session_key_119283")
# Place database in instance folder
os.makedirs("instance", exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///erp_encrypted.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Register system blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(supplier_bp)
app.register_blueprint(report_bp)
app.register_blueprint(backup_bp)
app.register_blueprint(api_bp)

# Basic base root route for smooth navigation flow
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard.home_view'))
    return redirect(url_for('auth.login_view'))


# Custom template helper filter for rendering values safely
@app.context_processor
def inject_now():
    return {'now': time.strftime("%Y-%m-%d %H:%M:%S")}


def initialize_database():
    """Initializes tables, seeds enterprise administration roles, and sample data."""
    db.create_all()

    # Check if we already have users configured
    user_repo = UserRepository()
    if not user_repo.get_by_username("admin"):
        auth_service = AuthService()
        # Seed core Admin
        auth_service.register_user(
            username="admin",
            password="AdminPassword321!",
            role="Admin",
            full_name="John Doe (Senior Architect)",
            contact="admin@enterprise-mechanical.com"
        )

        # Seed Inventory Manager
        auth_service.register_user(
            username="inventory_mgr",
            password="ManagerPassword!",
            role="InventoryManager",
            full_name="Alice Smith (Inventory Head)",
            contact="alice@enterprise-mechanical.com"
        )

        # Seed Procurement Manager
        auth_service.register_user(
            username="procurement_mgr",
            password="BuyerPassword!",
            role="ProcurementManager",
            full_name="Bob Johnson (Procurement Lead)",
            contact="bob@enterprise-mechanical.com"
        )

        # Seed Viewer
        auth_service.register_user(
            username="viewer",
            password="ViewerPassword!",
            role="Viewer",
            full_name="Charlie Brown (Floor Technician)",
            contact="charlie@enterprise-mechanical.com"
        )

        # Seed some initial high-quality mechanical stock items
        inv_repo = InventoryRepository()
        if not inv_repo.get_by_sku("MS-BALL-001"):
            from models import Item
            # Create premium bearing item
            bearing = Item(
                sku="MS-BALL-001",
                name="Heavy Duty Ball Bearing 50mm",
                category="Bearings",
                location="Rack-A1-Level2",
                quantity=100,
                safety_threshold=15,
                unit_price=45.50
            )
            bearing.notes = "Chrome steel deep groove bearings for industrial shafts."
            inv_repo.add(bearing)

            # Create gasket item
            gasket = Item(
                sku="MS-GASK-002",
                name="High-Temperature Silicone Gasket",
                category="Seals & Gaskets",
                location="Rack-C3-Level1",
                quantity=8,  # Under safety threshold intentionally
                safety_threshold=10,
                unit_price=12.25
            )
            gasket.notes = "Max temp 300C. Resists oils and hydraulic fluids."
            inv_repo.add(gasket)

            # Create valve item
            valve = Item(
                sku="MS-VALV-003",
                name="Stainless Steel 2-Way Ball Valve 1/2in",
                category="Valves",
                location="Rack-B2-Level4",
                quantity=25,
                safety_threshold=5,
                unit_price=89.00
            )
            valve.notes = "316 Stainless steel, threaded connection, rated for 1000 PSI."
            inv_repo.add(valve)

            # Seed a default supplier
            supp_repo = SupplierRepository()
            if not supp_repo.get_by_code("SUP-IND-001"):
                from models import Supplier
                supp = Supplier(
                    code="SUP-IND-001",
                    name="Apex Mechanical & Industrial Supplies Ltd."
                )
                supp.contact_person = "Richard Hendrix"
                supp.phone = "+1-555-0199"
                supp.email = "orders@apex-industrial.com"
                supp.address = "100 Industrial Pkwy, Sector 4, Engineering Zone"
                supp_repo.add(supp)

                # Seed a demo Purchase Order
                from models import PurchaseOrder
                po = PurchaseOrder(
                    order_number="PO-INITIAL-001",
                    supplier_id=supp.id,
                    item_id=bearing.id,
                    quantity=50,
                    unit_cost=38.00,
                    status="Pending"
                )
                po.sign()
                db.session.add(po)
                db.session.commit()

            print("Database successfully seeded with enterprise roles and mechanical stock inventory items.")


def auto_launch_browser(url: str, delay: float = 1.5):
    """Wait for Flask server to launch and spawn default system browser."""
    time.sleep(delay)
    webbrowser.open(url)


# Tie database session with Flask App context
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        initialize_database()

    # Standard server launch info
    host = "127.0.0.1"
    port = 5000
    launch_url = f"http://{host}:{port}/"

    # Start thread to automatically launch default browser
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true": # Prevent auto-launch running twice with reloader
        print(f"Enterprise Inventory & ERP running. Launching default browser at {launch_url}...")
        threading.Thread(target=auto_launch_browser, args=(launch_url,), daemon=True).start()

    app.run(host=host, port=port, debug=False)
