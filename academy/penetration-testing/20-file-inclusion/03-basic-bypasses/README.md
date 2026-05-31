# Basic Bypasses

## [+] Concept Overview
Applications often implement naive filters to prevent path traversal (e.g., stripping `../`). These filters can frequently be bypassed using alternative encodings, non-recursive filtering tricks, or specific OS characteristics.

### Common Bypass Techniques

#### 1. Non-Recursive Stripping Bypass
If the application replaces `../` with an empty string (`""`) only once:
* **Payload**: `....//` or `..././`
* **Result after stripping**: `../`

#### 2. URL Encoding / Double Encoding
If the filter decodes the input before parsing but after validation:
* `.` $\rightarrow$ `%2e`
* `/` $\rightarrow$ `%2f`
* `\` $\rightarrow$ `%5c`
* **Double Encoding**: `%252e%252e%252f` (for `../`)

#### 3. Path Normalization / Absolute Pathing
If the application appends the input to a base directory (e.g., `/var/www/html/`):
* Try referencing absolute paths directly: `/etc/passwd` instead of using traversals.

#### 4. Null Byte Injection (PHP < 5.3.4)
If the application appends a file extension (e.g., `.php`):
* **Payload**: `/etc/passwd%00`
* **Result**: The execution engine terminates the string at the null byte, ignoring the appended extension.
