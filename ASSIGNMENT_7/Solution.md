# SQL Solutions – Assignment 7 (Banking Schema)

> Target DB: **Oracle Database Express Edition (Oracle XE)**

---

## 1. Create Tables

**(A) Branch**

```sql
CREATE TABLE Branch (
	branch_name VARCHAR2(50) PRIMARY KEY,
	branch_city VARCHAR2(50) NOT NULL,
	assets      NUMBER(15,2) NOT NULL
);
```

**(B) Customer**

```sql
CREATE TABLE Customer (
	customer_name VARCHAR2(50) PRIMARY KEY,
	street        VARCHAR2(50),
	city          VARCHAR2(50) NOT NULL
);
```

**(C) Loan**

```sql
CREATE TABLE Loan (
	loan_no     VARCHAR2(20) PRIMARY KEY,
	branch_name VARCHAR2(50) NOT NULL,
	amount      NUMBER(12,2) NOT NULL,
	CONSTRAINT fk_loan_branch
		FOREIGN KEY (branch_name) REFERENCES Branch(branch_name)
);
```

**(D) Borrower**

```sql
CREATE TABLE Borrower (
	customer_name VARCHAR2(50),
	loan_no       VARCHAR2(20),
	CONSTRAINT pk_borrower
		PRIMARY KEY (customer_name, loan_no),
	CONSTRAINT fk_borrower_customer
		FOREIGN KEY (customer_name) REFERENCES Customer(customer_name),
	CONSTRAINT fk_borrower_loan
		FOREIGN KEY (loan_no) REFERENCES Loan(loan_no)
);
```

**(E) Account**

```sql
CREATE TABLE Account (
	account_no  VARCHAR2(20) PRIMARY KEY,
	branch_name VARCHAR2(50) NOT NULL,
	balance     NUMBER(12,2) NOT NULL,
	CONSTRAINT fk_account_branch
		FOREIGN KEY (branch_name) REFERENCES Branch(branch_name)
);
```

**(F) Depositor**

```sql
CREATE TABLE Depositor (
	customer_name VARCHAR2(50),
	account_no    VARCHAR2(20),
	CONSTRAINT pk_depositor
		PRIMARY KEY (customer_name, account_no),
	CONSTRAINT fk_depositor_customer
		FOREIGN KEY (customer_name) REFERENCES Customer(customer_name),
	CONSTRAINT fk_depositor_account
		FOREIGN KEY (account_no) REFERENCES Account(account_no)
);
```

---

## 2. Insert Data

**(A) Insert into Branch**

```sql
INSERT ALL
	INTO Branch (branch_name, branch_city, assets) VALUES ('Salt Lake',       'Kolkata', 50000000)
	INTO Branch (branch_name, branch_city, assets) VALUES ('Park Street',     'Kolkata', 80000000)
	INTO Branch (branch_name, branch_city, assets) VALUES ('Chandni Chowk',   'Delhi',   35000000)
	INTO Branch (branch_name, branch_city, assets) VALUES ('Connaught Place', 'Delhi',   60000000)
SELECT * FROM dual;
```

**(B) Insert into Customer**

```sql
INSERT ALL
	INTO Customer (customer_name, street, city) VALUES ('Amit Sen',       'Salt Lake Sec-1',   'Kolkata')
	INTO Customer (customer_name, street, city) VALUES ('Rahul Roy',      'Gariahat Road',     'Kolkata')
	INTO Customer (customer_name, street, city) VALUES ('Priya Sharma',   'Connaught Circus',  'Delhi')
	INTO Customer (customer_name, street, city) VALUES ('Neha Gupta',     'Karol Bagh',        'Delhi')
	INTO Customer (customer_name, street, city) VALUES ('Vikram Malhotra', 'Bandra',            'Mumbai')
SELECT * FROM dual;
```

**(C) Insert into Loan**

```sql
INSERT ALL
	INTO Loan (loan_no, branch_name, amount) VALUES ('L201', 'Park Street',     150000)
	INTO Loan (loan_no, branch_name, amount) VALUES ('L202', 'Connaught Place', 200000)
	INTO Loan (loan_no, branch_name, amount) VALUES ('L203', 'Connaught Place', 250000)
SELECT * FROM dual;
```

**(D) Insert into Borrower**

```sql
INSERT ALL
	INTO Borrower (customer_name, loan_no) VALUES ('Rahul Roy',      'L201')
	INTO Borrower (customer_name, loan_no) VALUES ('Neha Gupta',     'L202')
	INTO Borrower (customer_name, loan_no) VALUES ('Vikram Malhotra', 'L203')
SELECT * FROM dual;
```

**(E) Insert into Account**

```sql
INSERT ALL
	INTO Account (account_no, branch_name, balance) VALUES ('A101', 'Salt Lake',       15000)
	INTO Account (account_no, branch_name, balance) VALUES ('A102', 'Park Street',     35000)
	INTO Account (account_no, branch_name, balance) VALUES ('A103', 'Chandni Chowk',   12000)
	INTO Account (account_no, branch_name, balance) VALUES ('A104', 'Salt Lake',       55000)
	INTO Account (account_no, branch_name, balance) VALUES ('A105', 'Connaught Place', 8000)
SELECT * FROM dual;
```

**(F) Insert into Depositor**

```sql
INSERT ALL
	INTO Depositor (customer_name, account_no) VALUES ('Amit Sen',       'A101')
	INTO Depositor (customer_name, account_no) VALUES ('Rahul Roy',      'A102')
	INTO Depositor (customer_name, account_no) VALUES ('Priya Sharma',   'A103')
	INTO Depositor (customer_name, account_no) VALUES ('Neha Gupta',     'A104')
	INTO Depositor (customer_name, account_no) VALUES ('Vikram Malhotra', 'A105')
SELECT * FROM dual;
```

---

# Queries and Answers

---

### (a) Give the customer name who has account but not any loan.

```sql
SELECT DISTINCT customer_name
FROM Depositor
WHERE customer_name NOT IN (
	SELECT customer_name
	FROM Borrower
)
ORDER BY customer_name;
```

---

### (b) Give the name of the customer who has either (10000-20000) or (30000-40000) in their account.

```sql
SELECT DISTINCT d.customer_name
FROM Depositor d
JOIN Account a ON d.account_no = a.account_no
WHERE a.balance BETWEEN 10000 AND 20000
   OR a.balance BETWEEN 30000 AND 40000
ORDER BY d.customer_name;
```

---

### (c) Which branch has issued maximum amount of loan?

```sql
SELECT branch_name, SUM(amount) AS total_loan_amount
FROM Loan
GROUP BY branch_name
HAVING SUM(amount) = (
	SELECT MAX(SUM(amount))
	FROM Loan
	GROUP BY branch_name
);
```

---

### (d) Give the name of the customer who has maximum balance in their account.

```sql
SELECT DISTINCT d.customer_name
FROM Depositor d
JOIN Account a ON d.account_no = a.account_no
WHERE a.balance = (
	SELECT MAX(balance)
	FROM Account
);
```

---

### (e) Give the name of the customer who has opened an account in a city in which he is not located.

```sql
SELECT DISTINCT c.customer_name
FROM Customer c
JOIN Depositor d ON c.customer_name = d.customer_name
JOIN Account a ON d.account_no = a.account_no
JOIN Branch b ON a.branch_name = b.branch_name
WHERE c.city <> b.branch_city
ORDER BY c.customer_name;
```
