
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Create tables in the database 
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        if User.query.filter_by(username=username).first():
            return "Username already exists. Please choose a different username."

        # Store user data in the database
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return f"User {username} signed up successfully!"

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check login credentials
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            return f"Welcome, {username}!"
        else:
            return "Invalid username or password. Please try again."

    return render_template('login.html')


@app.route('/reset_password')
def reset_password():
    return "Reset Password Page"


@app.route('/rename_username')
def rename_username():
    return "Rename Username Page"


if __name__ == '__main__':
    app.run(debug=True)