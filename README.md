# Shopping Management System

A database-driven Shopping Management System built using **Python Flask, HTML, CSS, JavaScript, and MySQL**. This project demonstrates database connectivity, CRUD operations, relational database design, order processing, and sales analytics.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Database Design](#database-design)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [Sales Analytics](#sales-analytics)
- [Database Operations](#database-operations)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

## Overview

The Shopping Management System provides a simple web interface for managing products, customers, and customer orders. It uses MySQL to store application data and Flask to communicate between the frontend and database.

The project is designed as a DBMS assignment to demonstrate how a web application interacts with a relational database to perform data insertion, retrieval, updating, deletion, and reporting.

## Features

### Dashboard
- View total products, customers, and orders.
- Display revenue statistics.
- View recent orders.

### Product Management
- Add new products.
- Edit existing product information.
- Search products by name or category.
- Delete products when database constraints permit.
- Manage product prices, descriptions, and stock quantities.

### Customer Management
- Add customer information.
- View registered customers.
- Delete customers when database constraints permit.

### Order Management
- Place orders containing multiple products.
- Validate product availability before placing an order.
- Calculate order totals automatically.
- Reduce stock quantities after a successful order.
- View order details and purchased items.
- Update order status.

### Sales Analytics
- Display key sales statistics.
- Visualize daily revenue.
- Identify top-selling products.
- Display order status distribution.

*Note: Analytics features require the analytics route and template to be implemented in your project.*

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application programming |
| Flask | Backend web framework |
| HTML5 | Web page structure |
| CSS3 | Styling and layout |
| JavaScript | Client-side functionality |
| MySQL | Relational database |
| MySQL Workbench | Database creation and administration |
| mysql-connector-python | Python-to-MySQL connectivity |
| python-dotenv | Loading environment variables from `.env` |
| Chart.js | Interactive charts for sales analytics |

## Project Structure

```text
shopping_management_system/
├── app.py
├── schema.sql
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── error.html
│   ├── products.html
│   ├── product_form.html
│   ├── customers.html
│   ├── customer_form.html
│   ├── orders.html
│   ├── order_form.html
│   ├── order_detail.html
│   └── analytics.html
└── static/
    ├── style.css
    └── app.js
```

The structure above represents the expected project layout. Adjust it if your actual repository contains different files.

## Database Design

The application uses a MySQL database named `shopping_db`.

### Tables

**1. `products`**

Stores product information, including name, category, price, available quantity, and description.

**2. `customers`**

Stores customer details such as name, email, phone number, and address.

**3. `orders`**

Stores order information, including customer reference, order date, total amount, and status.

**4. `order_items`**

Stores individual products included in each order, including quantity, unit price, and line total.

### Relationships

- One customer can place multiple orders.
- One order can contain multiple order items.
- One product can appear in multiple order items.
- Foreign keys maintain relationships between related records.
- Order items are linked to their corresponding orders and products.

## Prerequisites

Install the following before running the project:

- Python 3.10 or newer
- MySQL Server
- MySQL Workbench
- Git (optional, for cloning the repository)
- A modern web browser

## Installation and Setup

### 1. Clone the repository

If you are using GitHub, run:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd shopping_management_system
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's actual URL.

Alternatively, download the repository as a ZIP file and extract it.

### 2. Create a virtual environment

Run these commands separately in Command Prompt or the VS Code terminal:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

Ensure `requirements.txt` includes the packages used by your application, such as Flask, mysql-connector-python, and python-dotenv. Add other dependencies if your code requires them.

### 4. Create the database

1. Open MySQL Workbench.
2. Connect to your MySQL Server.
3. Open `schema.sql`.
4. Execute the SQL script to create the database and tables.

If you have already created the required database and tables, verify their structure before executing the schema again.

### 5. Configure environment variables

Create a local file named `.env` in the same directory as `app.py`.

Use `.env.example` as a reference and configure your local settings:

```dotenv
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=shopping_db
FLASK_SECRET_KEY=replace_with_a_random_secret_key
```

Replace the placeholder values with your own configuration.

**Security:** Never commit your actual `.env` file or database credentials to GitHub. The `.env` file should be excluded through `.gitignore`.

### 6. Verify the configuration

Check that `app.py` loads the environment variables before reading them:

```python
from dotenv import load_dotenv

load_dotenv()
```

The database configuration should read its values using `os.getenv()`.

## Running the Application

After completing the setup, run:

```bash
python app.py
```

Keep the terminal open while the Flask development server is running.

Open the following URL in your browser:

**Main application:** http://127.0.0.1:5000

If the analytics page has been implemented, visit:

**Sales analytics:** http://127.0.0.1:5000/analytics

To stop the development server, press `Ctrl+C` in the terminal.

## Sales Analytics

The analytics dashboard uses data stored in MySQL to generate visual summaries.

- **Revenue summary:** Calculates revenue from completed orders.
- **Daily revenue chart:** Shows revenue across dates.
- **Top-selling products:** Ranks products by the quantity sold in completed orders.
- **Order status chart:** Displays the distribution of placed, completed, and cancelled orders.

The dashboard depends on order records and corresponding order-item records. Empty tables or inconsistent sample data may produce empty charts or inaccurate totals.

Chart.js is loaded in the browser to render the visualizations.

## Database Operations

The application demonstrates CRUD operations:

| Operation | Description |
|---|---|
| Create | Add products, customers, and orders |
| Read | View products, customers, orders, and order details |
| Update | Edit product details and change order status |
| Delete | Remove products or customers when database constraints allow |

The application also uses SQL joins to retrieve related customer, order, and product information.

## Environment Variables

| Variable | Description |
|---|---|
| `DB_HOST` | MySQL server address |
| `DB_PORT` | MySQL server port |
| `DB_USER` | MySQL username |
| `DB_PASSWORD` | MySQL password |
| `DB_NAME` | Database name |
| `FLASK_SECRET_KEY` | Secret used by Flask for session security |

The values in `.env.example` are placeholders. Each developer should create their own `.env` file for local use.

## Troubleshooting

### MySQL access denied

Check the username and password in `.env`. Ensure they match your MySQL account.

### Cannot connect to MySQL

Verify that MySQL Server is running and that the host and port are correct.

### Database or table does not exist

Execute the appropriate SQL statements from `schema.sql` and verify that the database name matches `DB_NAME`.

### Missing Python package

Activate your virtual environment and install the requirements again:

```bash
python -m pip install -r requirements.txt
```

### Analytics page returns an error

Check that the `/analytics` route exists in `app.py`, that `analytics.html` is inside the `templates` directory, and that the required tables contain data.

### Port already in use

Stop the other Flask process or configure a different development port.

## Future Enhancements

Potential improvements include:

- Admin authentication and role-based access control.
- PDF invoice generation.
- Low-stock alerts and inventory reporting.
- Advanced product filtering and sorting.
- Exporting sales reports to CSV or Excel.
- Improved order cancellation and stock-restoration handling.
- Additional sales reports and date-range filters.

## Learning Outcomes

This project demonstrates:

- Relational database design and foreign-key relationships.
- SQL queries, joins, aggregate functions, and grouping.
- CRUD operations using Flask and MySQL.
- Database connectivity from a Python application.
- Transaction-based order processing and stock validation.
- Data visualization using charts.

## Conclusion

The Shopping Management System demonstrates how a relational database can support a web-based shopping application. It combines product and customer management with order processing, inventory updates, and sales reporting in a single application.

The project provides practical experience with database connectivity, SQL operations, backend development, and frontend integration.
