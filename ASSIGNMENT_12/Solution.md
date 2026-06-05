# SQL Solutions – Assignment 12 (Banking Schema II)

> Target DB: **Oracle Database Express Edition (Oracle XE)**

---

## 1. Create Tables

**(A) Branch**

```sql
CREATE TABLE Branch (
	BName  VARCHAR2(50) PRIMARY KEY,
	BCity  VARCHAR2(50) NOT NULL,
	Assets NUMBER(15,2) NOT NULL
);
```

**(B) Customer**

```sql
CREATE TABLE Customer (
	CName VARCHAR2(50) PRIMARY KEY,
	CCity VARCHAR2(50) NOT NULL
);
```

**(C) Loan**

```sql
CREATE TABLE Loan (
	LoanNo VARCHAR2(20) PRIMARY KEY,
	BName  VARCHAR2(50) NOT NULL,
	Amount NUMBER(12,2) NOT NULL,
	CONSTRAINT fk_loan_branch
		FOREIGN KEY (BName) REFERENCES Branch(BName)
);
```

**(D) Borrower**

```sql
CREATE TABLE Borrower (
	CName  VARCHAR2(50),
	LoanNo VARCHAR2(20),
	CONSTRAINT pk_borrower
		PRIMARY KEY (CName, LoanNo),
	CONSTRAINT fk_borrower_customer
		FOREIGN KEY (CName) REFERENCES Customer(CName),
	CONSTRAINT fk_borrower_loan
		FOREIGN KEY (LoanNo) REFERENCES Loan(LoanNo)
);
```

**(E) Account**

```sql
CREATE TABLE Account (
	AccNo   VARCHAR2(20) PRIMARY KEY,
	BName   VARCHAR2(50) NOT NULL,
	Balance NUMBER(12,2) NOT NULL,
	CONSTRAINT fk_account_branch
		FOREIGN KEY (BName) REFERENCES Branch(BName)
);
```

**(F) Depositor**

```sql
CREATE TABLE Depositor (
	CName VARCHAR2(50),
	AccNo VARCHAR2(20),
	CONSTRAINT pk_depositor
		PRIMARY KEY (CName, AccNo),
	CONSTRAINT fk_depositor_customer
		FOREIGN KEY (CName) REFERENCES Customer(CName),
	CONSTRAINT fk_depositor_account
		FOREIGN KEY (AccNo) REFERENCES Account(AccNo)
);
```

---

## 2. Insert Data

**(A) Insert into Branch**

```sql
INSERT ALL
	INTO Branch (BName, BCity, Assets) VALUES ('Salt Lake',       'Kolkata', 500000)
	INTO Branch (BName, BCity, Assets) VALUES ('Park Street',     'Kolkata', 30000)
	INTO Branch (BName, BCity, Assets) VALUES ('Connaught Place', 'Delhi',   700000)
	INTO Branch (BName, BCity, Assets) VALUES ('Chandni Chowk',   'Delhi',   25000)
	INTO Branch (BName, BCity, Assets) VALUES ('Bandra',          'Mumbai',  900000)
SELECT * FROM dual;
```

**(B) Insert into Customer**

```sql
INSERT ALL
	INTO Customer (CName, CCity) VALUES ('Debasis Biswas',   'Kolkata')
	INTO Customer (CName, CCity) VALUES ('Rahul Roy',       'Kolkata')
	INTO Customer (CName, CCity) VALUES ('Priya Sharma',    'Delhi')
	INTO Customer (CName, CCity) VALUES ('Neha Gupta',      'Delhi')
	INTO Customer (CName, CCity) VALUES ('Vikram Malhotra', 'Mumbai')
	INTO Customer (CName, CCity) VALUES ('Sagar Mehta',     'Mumbai')
SELECT * FROM dual;
```

**(C) Insert into Loan**

```sql
INSERT ALL
	INTO Loan (LoanNo, BName, Amount) VALUES ('L201', 'Park Street',     45000)
	INTO Loan (LoanNo, BName, Amount) VALUES ('L202', 'Connaught Place', 200000)
	INTO Loan (LoanNo, BName, Amount) VALUES ('L203', 'Bandra',          250000)
	INTO Loan (LoanNo, BName, Amount) VALUES ('L204', 'Bandra',          30000)
SELECT * FROM dual;
```

**(D) Insert into Borrower**

```sql
INSERT ALL
	INTO Borrower (CName, LoanNo) VALUES ('Rahul Roy',       'L201')
	INTO Borrower (CName, LoanNo) VALUES ('Neha Gupta',      'L202')
	INTO Borrower (CName, LoanNo) VALUES ('Vikram Malhotra', 'L203')
	INTO Borrower (CName, LoanNo) VALUES ('Sagar Mehta',     'L204')
SELECT * FROM dual;
```

**(E) Insert into Account**

```sql
INSERT ALL
	INTO Account (AccNo, BName, Balance) VALUES ('A101', 'Salt Lake',       15000)
	INTO Account (AccNo, BName, Balance) VALUES ('A102', 'Park Street',     35000)
	INTO Account (AccNo, BName, Balance) VALUES ('A103', 'Chandni Chowk',   5000)
	INTO Account (AccNo, BName, Balance) VALUES ('A104', 'Salt Lake',       8000)
	INTO Account (AccNo, BName, Balance) VALUES ('A105', 'Bandra',          12000)
SELECT * FROM dual;
```

**(F) Insert into Depositor**

```sql
INSERT ALL
	INTO Depositor (CName, AccNo) VALUES ('Debasis Biswas',   'A101')
	INTO Depositor (CName, AccNo) VALUES ('Rahul Roy',       'A102')
	INTO Depositor (CName, AccNo) VALUES ('Priya Sharma',    'A103')
	INTO Depositor (CName, AccNo) VALUES ('Neha Gupta',      'A104')
	INTO Depositor (CName, AccNo) VALUES ('Vikram Malhotra', 'A105')
	INTO Depositor (CName, AccNo) VALUES ('Vikram Malhotra', 'A102')
SELECT * FROM dual;
```

