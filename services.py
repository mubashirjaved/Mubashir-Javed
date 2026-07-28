"""
Enterprise ERP Services & Repository Layer
Implements Repository Pattern and Service Layer in alignment with SOLID principles.
"""

import os
import shutil
import datetime
import csv
import io
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy import desc
from models import db, User, Item, Supplier, PurchaseOrder, IssueRecord, InventoryLog, ActivityLog, AuditLog, BackupRecord
from security import hash_password, verify_password, generate_jwt, verify_jwt

# ==========================================
# REPOSITORY PATTERN LAYER
# ==========================================

class UserRepository:
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        return db.session.get(User, user_id)

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_all() -> List[User]:
        return User.query.all()

    @staticmethod
    def add(user: User) -> User:
        user.sign()
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def save(user: User) -> User:
        user.sign()
        db.session.commit()
        return user


class InventoryRepository:
    @staticmethod
    def get_by_id(item_id: int) -> Optional[Item]:
        return db.session.get(Item, item_id)

    @staticmethod
    def get_by_sku(sku: str) -> Optional[Item]:
        return Item.query.filter_by(sku=sku).first()

    @staticmethod
    def get_all() -> List[Item]:
        return Item.query.all()

    @staticmethod
    def get_low_stock() -> List[Item]:
        return Item.query.filter(Item.quantity <= Item.safety_threshold).all()

    @staticmethod
    def add(item: Item) -> Item:
        item.sign()
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def save(item: Item) -> Item:
        item.sign()
        db.session.commit()
        return item


class SupplierRepository:
    @staticmethod
    def get_by_id(supplier_id: int) -> Optional[Supplier]:
        return db.session.get(Supplier, supplier_id)

    @staticmethod
    def get_by_code(code: str) -> Optional[Supplier]:
        return Supplier.query.filter_by(code=code).first()

    @staticmethod
    def get_all() -> List[Supplier]:
        return Supplier.query.all()

    @staticmethod
    def add(supplier: Supplier) -> Supplier:
        supplier.sign()
        db.session.add(supplier)
        db.session.commit()
        return supplier

    @staticmethod
    def save(supplier: Supplier) -> Supplier:
        supplier.sign()
        db.session.commit()
        return supplier


class OrderRepository:
    @staticmethod
    def get_order_by_id(order_id: int) -> Optional[PurchaseOrder]:
        return db.session.get(PurchaseOrder, order_id)

    @staticmethod
    def get_order_by_number(order_number: str) -> Optional[PurchaseOrder]:
        return PurchaseOrder.query.filter_by(order_number=order_number).first()

    @staticmethod
    def get_all_orders() -> List[PurchaseOrder]:
        return PurchaseOrder.query.all()

    @staticmethod
    def add_order(order: PurchaseOrder) -> PurchaseOrder:
        order.sign()
        db.session.add(order)
        db.session.commit()
        return order

    @staticmethod
    def save_order(order: PurchaseOrder) -> PurchaseOrder:
        order.sign()
        db.session.commit()
        return order

    @staticmethod
    def get_issue_by_ticket(ticket: str) -> Optional[IssueRecord]:
        return IssueRecord.query.filter_by(issue_ticket=ticket).first()

    @staticmethod
    def get_all_issues() -> List[IssueRecord]:
        return IssueRecord.query.all()

    @staticmethod
    def add_issue(issue: IssueRecord) -> IssueRecord:
        issue.sign()
        db.session.add(issue)
        db.session.commit()
        return issue


class LogRepository:
    @staticmethod
    def add_inventory_log(log: InventoryLog) -> InventoryLog:
        log.sign()
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def get_inventory_logs() -> List[InventoryLog]:
        return InventoryLog.query.order_by(desc(InventoryLog.timestamp)).all()

    @staticmethod
    def add_activity_log(username: str, action: str, ip_address: str = None) -> ActivityLog:
        log = ActivityLog(username=username, action=action, ip_address=ip_address)
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def get_activity_logs() -> List[ActivityLog]:
        return ActivityLog.query.order_by(desc(ActivityLog.timestamp)).all()

    @staticmethod
    def add_audit_log(admin_user: str, operation: str, details: str) -> AuditLog:
        log = AuditLog(admin_user=admin_user, operation=operation, details=details)
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def get_audit_logs() -> List[AuditLog]:
        return AuditLog.query.order_by(desc(AuditLog.timestamp)).all()


