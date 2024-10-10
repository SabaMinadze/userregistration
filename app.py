from flask import Flask, redirect, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "dasdasdas dasdasd"


# Configure the SQLAlchemy part
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    age = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.name} {self.email} {self.age}>'

# Create the database and the database table
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        age = request.form.get("age")
        
        # Create a new user and save to the database
        new_user = User(name=name, email=email, age=age)
        db.session.add(new_user)
        db.session.commit()
        
        # Query all users to display
        users = User.query.all()
        print(users)
        return render_template("index.html", users=users)
    

    # On GET request, just display all users
    users = User.query.all()
    return render_template("index.html", users=users)


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)  # Get the user or 404 if not found
    db.session.delete(user_to_delete)  # Delete the user
    db.session.commit()  # Commit the changes
    flash(f'User {user_to_delete.name} has been deleted.')  # Optional: Add a flash message
    return redirect("/")  # Redirect back to the index page



if __name__ == "__main__":
    app.run(debug=True)