---

# Queries and Answers

---

### i) List the names of those branches that have assets in between 20000 and 40000.

```sql
SELECT BName
FROM Branch
WHERE Assets BETWEEN 20000 AND 40000
ORDER BY BName;
```

---

### ii) List the names of those customers along with the branch names who have an account in the same city as they live in.

```sql
SELECT d.CName, a.BName
FROM Depositor d
JOIN Account a ON d.AccNo = a.AccNo
JOIN Branch b ON a.BName = b.BName
JOIN Customer c ON d.CName = c.CName
WHERE c.CCity = b.BCity
ORDER BY d.CName;
```

---

### iii) Write the names of those customers who have an account, a loan or both.

```sql
SELECT CName FROM Depositor
UNION
SELECT CName FROM Borrower
ORDER BY CName;
```

---

### iv) Write the names of those customers who have both an account and a loan.

```sql
SELECT CName FROM Depositor
INTERSECT
SELECT CName FROM Borrower
ORDER BY CName;
```

---

### v) Write the names of those customers who have either an account or a loan.

*Note: Depending on interpretation, "either ... or" can mean a standard Logical Union (both included) or Symmetric Difference (has one but not both). Both versions are provided below.*

**Option A: Has one or the other, but not both (Symmetric Difference / XOR)**

```sql
-- Method 1: Using subqueries (Recommended)
SELECT CName FROM (
	SELECT CName FROM Depositor
	MINUS
	SELECT CName FROM Borrower
)
UNION
SELECT CName FROM (
	SELECT CName FROM Borrower
	MINUS
	SELECT CName FROM Depositor
)
ORDER BY CName;
```

**Alternative: Using GROUP BY and HAVING**

```sql
SELECT CName
FROM (
	SELECT DISTINCT CName FROM Depositor
	UNION ALL
	SELECT DISTINCT CName FROM Borrower
)
GROUP BY CName
HAVING COUNT(*) = 1
ORDER BY CName;
```

**Option B: Has an account, a loan, or both (Logical Union)**

```sql
SELECT CName FROM Depositor
UNION
SELECT CName FROM Borrower
ORDER BY CName;
```

---

### vi) Write the names of all customers having account balance more than 10000.

```sql
SELECT DISTINCT d.CName
FROM Depositor d
JOIN Account a ON d.AccNo = a.AccNo
WHERE a.Balance > 10000
ORDER BY d.CName;
```

---

### vii) Write the names of all customers along with branch name and branch city having account balance less than 10000.

```sql
SELECT d.CName, a.BName, b.BCity
FROM Depositor d
JOIN Account a ON d.AccNo = a.AccNo
JOIN Branch b ON a.BName = b.BName
WHERE a.Balance < 10000
ORDER BY d.CName;
```

---

### viii) Write the names of all customers along with branch name, branch city and customer city having account balance between 10000 and 20000.

```sql
SELECT d.CName, a.BName, b.BCity, c.CCity
FROM Depositor d
JOIN Account a ON d.AccNo = a.AccNo
JOIN Branch b ON a.BName = b.BName
JOIN Customer c ON d.CName = c.CName
WHERE a.Balance BETWEEN 10000 AND 20000
ORDER BY d.CName;
```

---

### ix) List the names of those customers along with branch name for those customers who have a loan amount more than account balance.

```sql
SELECT DISTINCT d.CName, a.BName
FROM Depositor d
JOIN Account a ON d.AccNo = a.AccNo
JOIN Borrower b ON d.CName = b.CName
JOIN Loan l ON b.LoanNo = l.LoanNo
WHERE l.Amount > a.Balance
ORDER BY d.CName;
```

---

### x) List the names of those customers who have an account but no loan.

```sql
SELECT CName FROM Depositor
MINUS
SELECT CName FROM Borrower
ORDER BY CName;
```

---

### xi) List the branch name along with branch city that issued highest loan amount.

```sql
SELECT b.BName, b.BCity
FROM Branch b
JOIN Loan l ON b.BName = l.BName
GROUP BY b.BName, b.BCity
HAVING SUM(l.Amount) = (
	SELECT MAX(SUM(Amount))
	FROM Loan
	GROUP BY BName
);
```

---

### xii) List the names of those customers who has opened an account in a city in which he is not located.

```sql
SELECT DISTINCT d.CName
FROM Depositor d
JOIN Account a ON d.AccNo = a.AccNo
JOIN Branch b ON a.BName = b.BName
JOIN Customer c ON d.CName = c.CName
WHERE c.CCity <> b.BCity
ORDER BY d.CName;
```

---

### xiii) List the branch city along with total amount of loan issued by the banks.

```sql
SELECT b.BCity, SUM(l.Amount) AS Total_Loan_Amount
FROM Branch b
JOIN Loan l ON b.BName = l.BName
GROUP BY b.BCity
ORDER BY b.BCity;
```

---

### xiv) List the names of those customers who have an account in a branch in Kolkata but have a loan at a bank in Mumbai.

```sql
SELECT DISTINCT d.CName
FROM Depositor d
JOIN Account a ON d.AccNo = a.AccNo
JOIN Branch b1 ON a.BName = b1.BName
JOIN Borrower br ON d.CName = br.CName
JOIN Loan l ON br.LoanNo = l.LoanNo
JOIN Branch b2 ON l.BName = b2.BName
WHERE b1.BCity = 'Kolkata'
  AND b2.BCity = 'Mumbai'
ORDER BY d.CName;
```