# ==========================================
# SERVICE LAYER
# ==========================================

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.log_repo = LogRepository()

    def register_user(self, username: str, password: str, role: str, full_name: str, contact: str, admin_actor: str = "System") -> Tuple[bool, str]:
        if self.user_repo.get_by_username(username):
            return False, "Username already exists"

        hashed = hash_password(password)
        new_user = User(
            username=username,
            password_hash=hashed,
            role=role,
            full_name=full_name,
            contact_info=contact
        )
        self.user_repo.add(new_user)
        self.log_repo.add_audit_log(admin_actor, "USER_CREATION", f"Created user '{username}' with role '{role}'")
        return True, "User registered successfully"

    def authenticate(self, username: str, password: str, ip_address: str = None) -> Tuple[Optional[User], Optional[str]]:
        """Verify password and return User with JWT token if successful."""
        user = self.user_repo.get_by_username(username)
        if not user:
            self.log_repo.add_activity_log(username or "Unknown", "FAILED_LOGIN_USER_NOT_FOUND", ip_address)
            return None, None

        if verify_password(password, user.password_hash):
            token = generate_jwt(user.id, user.username, user.role)
            self.log_repo.add_activity_log(username, "SUCCESSFUL_LOGIN", ip_address)
            return user, token

        self.log_repo.add_activity_log(username, "FAILED_LOGIN_INVALID_PASSWORD", ip_address)
        return None, None

    def change_user_role(self, username: str, new_role: str, admin_actor: str) -> Tuple[bool, str]:
        user = self.user_repo.get_by_username(username)
        if not user:
            return False, "User not found"
        old_role = user.role
        user.role = new_role
        self.user_repo.save(user)
        self.log_repo.add_audit_log(admin_actor, "USER_ROLE_CHANGE", f"Changed role of '{username}' from '{old_role}' to '{new_role}'")
        return True, f"User role modified to '{new_role}'"


class InventoryService:
    def __init__(self):
        self.inv_repo = InventoryRepository()
        self.log_repo = LogRepository()

    def create_item(self, sku: str, name: str, category: str, location: str, safety_threshold: int, unit_price: float, notes: str, user_id: int, username: str) -> Tuple[bool, str, Optional[Item]]:
        if self.inv_repo.get_by_sku(sku):
            return False, "SKU already exists", None

        new_item = Item(
            sku=sku,
            name=name,
            category=category,
            location=location,
            quantity=0,
            safety_threshold=safety_threshold,
            unit_price=unit_price,
            notes=notes
        )
        self.inv_repo.add(new_item)

        # Log inventory creation
        self.log_repo.add_activity_log(username, f"CREATE_ITEM: SKU={sku}, Name={name}")
        return True, "Item registered successfully", new_item

    def stock_in(self, sku: str, quantity: int, reference_id: str, user_id: int, username: str) -> Tuple[bool, str]:
        if quantity <= 0:
            return False, "Quantity must be greater than zero"

        item = self.inv_repo.get_by_sku(sku)
        if not item:
            return False, "Item not found"

        item.quantity += quantity
        self.inv_repo.save(item)

        # Log stock transaction
        txn_log = InventoryLog(
            item_id=item.id,
            transaction_type="STOCK_IN",
            quantity_changed=quantity,
            balance_after=item.quantity,
            user_id=user_id,
            reference_id=reference_id
        )
        self.log_repo.add_inventory_log(txn_log)
        self.log_repo.add_activity_log(username, f"STOCK_IN: Item={item.name}, SKU={sku}, Qty=+{quantity}")
        return True, f"Stock successfully updated. Current stock: {item.quantity}"

    def stock_out(self, sku: str, quantity: int, issued_to: str, work_order: str, user_id: int, username: str) -> Tuple[bool, str]:
        if quantity <= 0:
            return False, "Quantity must be greater than zero"

        item = self.inv_repo.get_by_sku(sku)
        if not item:
            return False, "Item not found"

        if item.quantity < quantity:
            return False, f"Insufficient stock. Available: {item.quantity}, Requested: {quantity}"

        item.quantity -= quantity
        self.inv_repo.save(item)

        # Create Issue Record
        import uuid
        ticket_num = f"ISS-{int(datetime.datetime.utcnow().timestamp())}-{uuid.uuid4().hex[:6].upper()}"
        issue_record = IssueRecord(
            issue_ticket=ticket_num,
            item_id=item.id,
            quantity=quantity,
            issued_to_employee=issued_to,
            work_order_reference=work_order
        )
        OrderRepository.add_issue(issue_record)

        # Log inventory transaction
        txn_log = InventoryLog(
            item_id=item.id,
            transaction_type="STOCK_OUT",
            quantity_changed=-quantity,
            balance_after=item.quantity,
            user_id=user_id,
            reference_id=ticket_num
        )
        self.log_repo.add_inventory_log(txn_log)
        self.log_repo.add_activity_log(username, f"STOCK_OUT: Item={item.name}, SKU={sku}, Qty=-{quantity}, Ticket={ticket_num}")

        warning_msg = ""
        if item.quantity <= item.safety_threshold:
            warning_msg = f" [ALERT: Stock falls below safety threshold of {item.safety_threshold}!]"

        return True, f"Stock issued successfully. Issue Ticket: {ticket_num}.{warning_msg}"


