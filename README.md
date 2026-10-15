# Shopping Management System

A student-friendly DBMS project using Flask, HTML/CSS/JavaScript, and MySQL.

## Features
- Dashboard with product, customer, order, and revenue totals
- Add, edit, search, and delete products
- Add and list customers
- Place orders with multiple products
- Stock validation and automatic stock reduction
- View order details and update order status

## Requirements
- Python 3.10 or newer
- MySQL Server and MySQL Workbench

## Setup on Windows

1. Extract this ZIP file.
2. Open Command Prompt in the extracted `shopping_management_system` folder.
3. Create and activate a virtual environment:

   ```bat
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install Python packages:

   ```bat
   pip install -r requirements.txt
   ```

5. Open `schema.sql` in MySQL Workbench and execute it. If you already created the same database and tables, you can skip this step.
6. Set your MySQL password in the current Command Prompt. Replace `YOUR_MYSQL_PASSWORD` with the password you use in MySQL Workbench:

   ```bat
   set DB_PASSWORD=YOUR_MYSQL_PASSWORD
   ```

   If your MySQL root account has no password, run `set DB_PASSWORD=` instead.
7. Start the website:

   ```bat
   python app.py
   ```

8. Open this address in your browser: http://127.0.0.1:5000

Keep the Command Prompt window open while using the website. Press `Ctrl+C` in that window to stop the server.

## Database configuration
Defaults are `127.0.0.1:3306`, user `root`, database `shopping_db`. You can set `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME` as environment variables if your MySQL configuration differs.

## Troubleshooting
- If `Access denied for user 'root'` appears, check the `DB_PASSWORD` value.
- If `Can't connect to MySQL server` appears, make sure MySQL Server is running.
- If a port is already in use, stop the other Flask process or change the port in `app.run`.
