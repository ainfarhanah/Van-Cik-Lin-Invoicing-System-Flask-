# Van Cik Lin Invoicing-System

A web based invoicing and payment tracking system built using **Python Flask** and **MySQL** for a small school van service.

This project was developed as a **personal learning project** to explore web development with Python while solving a real-world problem for my mom's school van service business.


## Project Overview

This project helps manage:
- Customer information
- Invoice records
- Payment tracking
- Basic business insight through a visualization dashboard

Previously, all records were manage manually. This system aims to improve ogranization, reduce errors, and provide clearer visibility of monthly payments and outstanding balances.

---

## ERD Diagram
```mermaid
erDiagram
	direction LR
	USERS{
		int id  ""  
		string username  ""  
		string email  ""  
		string password  ""  
		created_at timestamp  ""  
	}

	CUSTOMERS {
		int custID  ""  
		string custName  ""  
		string custPhone  ""  
		created_at timestamp  ""  
	}

    CHILDREN{
        int childID
        string childName
        string childCategory 
        int childAge
        int custID
        created_at timestamp
    }

	SERVICES {
		int serviceID  ""  
		string serviceName  ""  
		string serviceDesc  ""  
		float serviceFee  ""  
		created_at timestamp  ""  
	}

	INVOICES {
		int invID  ""  
		date invDate  ""  
		date invDue  ""  
		id serviceID  ""  
		string invDesc  ""  
		float invAmt  ""  
		float invPaid  ""  
		float invTotal  ""  
		string invStatus  ""  
		created_at timestamp  ""  
	}

	ITEMS {
		int itemID  ""  
		float itemPrice  ""  
		int itemQty  ""  
		float itemAmt  ""  
		created_at timestamp  ""  
	}

	PAYMENTS {
		int paymentID  ""  
		string paymentMethod  ""  
		int userID  ""  
		int invoiceID  ""  
		created_at timestamp  ""  
	}

	USERS||--o{CUSTOMERS:"has"
	USERS||--o{SERVICES:"provides"
	USERS||--o{INVOICES:"creates"
	INVOICES||--o{ITEMS:"has"
	INVOICES||--o{SERVICES:"has"
	INVOICES||--o{CUSTOMERS:"has"
	USERS||--o{PAYMENTS:"creates"
	PAYMENTS||--o{INVOICES:"has"
	CUSTOMERS||--o{PAYMENTS:"pay"
    CUSTOMERS ||--o{ CHILDREN: "has"
```


## Tech Stack

- **Backend**: Python Flask
- **Database**: MySQL (mysqldb)
- **Frontend**: HTML, CSS, JavaScript
- **Charting**: Chart.js

## Key Features

- **User Authentication**: Secure login and registration
- **Invoice Management**: Create, view, and manage invoices
- **Payment Tracking**: Track payments and outstanding balances
- **Dashboard**: Visualize key metrics and trends