class SupplierService:
    def __init__(self):
        self.supplier_repo = SupplierRepository()
        self.order_repo = OrderRepository()
        self.log_repo = LogRepository()

    def create_supplier(self, code: str, name: str, contact_person: str, phone: str, email: str, address: str, username: str) -> Tuple[bool, str]:
        if self.supplier_repo.get_by_code(code):
            return False, "Supplier code already exists"

        new_supplier = Supplier(
            code=code,
            name=name,
            contact_person=contact_person,
            phone=phone,
            email=email,
            address=address
        )
        self.supplier_repo.add(new_supplier)
        self.log_repo.add_activity_log(username, f"CREATE_SUPPLIER: Code={code}, Name={name}")
        return True, "Supplier created successfully"

    def create_purchase_order(self, supplier_id: int, item_id: int, quantity: int, unit_cost: float, username: str) -> Tuple[bool, str]:
        if quantity <= 0 or unit_cost <= 0:
            return False, "Quantity and Unit Cost must be positive"

        order_num = f"PO-{int(datetime.datetime.utcnow().timestamp())}"
        new_po = PurchaseOrder(
            order_number=order_num,
            supplier_id=supplier_id,
            item_id=item_id,
            quantity=quantity,
            unit_cost=unit_cost,
            status="Pending"
        )
        self.order_repo.add_order(new_po)
        self.log_repo.add_activity_log(username, f"CREATE_PO: Order={order_num}, Qty={quantity}")
        return True, f"Purchase Order created successfully. Order Number: {order_num}"

    def receive_purchase_order(self, order_id: int, user_id: int, username: str) -> Tuple[bool, str]:
        po = self.order_repo.get_order_by_id(order_id)
        if not po:
            return False, "Purchase order not found"

        if po.status != "Pending":
            return False, f"Cannot receive order with status: {po.status}"

        # Update PO status
        po.status = "Completed"
        self.order_repo.save_order(po)

        # Increase item quantity
        inv_service = InventoryService()
        success, msg = inv_service.stock_in(po.item.sku, po.quantity, po.order_number, user_id, username)
        if not success:
            return False, f"Failed to complete stock-in during order receipt: {msg}"

        self.log_repo.add_activity_log(username, f"RECEIVE_PO: Order={po.order_number}, Status=Completed")
        return True, f"Purchase order successfully received. Stock updated."


