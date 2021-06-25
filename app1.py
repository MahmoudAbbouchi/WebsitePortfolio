# Created by Mahmoud Abbouchi
# Testing out flask for website framework development
from flask import Flask, render_template, redirect, url_for, request
import sqlite3
# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)
sqlconnection = sqlite3.connect("names.db")
cursor = sqlconnection.cursor()
sql_command = """
CREATE TABLE IF NOT EXISTS names (
fname VARCHAR(20));"""
cursor.execute(sql_command)
# Flask route decorators map / and /hello to the hello function.
# To add other resources, create functions that generate the page contents
# and add decorators to define the appropriate resource locators for them.

@app.route('/')
def mainpage():
    #This is the index page
    return render_template('mainpage.html')

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    # Regenerate sql connection
    sqlconnection = sqlite3.connect("names.db")
    cursor = sqlconnection.cursor()
    # Render the page
    if request.method == 'POST':
        new_name = request.form['name']
        cursor.execute("SELECT fname FROM names WHERE fname=?", [new_name])
        res = cursor.fetchone() 
        if res:
            return ("Name: " + new_name + " Already in database.\n")
        else:
            sql_command = "INSERT INTO names (fname) VALUES ('"+ new_name +"');"
            print(sql_command)
            cursor.execute(sql_command)
            sqlconnection.commit()
            return ("Adding new name " + new_name)
    else:
        return "Hello Python!"

@app.route('/bye')
def bye():
    # Render the page
    return "Exit Page."

if __name__ == '__main__':
    # Run the app server on localhost:131773
    app.run('localhost', 420)
    