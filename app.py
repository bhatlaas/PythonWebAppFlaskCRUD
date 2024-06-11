from flask import Flask, request, render_template, redirect, url_for
import pyodbc
import os
from datetime import datetime

app = Flask(__name__)


# Connection string for SQL Server using Windows Authentication
# conn_str = (
#     'Driver={ODBC Driver 17 for SQL Server};'
#     'Server=DESKTOP-FBLI0GU\\MSSQLSERVER01;'  # Replace with your server name
#     'Database=testWebApp;'                    # Replace with your database name
#     'Trusted_Connection=yes;'
# )

# def get_db_connection():
#     return pyodbc.connect(conn_str)

# Retrieve the connection string from the environment variable
def get_db_connection():
    conn_str = os.getenv('Myconnection')
    print(f"Connection string: {conn_str}")  # Debug print
    if not conn_str:
        raise ValueError("Connection string is not set in environment variables")
    return pyodbc.connect(conn_str)

def insert_site_visit_notice(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Site_Visit_Notice (
            Regional_Office_Id,
            Facility_Number,
            Site_Visit_Date,
            Regulatory_Violation_Citation_Ind,
            Regulatory_Violation_TypeA_Citation_Ind,
            Regulatory_Violation_TypeB_Citation_Ind,
            LPA_Name,
            LPA_Phone_Number,
            Inserted_DateTime,
            Created_By,
            Create_DateTime,
            Updated_By,
            Update_DateTime,
            Program_Code,
            Code_FT
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'CODE1', 'FT1')
    """, data['Regional_Office_Id'], data['Facility_Number'], data['Site_Visit_Date'], 
       data['Regulatory_Violation_Citation_Ind'], data['Regulatory_Violation_TypeA_Citation_Ind'], 
       data['Regulatory_Violation_TypeB_Citation_Ind'], data['LPA_Name'], data['LPA_Phone_Number'],
       datetime.now(), 'Admin', datetime.now(), 'Admin', datetime.now())
    conn.commit()
    conn.close()

def read_site_visit_notice(Facility_Number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Site_Visit_Notice WHERE Facility_Number = ?", Facility_Number)
    result = cursor.fetchone()
    conn.close()
    return result

def update_site_visit_notice(Facility_Number, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Site_Visit_Notice
        SET
            Regional_Office_Id = ?,
            Facility_Number = ?,
            Site_Visit_Date = ?,
            Regulatory_Violation_Citation_Ind = ?,
            Regulatory_Violation_TypeA_Citation_Ind = ?,
            Regulatory_Violation_TypeB_Citation_Ind = ?,
            LPA_Name = ?,
            LPA_Phone_Number = ?,
            Updated_By = 'Admin',
            Update_DateTime = ?
        WHERE Facility_Number = ?
    """, data['Regional_Office_Id'], data['Facility_Number'], data['Site_Visit_Date'],
       data['Regulatory_Violation_Citation_Ind'], data['Regulatory_Violation_TypeA_Citation_Ind'],
       data['Regulatory_Violation_TypeB_Citation_Ind'], data['LPA_Name'], data['LPA_Phone_Number'],
       datetime.now(), Facility_Number)
    conn.commit()
    conn.close()

def delete_site_visit_notice(Facility_Number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Site_Visit_Notice WHERE Facility_Number = ?", Facility_Number)
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def site_visit_notice():
    if request.method == 'POST':
        data = {
            'Regional_Office_Id': request.form['Regional_Office_Id'],
            'Facility_Number': request.form['Facility_Number'],
            'Site_Visit_Date': request.form['Site_Visit_Date'],
            'Regulatory_Violation_Citation_Ind': request.form['Regulatory_Violation_Citation_Ind'],
            'Regulatory_Violation_TypeA_Citation_Ind': request.form['Regulatory_Violation_TypeA_Citation_Ind'],
            'Regulatory_Violation_TypeB_Citation_Ind': request.form['Regulatory_Violation_TypeB_Citation_Ind'],
            'LPA_Name': request.form['LPA_Name'],
            'LPA_Phone_Number': request.form['LPA_Phone_Number']
        }
        insert_site_visit_notice(data)
        return "Form submitted successfully!"
    return render_template('index.html')

@app.route('/read/<int:Facility_Number>')
def read(Facility_Number):
    record = read_site_visit_notice(Facility_Number)
    return render_template('read.html', record=record)

@app.route('/update/<int:Facility_Number>', methods=['GET', 'POST'])
def update(Facility_Number):
    if request.method == 'POST':
        data = {
            'Regional_Office_Id': request.form['Regional_Office_Id'],
            'Facility_Number': request.form['Facility_Number'],
            'Site_Visit_Date': request.form['Site_Visit_Date'],
            'Regulatory_Violation_Citation_Ind': request.form['Regulatory_Violation_Citation_Ind'],
            'Regulatory_Violation_TypeA_Citation_Ind': request.form['Regulatory_Violation_TypeA_Citation_Ind'],
            'Regulatory_Violation_TypeB_Citation_Ind': request.form['Regulatory_Violation_TypeB_Citation_Ind'],
            'LPA_Name': request.form['LPA_Name'],
            'LPA_Phone_Number': request.form['LPA_Phone_Number']
        }
        update_site_visit_notice(Facility_Number, data)
        return redirect(url_for('read', Facility_Number=request.form['Facility_Number']))
    record = read_site_visit_notice(Facility_Number)
    return render_template('update.html', record=record)

@app.route('/delete/<int:Facility_Number>', methods=['GET','POST'])
def delete(Facility_Number):
    delete_site_visit_notice(Facility_Number)
    return redirect(url_for('site_visit_notice'))

if __name__ == '__main__':
    # Use default port 5000 if PORT environment variable is not set
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
