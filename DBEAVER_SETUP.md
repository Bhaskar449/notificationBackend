# 🐘 DBeaver PostgreSQL Connection Guide

This guide will help you connect your Flask backend's PostgreSQL database to DBeaver GUI for easy database management and visualization.

## 📋 **Database Information**

Based on your current Flask backend configuration:

| Parameter | Value |
|-----------|-------|
| **Database Type** | PostgreSQL |
| **Host** | `localhost` |
| **Port** | `5432` |
| **Database Name** | `flask_backend_db` |
| **Username** | `bhaskarjoshi` |
| **Password** | *(no password - local connection)* |
| **Schema** | `public` |

## 🚀 **Step-by-Step DBeaver Setup**

### **Step 1: Install DBeaver**

If you don't have DBeaver installed:

```bash
# macOS (using Homebrew)
brew install --cask dbeaver-community

# Or download from: https://dbeaver.io/download/
```

### **Step 2: Open DBeaver and Create New Connection**

1. **Launch DBeaver**
2. **Click** on the "New Database Connection" icon (or `File → New → Database Connection`)
3. **Select PostgreSQL** from the database list
4. **Click Next**

### **Step 3: Configure Connection Settings**

In the connection settings dialog, enter the following:

#### **Main Tab:**
```
Server Host:    localhost
Port:           5432
Database:       flask_backend_db
Username:       bhaskarjoshi
Password:       (leave empty)
```

#### **PostgreSQL Tab:**
```
Show all databases: ✓ (checked)
```

#### **Driver Properties Tab:**
No changes needed - use defaults.

### **Step 4: Test Connection**

1. **Click "Test Connection"** button
2. If successful, you should see: ✅ "Connected"
3. If prompted to download drivers, click **"Download"**

### **Step 5: Save and Connect**

1. **Give your connection a name**: `Flask Backend DB`
2. **Click "Finish"**
3. **Double-click** the connection in the Database Navigator to connect

## 📊 **What You'll See in DBeaver**

After connecting, you'll see the following structure:

```
Flask Backend DB
├── Databases
│   └── flask_backend_db
│       └── Schemas
│           └── public
│               ├── Tables
│               │   ├── alembic_version (Migration tracking)
│               │   └── users (Your user data)
│               ├── Views
│               ├── Indexes
│               └── Sequences
```

### **Tables Overview:**

#### **1. users Table**
```sql
Column         | Type                   | Constraints
---------------|------------------------|------------------
id             | integer                | PRIMARY KEY, NOT NULL
username       | character varying(80)  | UNIQUE, NOT NULL
email          | character varying(120) | UNIQUE, NOT NULL
password_hash  | character varying(128) | NOT NULL
first_name     | character varying(50)  | NOT NULL
last_name      | character varying(50)  | NOT NULL
is_active      | boolean                | DEFAULT true
created_at     | timestamp              | DEFAULT now()
updated_at     | timestamp              | DEFAULT now()
```

#### **2. alembic_version Table**
```sql
Column         | Type                   | Purpose
---------------|------------------------|------------------
version_num    | character varying(32)  | Flask-Migrate tracking
```

## 🔍 **Useful DBeaver Features for Your Flask App**

### **1. View Data**
```sql
-- View all users
SELECT * FROM users;

-- View specific user details
SELECT id, username, email, first_name, last_name, is_active, created_at 
FROM users 
WHERE id = 1;
```

### **2. Data Analysis**
```sql
-- Count total users
SELECT COUNT(*) as total_users FROM users;

-- Count active users
SELECT COUNT(*) as active_users FROM users WHERE is_active = true;

-- Recent registrations
SELECT username, email, created_at 
FROM users 
ORDER BY created_at DESC 
LIMIT 10;
```

### **3. Data Management**
```sql
-- Update user information
UPDATE users 
SET first_name = 'Updated Name', updated_at = NOW() 
WHERE id = 1;

-- Deactivate user
UPDATE users 
SET is_active = false, updated_at = NOW() 
WHERE id = 1;
```

## 🛠️ **DBeaver Tips & Tricks**

### **1. SQL Console**
- **Right-click** on your database → **SQL Editor** → **Open SQL Console**
- Write and execute custom SQL queries
- Use `Ctrl+Enter` to execute selected query

### **2. Data Export**
- **Right-click** on table → **Export Data**
- Choose format: CSV, Excel, JSON, etc.
- Useful for data backup or analysis

### **3. ER Diagram**
- **Right-click** on schema → **Generate SQL** → **DDL**
- Or use **Tools** → **ER Diagram** for visual representation

### **4. Database Backup**
- **Right-click** on database → **Tools** → **Dump Database**
- Creates a PostgreSQL dump file for backup

## 🔧 **Troubleshooting**

### **Connection Issues:**

#### **Problem: "Connection refused"**
**Solution:**
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# Start PostgreSQL if not running
brew services start postgresql@14
```

#### **Problem: "Database does not exist"**
**Solution:**
```bash
# Verify database exists
psql -l | grep flask_backend_db

# Create database if missing
createdb flask_backend_db
```

#### **Problem: "Authentication failed"**
**Solution:**
- Ensure username is `bhaskarjoshi`
- Leave password field empty for local connections
- Check PostgreSQL user permissions

### **Permission Issues:**

If you get permission errors:
```bash
# Check current user
whoami

# Connect to PostgreSQL as superuser
psql postgres

# Grant permissions to your user
GRANT ALL PRIVILEGES ON DATABASE flask_backend_db TO bhaskarjoshi;
```

## 📈 **Advanced DBeaver Features**

### **1. Query History**
- View all previously executed queries
- **Window** → **Show View** → **Query Manager**

### **2. Data Editor**
- Double-click any table to open data editor
- Edit data directly in grid format
- Auto-generates UPDATE statements

### **3. Database Monitoring**
- **Window** → **Show View** → **Database Monitor**
- Monitor active connections and queries
- View database performance metrics

### **4. Schema Browser**
- Navigate database structure easily
- Search for tables, columns, and objects
- View dependencies and relationships

## 🔒 **Security Best Practices**

### **For Development:**
✅ Current setup is fine for local development

### **For Production:**
When moving to production, update connection with:
```
Host:       your-production-host
Port:       5432 (or custom port)
Database:   production_db_name
Username:   production_username
Password:   strong_production_password
SSL Mode:   require
```

## 📝 **Quick Reference Commands**

### **Essential SQL Queries for Your Flask App:**

```sql
-- Check user registration data
SELECT 
    id,
    username,
    email,
    first_name || ' ' || last_name as full_name,
    is_active,
    created_at
FROM users
ORDER BY created_at DESC;

-- Find users by email domain
SELECT * FROM users 
WHERE email LIKE '%@gmail.com';

-- Check migration status
SELECT * FROM alembic_version;

-- Database size information
SELECT 
    pg_size_pretty(pg_total_relation_size('users')) as users_table_size,
    pg_size_pretty(pg_database_size('flask_backend_db')) as database_size;
```

---

## ✅ **Connection Summary**

**Your DBeaver connection settings:**
```
Connection Name: Flask Backend DB
Type:           PostgreSQL
Host:           localhost
Port:           5432
Database:       flask_backend_db
Username:       bhaskarjoshi
Password:       (empty)
```

**Test Query:**
After connecting, try this query to verify everything works:
```sql
SELECT 'Connection successful!' as status, COUNT(*) as user_count FROM users;
```

You're now ready to manage your Flask backend database through DBeaver! 🎉 