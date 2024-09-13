from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///people.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to disable track modifications
db = SQLAlchemy(app)
CORS(app)

# Define the model for the people
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)

# Function to create the database and seed it
def init_db():
    db.create_all()

    # Check if the table is empty, and if so, populate it
    if not Person.query.first():
        people = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 24},
            {"name": "Charlie", "age": 29},
            {"name": "Diana", "age": 35},
            {"name": "Eve", "age": 28},
            {"name": "Frank", "age": 32},
            {"name": "Grace", "age": 26},
            {"name": "Hank", "age": 31},
            {"name": "Ivy", "age": 27},
            {"name": "Jack", "age": 36},
            {"name": "Karen", "age": 34},
            {"name": "Leo", "age": 25},
            {"name": "Mia", "age": 33},
            {"name": "Nick", "age": 22},
            {"name": "Olivia", "age": 29}
        ]
        for person in people:
            new_person = Person(name=person["name"], age=person["age"])
            db.session.add(new_person)
        db.session.commit()


# Route to add a new person
@app.route('/add_person', methods=['POST'])
def add_person():
    data = request.get_json()  # Get the JSON data sent from the client
    name = data.get("name")
    age = data.get("age")
    
    if not name or not age:
        return jsonify({"error": "Missing name or age"}), 400
    
    try:
        # Create a new person object and add it to the database
        new_person = Person(name=name, age=int(age))
        db.session.add(new_person)
        db.session.commit()

        return jsonify({"message": "Person added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for a dynamic page
@app.route('/hello')
def hello():
    # Query the database for all people
    people = Person.query.all()
    # Convert the query result to a list of dictionaries
    people_list = [{"name": person.name, "age": person.age} for person in people]
    return jsonify(people_list)

@app.route('/')
def home():
    return "Hello, welcome to my simple Flask app!"

if __name__ == '__main__':
    # Initialize the database and seed it when the app starts
    with app.app_context():
        init_db()
        
    app.run(debug=True)
