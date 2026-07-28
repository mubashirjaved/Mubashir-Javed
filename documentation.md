# Enterprise-Grade Mechanical Inventory & ERP System Documentation

Welcome to the comprehensive technical and operational manuals for the premium **M-Store ERP System**.

---

## 1. DATABASE SCHEMA DOCUMENTATION

The system uses an **encrypted SQLite storage** structure configured with dynamic column validation, AES-256 field-level symmetric key protection, and dynamic integrity record hashing.

### Tables Overview

1. **`users`**
   - `id` (Integer, Primary Key)
   - `username` (String, Unique, Nullable=False)
   - `password_hash` (String, Hashed using Bcrypt)
   - `role` (String, Clearance options: `Admin`, `InventoryManager`, `ProcurementManager`, `Viewer`)
   - `created_at` (DateTime)
   - `_full_name` (Encrypted text block)
   - `_contact_info` (Encrypted text block)
   - `signature` (SHA-256 HMAC of row contents)

2. **`items` (Mechanical parts)**
   - `id` (Integer, Primary Key)
   - `sku` (String, Unique, Nullable=False)
   - `name` (String, Nullable=False)
   - `category` (String, Nullable=False)
   - `location` (String, Rack details)
   - `quantity` (Integer, default=0)
   - `safety_threshold` (Integer, default=5)
   - `unit_price` (Float, default=0.0)
   - `_notes` (Encrypted specifications)
   - `signature` (SHA-256 HMAC of row contents)

3. **`suppliers`**
   - `id` (Integer, Primary Key)
   - `code` (String, Unique, Nullable=False)
   - `name` (String, Nullable=False)
   - `_contact_person` (Encrypted)
   - `_phone` (Encrypted)
   - `_email` (Encrypted)
   - `_address` (Encrypted)
   - `signature` (SHA-256 HMAC of row contents)

4. **`purchase_orders`**
   - `id` (Integer, Primary Key)
   - `order_number` (String, Unique)
   - `supplier_id` (ForeignKey to `suppliers`)
   - `item_id` (ForeignKey to `items`)
   - `quantity` (Integer)
   - `unit_cost` (Float)
   - `status` (String: `Pending`, `Completed`, `Cancelled`)
   - `order_date` (DateTime)
   - `signature` (SHA-256 HMAC)

5. **`issue_records`**
   - `id` (Integer, Primary Key)
   - `issue_ticket` (String, Unique)
   - `item_id` (ForeignKey to `items`)
   - `quantity` (Integer)
   - `issued_date` (DateTime)
   - `_issued_to_employee` (Encrypted)
   - `_work_order_reference` (Encrypted)
   - `signature` (SHA-256 HMAC)

6. **`inventory_logs`**
   - `id` (Integer, Primary Key)
   - `item_id` (ForeignKey to `items`)
   - `transaction_type` (String: `STOCK_IN`, `STOCK_OUT`, `ADJUSTMENT`)
   - `quantity_changed` (Integer)
   - `balance_after` (Integer)
   - `user_id` (ForeignKey to `users`)
   - `reference_id` (String)
   - `timestamp` (DateTime)
   - `signature` (SHA-256 HMAC)

7. **`activity_logs`**
   - `id` (Integer, Primary Key)
   - `username` (String)
   - `action` (String)
   - `ip_address` (String)
   - `timestamp` (DateTime)

8. **`audit_logs`**
   - `id` (Integer, Primary Key)
   - `admin_user` (String)
   - `operation` (String)
   - `details` (Text)
   - `timestamp` (DateTime)

9. **`backup_records`**
   - `id` (Integer, Primary Key)
   - `backup_filename` (String)
   - `file_path` (String)
   - `file_size_kb` (Float)
   - `created_by` (String)
   - `status` (String)
   - `timestamp` (DateTime)

---

## 2. REST API DOCUMENTATION (V1)

All system endpoints are secure, requiring Bearer JWT tokens in the `Authorization` header.

### Authenticate Session
- **Endpoint:** `POST /api/v1/auth/login`
- **Request Body:**
  ```json
  {
    "username": "admin",
    "password": "AdminPassword321!"
  }
  ```
- **Response:**
  ```json
  {
    "status": "success",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "role": "Admin",
      "full_name": "John Doe"
    }
  }
  ```

### Get Inventory List
- **Endpoint:** `GET /api/v1/inventory`
- **Header:** `Authorization: Bearer <JWT_TOKEN>`
- **Response:**
  ```json
  [
    {
      "id": 1,
      "sku": "MS-BALL-001",
      "name": "Heavy Duty Ball Bearing 50mm",
      "category": "Bearings",
      "quantity": 100,
      "safety_threshold": 15,
      "unit_price": 45.50,
      "notes": "Chrome steel deep groove bearings."
    }
  ]
  ```

### Receive Stock In
- **Endpoint:** `POST /api/v1/inventory/stock-in`
- **Header:** `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  {
    "sku": "MS-BALL-001",
    "quantity": 20,
    "reference_id": "PO-991823"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Stock successfully updated. Current stock: 120"
  }
  ```

---

## 3. USER & ADMINISTRATOR MANUAL

### Operational Workflow

1. **Session Inactivity Protection:** The application checks user activity. If idle for more than 15 minutes, it invalidates cookies and logs the user out.
2. **Stock-In Process:** Open the **Inventory Control** panel, click **Stock In**, select the target SKU, specify quantity, and enter a reference number.
3. **Stock-Out Process (Issuing Parts):** Click **Stock Out**, specify quantity, employee name, and maintenance ticket reference. If the stock falls below the safety threshold, a warning badge is triggered.
4. **Suppliers & Purchase Orders:** Administrative staff can issue Purchase Orders to suppliers. When order shipment arrives on the factory floor, the operator logs into the **Suppliers & Orders** panel and clicks **Receive** to automatically update stock.
5. **Database Backups:** Administrators can click **Run Backup Staging** in the security panel to backup database files.
6. **Tamper Check:** Clicking **Verify Database Integrity** runs an instant HMAC SHA-256 signature check of all rows to discover database tampering.
