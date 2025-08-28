### R001 - Avoid console.log in production
pattern: console\.log
severity: HIGH
message: Avoid console.log in production code.

### R002 - Constants must be UPPER_CASE (Java)
pattern: public\s+static\s+final\s+\w+\s+[a-z]+ =
severity: MEDIUM
message: Constant variables should be UPPER_CASE (e.g., MAX_VALUE).
