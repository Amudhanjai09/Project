from flask import Flask, request, render_template_string
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j Connection Setup
uri = "neo4j://localhost:7687"  # Change to your Neo4j instance URI
username = "neo4j"
password = "your_password"  # Replace with your Neo4j password

driver = GraphDatabase.driver(uri, auth=(username, password))

# Function to insert data into Neo4j
def insert_data(name, regno, department, email, address, gender):
    with driver.session() as session:
        session.run(
            """
            CREATE (s:Student {
                name: $name, 
                regno: $regno, 
                department: $department, 
                email: $email, 
                address: $address, 
                gender: $gender
            })
            """,
            name=name,
            regno=regno,
            department=department,
            email=email,
            address=address,
            gender=gender
        )

# Route to render the form (optional if using HTML file)
@app.route('/')
def form():
    return render_template_string(open("index.html").read())  # Renders the form from the HTML file

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Extract data from the form
    name = request.form['name']
    regno = request.form['regno']
    department = request.form['department']
    email = request.form['email']
    address = request.form['address']
    gender = request.form['gender']

    # Insert data into Neo4j
    insert_data(name, regno, department, email, address, gender)

    # Confirmation page
    return f'''
    <h1>Form Submitted Successfully!</h1>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Reg No:</strong> {regno}</p>
    <p><strong>Department:</strong> {department}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Address:</strong> {address}</p>
    <p><strong>Gender:</strong> {gender}</p>
    <a href="/">Go Back</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)
