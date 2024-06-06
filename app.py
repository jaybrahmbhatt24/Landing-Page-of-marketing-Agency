from flask import Flask, request, render_template, redirect, url_for, flash
from wtforms import Form, StringField, TextAreaField, validators # type: ignore
import mysql.connector

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = '953554'

# Define the form class for Contact Us page
class ContactForm(Form):
    name = StringField('Name', [validators.InputRequired()])
    email = StringField('Email', [validators.InputRequired(), validators.Email()])
    message = TextAreaField('Message', [validators.InputRequired()])

# Database connection function
def get_db_connection():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Jay(?24$)',
        database='portfolio'
    )
    return mydb

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/contact_form", methods=['GET', 'POST'])
def contact_form():
    form = ContactForm(request.form)
    
    if request.method == 'POST' and form.validate():
        # Get form data
        name = form.name.data
        email = form.email.data
        message = form.message.data
        
        # Connect to the database
        mydb = get_db_connection()
        cursor = mydb.cursor()
        
        # Insert form data into the database
        query = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
        values = (name, email, message)
        cursor.execute(query, values)
        
        # Commit the transaction and close the database connection
        mydb.commit()
        cursor.close()
        mydb.close()
        
        # Flash a success message
        flash('Message sent successfully!', 'success')

        # Redirect to the main page
        return redirect(url_for('main'))
    
    # Handle GET requests by rendering the contact form template
    return render_template("contact.html", form=form)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
