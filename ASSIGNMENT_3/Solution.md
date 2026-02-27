# SQL Solutions – Assignment 3 (Parts, Supplier, Cost)

> Target DB: **Oracle Database Express Edition (Oracle XE)**

---

## 1. Create Tables

**(A) Parts(p_id, p_name) where p_name should start with 'P'**

```sql
CREATE TABLE Parts (
	p_id   VARCHAR2(10) PRIMARY KEY,
	p_name VARCHAR2(50) NOT NULL,
	CONSTRAINT chk_parts_name
		CHECK (p_name LIKE 'P%')
);
```

**(B) Supplier(s_id, s_name) where s_name should start with 'S'**

```sql
CREATE TABLE Supplier (
	s_id   VARCHAR2(10) PRIMARY KEY,
	s_name VARCHAR2(50) NOT NULL,
	CONSTRAINT chk_supplier_name
		CHECK (s_name LIKE 'S%')
);
```

**(C) Cost(s_id, p_id, cost)**

```sql
CREATE TABLE Cost (
	s_id VARCHAR2(10) NOT NULL,
	p_id VARCHAR2(10) NOT NULL,
	cost NUMBER(10,2) NOT NULL,
	CONSTRAINT pk_cost PRIMARY KEY (s_id, p_id),
	CONSTRAINT fk_cost_supplier FOREIGN KEY (s_id) REFERENCES Supplier (s_id),
	CONSTRAINT fk_cost_parts    FOREIGN KEY (p_id) REFERENCES Parts (p_id),
	CONSTRAINT chk_cost_positive CHECK (cost > 0)
);
```

---

## 2. Insert Adequate Records

```sql
INSERT ALL
	INTO Parts (p_id, p_name) VALUES ('P1', 'PEN')
	INTO Parts (p_id, p_name) VALUES ('P2', 'PAPER')
	INTO Parts (p_id, p_name) VALUES ('P3', 'PENCIL')
	INTO Parts (p_id, p_name) VALUES ('P4', 'PCLIP')
	INTO Parts (p_id, p_name) VALUES ('P5', 'PAD')
	INTO Parts (p_id, p_name) VALUES ('P6', 'PLATE')
SELECT * FROM dual;

INSERT ALL
	INTO Supplier (s_id, s_name) VALUES ('S1', 'SOne')
	INTO Supplier (s_id, s_name) VALUES ('S2', 'STwo')
	INTO Supplier (s_id, s_name) VALUES ('S3', 'SThree')
SELECT * FROM dual;

INSERT ALL
	-- Supplier S1
	INTO Cost (s_id, p_id, cost) VALUES ('S1', 'P1',  5)
	INTO Cost (s_id, p_id, cost) VALUES ('S1', 'P2', 12)
	INTO Cost (s_id, p_id, cost) VALUES ('S1', 'P3',  8)
	INTO Cost (s_id, p_id, cost) VALUES ('S1', 'P4', 20)
	INTO Cost (s_id, p_id, cost) VALUES ('S1', 'P5',  7)
	-- Supplier S2
	INTO Cost (s_id, p_id, cost) VALUES ('S2', 'P2', 11)
	INTO Cost (s_id, p_id, cost) VALUES ('S2', 'P3',  9)
	INTO Cost (s_id, p_id, cost) VALUES ('S2', 'P4', 18)
	INTO Cost (s_id, p_id, cost) VALUES ('S2', 'P6',  6)
	-- Supplier S3
	INTO Cost (s_id, p_id, cost) VALUES ('S3', 'P2', 10)
	INTO Cost (s_id, p_id, cost) VALUES ('S3', 'P4', 25)
	INTO Cost (s_id, p_id, cost) VALUES ('S3', 'P6',  7)
SELECT * FROM dual;

COMMIT;
```

---

# Queries and Answers

---

### (i) Display the parts’ name supplied by supplier S1.

```sql
SELECT DISTINCT p.p_name
FROM Parts p
JOIN Cost c ON c.p_id = p.p_id
WHERE c.s_id = 'S1'
ORDER BY p.p_name;
```

---

### (ii) Display the number of parts supplied by each supplier.

```sql
SELECT c.s_id, COUNT(DISTINCT c.p_id) AS parts_count
FROM Cost c
GROUP BY c.s_id
ORDER BY c.s_id;
```

---

### (iii) Display the names of the parts supplied by supplier S1 only.

```sql
SELECT p.p_name
FROM Parts p
JOIN Cost c ON c.p_id = p.p_id
WHERE c.s_id = 'S1'
  AND NOT EXISTS (
		SELECT 1
		FROM Cost c2
		WHERE c2.p_id = c.p_id
		  AND c2.s_id <> 'S1'
  )
ORDER BY p.p_name;
```

---

### (iv) Display the name of the parts supplied by all the suppliers.

```sql
SELECT p.p_name
FROM Parts p
JOIN Cost c ON c.p_id = p.p_id
GROUP BY p.p_id, p.p_name
HAVING COUNT(DISTINCT c.s_id) = (SELECT COUNT(*) FROM Supplier)
ORDER BY p.p_name;
```

---

### (v) Display the name of the parts supplied by both S1 and S2.

```sql
SELECT p.p_name
FROM Parts p
JOIN Cost c ON c.p_id = p.p_id
WHERE c.s_id IN ('S1', 'S2')
GROUP BY p.p_id, p.p_name
HAVING COUNT(DISTINCT c.s_id) = 2
ORDER BY p.p_name;
```

---

### (vi) Display the supplier name who supplies parts of maximum cost.

```sql
SELECT DISTINCT s.s_name
FROM Supplier s
JOIN Cost c ON c.s_id = s.s_id
WHERE c.cost = (SELECT MAX(cost) FROM Cost);
```

---

### (vii) Display the part and supplier id’s for the three lowest cost parts.

```sql
SELECT s_id, p_id, cost
FROM (
	SELECT s_id, p_id, cost
	FROM Cost
	ORDER BY cost ASC, s_id, p_id
)
WHERE ROWNUM <= 3;
```

---

### (viii) Display the part name with minimum cost.

```sql
SELECT DISTINCT p.p_name
FROM Parts p
JOIN Cost c ON c.p_id = p.p_id
WHERE c.cost = (SELECT MIN(cost) FROM Cost)
ORDER BY p.p_name;
```

---

### (ix) Find the total number of parts supplied by supplier S1.

```sql
SELECT COUNT(DISTINCT p_id) AS total_parts_by_s1
FROM Cost
WHERE s_id = 'S1';
```

---

### (x) Find the total number of parts supplied by supplier S2 with cost greater than Rs. 10.

```sql
SELECT COUNT(DISTINCT p_id) AS total_parts_by_s2_cost_gt_10
FROM Cost
WHERE s_id = 'S2'
  AND cost > 10;
```
