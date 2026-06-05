# SQL Solutions – Assignment 10 (Shipment & Truck Schema)

> Target DB: **Oracle Database Express Edition (Oracle XE)**

*Note: In Oracle SQL, hyphens in table or column names are replaced with underscores (e.g. `cust_id` instead of `cust-id`, `truck_no` instead of `truck-no`) to comply with standard SQL identifier naming rules.*

---

## 1. Create Tables

**(A) Customer**

```sql
CREATE TABLE Customer (
	cust_id        NUMBER PRIMARY KEY,
	cust_name      VARCHAR2(100) NOT NULL,
	annual_revenue NUMBER(15,2) NOT NULL,
	cust_type      VARCHAR2(20) NOT NULL,
	CONSTRAINT chk_cust_type
		CHECK (cust_type IN ('manufacturer', 'wholesaler', 'retailer', 'distributor'))
);
```

**(B) Truck**

```sql
CREATE TABLE Truck (
	truck_no    VARCHAR2(20) PRIMARY KEY,
	driver_name VARCHAR2(100) NOT NULL
);
```

**(C) City**

```sql
CREATE TABLE City (
	city_name  VARCHAR2(50) PRIMARY KEY,
	population NUMBER NOT NULL
);
```

**(D) Shipment**

```sql
CREATE TABLE Shipment (
	shipment_no      VARCHAR2(20) PRIMARY KEY,
	cust_id          NUMBER NOT NULL,
	weight           NUMBER(10,2) NOT NULL,
	truck_no         VARCHAR2(20) NOT NULL,
	start_city       VARCHAR2(50) NOT NULL,
	destination_city VARCHAR2(50) NOT NULL,
	CONSTRAINT fk_shipment_customer
		FOREIGN KEY (cust_id) REFERENCES Customer(cust_id),
	CONSTRAINT fk_shipment_truck
		FOREIGN KEY (truck_no) REFERENCES Truck(truck_no),
	CONSTRAINT fk_shipment_start_city
		FOREIGN KEY (start_city) REFERENCES City(city_name),
	CONSTRAINT fk_shipment_dest_city
		FOREIGN KEY (destination_city) REFERENCES City(city_name)
);
```

**(E) Sequence (Auto-increment cust_id starting from 100)**

```sql
CREATE SEQUENCE Customer_Seq
	START WITH 100
	INCREMENT BY 1;
```

**(F) Trigger (Auto-fill cust_id)**

```sql
CREATE OR REPLACE TRIGGER Customer_BI
BEFORE INSERT ON Customer
FOR EACH ROW
WHEN (NEW.cust_id IS NULL)
BEGIN
	SELECT Customer_Seq.NEXTVAL
	INTO :NEW.cust_id
	FROM dual;
END;
/
```

---

## 2. Insert Data

**(A) Insert into Customer**

```sql
INSERT ALL
	INTO Customer (cust_name, annual_revenue, cust_type) VALUES ('Alpha Ind', 5000000, 'manufacturer')
	INTO Customer (cust_name, annual_revenue, cust_type) VALUES ('Beta Corp', 12000000, 'wholesaler')
	INTO Customer (cust_name, annual_revenue, cust_type) VALUES ('Gamma Retail', 3000000, 'retailer')
	INTO Customer (cust_name, annual_revenue, cust_type) VALUES ('Delta Dist', 8000000, 'distributor')
	INTO Customer (cust_name, annual_revenue, cust_type) VALUES ('Ashton Log', 4500000, 'wholesaler')
SELECT * FROM dual;
```

**(B) Insert into Truck**

```sql
INSERT ALL
	INTO Truck (truck_no, driver_name) VALUES ('T501', 'Priya')
	INTO Truck (truck_no, driver_name) VALUES ('T502', 'Amit')
	INTO Truck (truck_no, driver_name) VALUES ('T503', 'Arjun')
	INTO Truck (truck_no, driver_name) VALUES ('T504', 'Karan')
SELECT * FROM dual;
```

