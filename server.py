from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
from datetime import datetime
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector(app,'emails')

@app.route('/')
def index():
    myEmails = mysql.query_db("SELECT * FROM tblemails")
    print myEmails
    return render_template('index.html', all_emails=myEmails)

# Insert into database starting with the root route, then the index from root sends us to this route.
@app.route('/addEmails', methods=['POST'])
def create():
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query.
    # We'll then create a dictionary of data from the POST data received.
    data = {
                'email': request.form['email']
            }
    if not EMAIL_REGEX.match(request.form['email']):
        flash(u"Invalid Email Address!",'flashErrorMessages')
        return redirect('/')
    else:
        flash(u"The Email you entered("+request.form['email']+") is a valid email address!",'flashNoErrorMessages')
        #message = "The Email you entered "+ request.form['email'] + ") is a valid email address!"
        # flash(u"The Email you entered (",'flashNoErrorMessages')
        # flash(request.form['email'])
        # flash(u") is a valid email address!",'flashNoErrorMessages')
        query = "INSERT INTO tblemails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        # Run query, with dictionary values injected into the query.
        mysql.query_db(query, data)
        return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
    print '************************'
    print request.form['id']
    query = "DELETE FROM tblemails where id = :id"
    data = {'id': request.form['id']}
    mysql.query_db(query, data)
    return redirect('/')



app.run(debug=True)
