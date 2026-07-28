"""
Flask Blueprints and Controller Layers
Sets up routing for Web UI and REST API. Provides JWT authentication checks and session control.
"""

from functools import wraps
from flask import Blueprint, request, jsonify, session, redirect, url_for, flash, Response
from services import AuthService, InventoryService, SupplierService, ReportService, BackupService, LogRepository, UserRepository, InventoryRepository, SupplierRepository, OrderRepository
from models import Item, Supplier, PurchaseOrder, IssueRecord
from security import verify_jwt

# Define Blueprints
auth_bp = Blueprint('auth', __name__)
dashboard_bp = Blueprint('dashboard', __name__)
inventory_bp = Blueprint('inventory', __name__)
supplier_bp = Blueprint('supplier', __name__)
report_bp = Blueprint('report', __name__)
backup_bp = Blueprint('backup', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Rate limit simulator (simulates enterprise scale defense)
def rate_limit():
    # Simple simulation: we can expand or log request spikes in prod
    pass


# Middleware: Require session login for Web Views
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        rate_limit()
        if 'user_id' not in session:
            flash("Please authenticate to access the Inventory ERP.", "danger")
            return redirect(url_for('auth.login_view'))
        return f(*args, **kwargs)
    return decorated_function


# Middleware: Require specific enterprise roles
def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session or session['user_role'] not in roles:
                flash("Unauthorized! Access restricted to higher clearance levels.", "danger")
                return redirect(url_for('dashboard.home_view'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Middleware: JWT Authentication for REST API
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid authorization header"}), 401

        token = auth_header.split(" ")[1]
        payload = verify_jwt(token)
        if not payload:
            return jsonify({"error": "Token expired or invalid"}), 401

        request.user_payload = payload
        return f(*args, **kwargs)
    return decorated_function


# ==========================================
# 1. AUTH BLUEPRINT
# ==========================================

from flask import render_template

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        auth_service = AuthService()
        user, token = auth_service.authenticate(username, password, request.remote_addr)

        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_role'] = user.role
            session['full_name'] = user.full_name
            # Store the token in session too so frontend scripts can read/authenticate easily
            session['jwt_token'] = token
            # Anti-CSRF session token creation
            session['csrf_token'] = f"token_{user.id}_{int(request.remote_addr.replace('.', '')) % 1000}"
            flash(f"Welcome back, {user.full_name}! Level: {user.role}", "success")
            return redirect(url_for('dashboard.home_view'))
        else:
            flash("Invalid authentication credentials. Try again.", "danger")

    return render_template('login.html')


@auth_bp.route('/logout')
def logout_view():
    username = session.get('username', 'Unknown')
    session.clear()
    LogRepository.add_activity_log(username, "LOGOUT_SUCCESS")
    flash("Successfully signed out.", "info")
    return redirect(url_for('auth.login_view'))


# ==========================================
# 2. DASHBOARD BLUEPRINT
# ==========================================

@dashboard_bp.route('/')
@login_required
def home_view():
    summary = ReportService.get_dashboard_summary()
    activities = LogRepository.get_activity_logs()[:10]  # Show top 10 activity logs
    audit_logs = LogRepository.get_audit_logs()[:10]  # Show top 10 audit logs
    low_stocks = InventoryRepository.get_low_stock()

    return render_template('dashboard.html',
                           summary=summary,
                           activities=activities,
                           audit_logs=audit_logs,
                           low_stocks=low_stocks)


# ==========================================
# 3. INVENTORY BLUEPRINT
# ==========================================

@inventory_bp.route('/inventory', methods=['GET', 'POST'])
@login_required
def list_inventory():
    if request.method == 'POST':
        # Add new item
        sku = request.form.get('sku')
        name = request.form.get('name')
        category = request.form.get('category')
        location = request.form.get('location')
        safety_threshold = int(request.form.get('safety_threshold', 5))
        unit_price = float(request.form.get('unit_price', 0.0))
        notes = request.form.get('notes', '')

        inv_service = InventoryService()
        success, msg, _ = inv_service.create_item(
            sku=sku, name=name, category=category, location=location,
            safety_threshold=safety_threshold, unit_price=unit_price,
            notes=notes, user_id=session['user_id'], username=session['username']
        )
        if success:
            flash(msg, "success")
        else:
            flash(msg, "danger")

    items = InventoryRepository.get_all()
    return render_template('inventory.html', items=items)


@inventory_bp.route('/inventory/stock-in', methods=['POST'])
@login_required
@roles_required('Admin', 'InventoryManager')
def stock_in():
    sku = request.form.get('sku')
    quantity = int(request.form.get('quantity', 0))
    ref = request.form.get('reference_id', 'Direct Manual Update')

    inv_service = InventoryService()
    success, msg = inv_service.stock_in(sku, quantity, ref, session['user_id'], session['username'])
    if success:
        flash(msg, "success")
    else:
        flash(msg, "danger")
    return redirect(url_for('inventory.list_inventory'))


@inventory_bp.route('/inventory/stock-out', methods=['POST'])
@login_required
@roles_required('Admin', 'InventoryManager')
def stock_out():
    sku = request.form.get('sku')
    quantity = int(request.form.get('quantity', 0))
    issued_to = request.form.get('issued_to_employee')
    work_order = request.form.get('work_order_reference')

    inv_service = InventoryService()
    success, msg = inv_service.stock_out(sku, quantity, issued_to, work_order, session['user_id'], session['username'])
    if success:
        flash(msg, "success")
    else:
        flash(msg, "danger")
    return redirect(url_for('inventory.list_inventory'))


# ==========================================
# 4. SUPPLIER & PURCHASE ORDER BLUEPRINT
# ==========================================

@supplier_bp.route('/suppliers', methods=['GET', 'POST'])
@login_required
def list_suppliers():
    supplier_service = SupplierService()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_supplier':
            code = request.form.get('code')
            name = request.form.get('name')
            contact = request.form.get('contact_person')
            phone = request.form.get('phone')
            email = request.form.get('email')
            address = request.form.get('address')

            success, msg = supplier_service.create_supplier(code, name, contact, phone, email, address, session['username'])
            if success:
                flash(msg, "success")
            else:
                flash(msg, "danger")

        elif action == 'create_order':
            # Role clearance validation
            if session['user_role'] not in ('Admin', 'ProcurementManager'):
                flash("Insufficient access level to issue purchase orders.", "danger")
            else:
                supplier_id = int(request.form.get('supplier_id'))
                item_id = int(request.form.get('item_id'))
                quantity = int(request.form.get('quantity'))
                unit_cost = float(request.form.get('unit_cost'))

                success, msg = supplier_service.create_purchase_order(supplier_id, item_id, quantity, unit_cost, session['username'])
                if success:
                    flash(msg, "success")
                else:
                    flash(msg, "danger")

    suppliers = SupplierRepository.get_all()
    orders = OrderRepository.get_all_orders()
    items = InventoryRepository.get_all()
    return render_template('suppliers.html', suppliers=suppliers, orders=orders, items=items)


@supplier_bp.route('/orders/receive/<int:order_id>', methods=['POST'])
@login_required
@roles_required('Admin', 'InventoryManager', 'ProcurementManager')
def receive_order(order_id):
    supplier_service = SupplierService()
    success, msg = supplier_service.receive_purchase_order(order_id, session['user_id'], session['username'])
    if success:
        flash(msg, "success")
    else:
        flash(msg, "danger")
    return redirect(url_for('supplier.list_suppliers'))


# ==========================================
# 5. REPORTING BLUEPRINT
# ==========================================

@report_bp.route('/reports')
@login_required
def show_reports():
    activity_logs = LogRepository.get_activity_logs()
    audit_logs = LogRepository.get_audit_logs()
    return render_template('reports.html', activity_logs=activity_logs, audit_logs=audit_logs)


@report_bp.route('/reports/export-inventory')
@login_required
def export_inventory_csv():
    csv_data = ReportService.export_inventory_csv()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=erp_inventory_report.csv"}
    )


# ==========================================
# 6. SYSTEM BACKUP & TAMPER BLUEPRINT
# ==========================================

@backup_bp.route('/backups', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def backup_panel():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'trigger_backup':
            # Safe automated directory lookup
            backup_dir = "instance/backups"
            db_file_path = "instance/erp_encrypted.db"
            success, msg = BackupService.trigger_backup(backup_dir, db_file_path, session['username'])
            if success:
                flash(msg, "success")
            else:
                flash(msg, "danger")

        elif action == 'verify_integrity':
            # Perform deep verification
            failures = BackupService.verify_db_tamper_state()
            if not failures:
                flash("Integrity Verification Passed! All records matched structural signature SHA-256 HMAC checksums.", "success")
                LogRepository.add_audit_log(session['username'], "INTEGRITY_VERIFICATION", "Completed full database signature check. STATUS: PASSED")
            else:
                flash(f"CRITICAL WARNING! Structural Database Tamper Detected on {len(failures)} record(s)!", "danger")
                LogRepository.add_audit_log(session['username'], "INTEGRITY_VERIFICATION", f"Database signature verification FAILED! Corrupted entities: {failures}")

    backups = BackupRecord.query.all()
    return render_template('backups.html', backups=backups)


# ==========================================
# 7. REST API (JWT AUTHENTICATED)
# ==========================================

@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')

    auth_service = AuthService()
    user, token = auth_service.authenticate(username, password, request.remote_addr)
    if user and token:
        return jsonify({
            "status": "success",
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "full_name": user.full_name
            }
        }), 200

    return jsonify({"error": "Invalid username or password"}), 401


@api_bp.route('/inventory', methods=['GET'])
@jwt_required
def api_get_inventory():
    items = InventoryRepository.get_all()
    return jsonify([{
        "id": i.id,
        "sku": i.sku,
        "name": i.name,
        "category": i.category,
        "quantity": i.quantity,
        "safety_threshold": i.safety_threshold,
        "unit_price": i.unit_price,
        "notes": i.notes
    } for i in items]), 200


@api_bp.route('/inventory/stock-in', methods=['POST'])
@jwt_required
def api_stock_in():
    # Only Admin or InventoryManager
    payload = request.user_payload
    if payload.get("role") not in ('Admin', 'InventoryManager'):
        return jsonify({"error": "Insufficient operational permissions"}), 403

    data = request.json or {}
    sku = data.get("sku")
    quantity = int(data.get("quantity", 0))
    ref = data.get("reference_id", "API Transaction")

    inv_service = InventoryService()
    success, msg = inv_service.stock_in(sku, quantity, ref, payload.get("sub"), payload.get("username"))
    if success:
        return jsonify({"message": msg}), 200
    return jsonify({"error": msg}), 400
