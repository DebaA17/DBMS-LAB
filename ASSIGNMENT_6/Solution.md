# SQL & PL/SQL Solutions – Assignment 6 (Leap Year)

> Target DB: **Oracle Database Express Edition (Oracle XE)**

---

## 1. Create Table

```sql
CREATE TABLE Leapyear (
	year NUMBER(4) PRIMARY KEY
);
```

---

## 2. PL/SQL Code

This PL/SQL block checks whether a given year `y` is a leap year. If it is, it inserts it into the `Leapyear` table and prints a confirmation message. Otherwise, it prints a message stating it is not a leap year.

```sql
DECLARE
	y NUMBER := 2024;
BEGIN
	IF (MOD(y,4)=0 AND MOD(y,100)<>0) OR MOD(y,400)=0 THEN
		INSERT INTO Leapyear VALUES(y);
		DBMS_OUTPUT.PUT_LINE(y || ' is a Leap Year and inserted into table.');
	ELSE
		DBMS_OUTPUT.PUT_LINE(y || ' is NOT a Leap Year.');
	END IF;
	COMMIT;
END;
/
```

---

## 3. Verify Table Contents

```sql
SELECT * FROM Leapyear;
```