**(C) Insert into City**

```sql
INSERT ALL
	INTO City (city_name, population) VALUES ('Kolkata', 15000000)
	INTO City (city_name, population) VALUES ('Delhi', 20000000)
	INTO City (city_name, population) VALUES ('Mumbai', 22000000)
	INTO City (city_name, population) VALUES ('Chennai', 8000000)
	INTO City (city_name, population) VALUES ('Bangalore', 12000000)
SELECT * FROM dual;
```

**(D) Insert into Shipment**

```sql
INSERT ALL
	INTO Shipment (shipment_no, cust_id, weight, truck_no, start_city, destination_city) VALUES ('S901', 100, 150.50, 'T501', 'Delhi', 'Delhi')
	INTO Shipment (shipment_no, cust_id, weight, truck_no, start_city, destination_city) VALUES ('S902', 101, 250.00, 'T503', 'Kolkata', 'Delhi')
	INTO Shipment (shipment_no, cust_id, weight, truck_no, start_city, destination_city) VALUES ('S903', 102, 300.00, 'T503', 'Delhi', 'Mumbai')
	INTO Shipment (shipment_no, cust_id, weight, truck_no, start_city, destination_city) VALUES ('S904', 103, 100.00, 'T503', 'Mumbai', 'Chennai')
	INTO Shipment (shipment_no, cust_id, weight, truck_no, start_city, destination_city) VALUES ('S905', 104, 180.00, 'T501', 'Kolkata', 'Chennai')
	INTO Shipment (shipment_no, cust_id, weight, truck_no, start_city, destination_city) VALUES ('S906', 100, 220.00, 'T502', 'Chennai', 'Bangalore')
SELECT * FROM dual;
```

---

## 3. User-Friendly Form Design (Customer Table)

The following is a clean form layout designed to safely capture input for inserting records into the **Customer** table.

### Form Controls & Validations

| Field Label | Input Control Type | Validation Rules / HTML Attributes |
| :--- | :--- | :--- |
| **Customer Name** | Text Input | `required`, `maxlength="100"` |
| **Annual Revenue** | Number Input | `required`, `min="0"`, `step="0.01"` |
| **Customer Type** | Dropdown Select | `required` (Options: Manufacturer, Wholesaler, Retailer, Distributor) |

*Note: The `cust_id` field is omitted from the form design as it is automatically generated starting from 100 via the database sequence and trigger.*

---

# Queries and Answers

---

### (i) Give the details for those shipments where the start-city and destination-city are same.

```sql
SELECT *
FROM Shipment
WHERE start_city = destination_city;
```

---

### (ii) Give the driver names who participated in maximum numbers of shipments?

```sql
SELECT t.driver_name, COUNT(s.shipment_no) AS shipment_count
FROM Truck t
JOIN Shipment s ON t.truck_no = s.truck_no
GROUP BY t.truck_no, t.driver_name
HAVING COUNT(s.shipment_no) = (
	SELECT MAX(COUNT(shipment_no))
	FROM Shipment
	GROUP BY truck_no
);
```

---

### (iii) Give the name of the city never appears in destination-city.

```sql
SELECT city_name
FROM City
WHERE city_name NOT IN (
	SELECT DISTINCT destination_city
	FROM Shipment
	WHERE destination_city IS NOT NULL
)
ORDER BY city_name;
```

---

### (iv) Give the name of the cities whose population is more than the average of all the cities.

```sql
SELECT city_name
FROM City
WHERE population > (
	SELECT AVG(population)
	FROM City
)
ORDER BY city_name;
```

---

### (v) Give the shipment details where the starting character of customer name and the last character of driver name is 'A'.

```sql
SELECT s.*
FROM Shipment s
JOIN Customer c ON s.cust_id = c.cust_id
JOIN Truck t ON s.truck_no = t.truck_no
WHERE UPPER(SUBSTR(c.cust_name, 1, 1)) = 'A'
  AND UPPER(SUBSTR(t.driver_name, -1)) = 'A';
```