class ReportService:
    @staticmethod
    def get_dashboard_summary() -> Dict[str, Any]:
        """Collect real-time dashboard widgets statistics."""
        total_items = Item.query.count()
        low_stock_items = Item.query.filter(Item.quantity <= Item.safety_threshold).count()
        total_suppliers = Supplier.query.count()
        pending_orders = PurchaseOrder.query.filter_by(status="Pending").count()

        # Financial evaluation of currently stored mechanical stock
        total_stock_value = sum(item.quantity * item.unit_price for item in Item.query.all())

        # Compute recent transaction counts (Stock In and Out in last 7 days)
        seven_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        recent_in = InventoryLog.query.filter(InventoryLog.transaction_type == "STOCK_IN", InventoryLog.timestamp >= seven_days_ago).count()
        recent_out = InventoryLog.query.filter(InventoryLog.transaction_type == "STOCK_OUT", InventoryLog.timestamp >= seven_days_ago).count()

        return {
            "total_items": total_items,
            "low_stock_items": low_stock_items,
            "total_suppliers": total_suppliers,
            "pending_orders": pending_orders,
            "total_stock_value": round(total_stock_value, 2),
            "recent_stock_in": recent_in,
            "recent_stock_out": recent_out
        }

    @staticmethod
    def export_inventory_csv() -> str:
        """Export full inventory table to CSV format in-memory."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["SKU", "Item Name", "Category", "Location", "Quantity", "Safety Threshold", "Unit Price", "Total Cost", "Notes"])

        for item in Item.query.all():
            writer.writerow([
                item.sku,
                item.name,
                item.category,
                item.location,
                item.quantity,
                item.safety_threshold,
                item.unit_price,
                round(item.quantity * item.unit_price, 2),
                item.notes
            ])
        return output.getvalue()


class BackupService:
    @staticmethod
    def trigger_backup(backup_dir: str, db_file_path: str, created_by: str) -> Tuple[bool, str]:
        """Perform safe offline backup of SQLite database, keeping metadata log."""
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        if not os.path.exists(db_file_path):
            return False, f"Source DB file not found: {db_file_path}"

        timestamp_str = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"erp_backup_{timestamp_str}.sqlite"
        dest_path = os.path.join(backup_dir, backup_filename)

        try:
            shutil.copy2(db_file_path, dest_path)
            file_size_kb = round(os.path.getsize(dest_path) / 1024, 2)

            # Log backup event in model
            backup_rec = BackupRecord(
                backup_filename=backup_filename,
                file_path=dest_path,
                file_size_kb=file_size_kb,
                created_by=created_by,
                status="Successful"
            )
            db.session.add(backup_rec)
            db.session.commit()

            # Log into audit logs
            log_repo = LogRepository()
            log_repo.add_audit_log(created_by, "DATABASE_BACKUP", f"Database successfully backed up to {backup_filename}")
            return True, f"Backup successful: {backup_filename}"
        except Exception as e:
            return False, f"Backup error occurred: {str(e)}"

    @staticmethod
    def verify_db_tamper_state() -> List[Dict[str, Any]]:
        """
        Verify every single item, supplier, issue, and PO record's
        tamper detection signature against current state.
        Returns a list of detected integrity failures if any.
        """
        failures = []

        # Check Items
        for item in Item.query.all():
            if not item.check_integrity():
                failures.append({"table": "items", "id": item.id, "identifier": item.sku, "error": "Signature Mismatch"})

        # Check Users
        for user in User.query.all():
            if not user.check_integrity():
                failures.append({"table": "users", "id": user.id, "identifier": user.username, "error": "Signature Mismatch"})

        # Check Suppliers
        for supplier in Supplier.query.all():
            if not supplier.check_integrity():
                failures.append({"table": "suppliers", "id": supplier.id, "identifier": supplier.code, "error": "Signature Mismatch"})

        # Check PurchaseOrders
        for po in PurchaseOrder.query.all():
            if not po.check_integrity():
                failures.append({"table": "purchase_orders", "id": po.id, "identifier": po.order_number, "error": "Signature Mismatch"})

        # Check IssueRecords
        for issue in IssueRecord.query.all():
            if not issue.check_integrity():
                failures.append({"table": "issue_records", "id": issue.id, "identifier": issue.issue_ticket, "error": "Signature Mismatch"})

        return failures
