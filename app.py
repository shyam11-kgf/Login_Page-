from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

FILE_NAME = "users.txt"


# Function to save user data into file
def save_user(username, password):
    with open(FILE_NAME, "a") as file:
        file.write(f"{username},{password}\n")


# Function to check login details
def check_user(username, password):
    try:
        with open(FILE_NAME, "r") as file:
            users = file.readlines()
            for user in users:
                stored_username, stored_password = user.strip().split(",")
                if stored_username == username and stored_password == password:
                    return True
    except FileNotFoundError:
        return False
    return False


# Home route
@app.route("/")
def home():
    return redirect(url_for("login"))


# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if username already exists
        try:
            with open(FILE_NAME, "r") as file:
                users = file.readlines()
                for user in users:
                    stored_username, _ = user.strip().split(",")
                    if stored_username == username:
                        message = "Username already exists!"
                        return render_template("register.html", message=message)
        except FileNotFoundError:
            pass

        save_user(username, password)
        message = "Registration successful! Now login."
        return render_template("register.html", message=message)

    return render_template("register.html", message=message)


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_user(username, password):
            message = "Login successful!"
        else:
            message = "Invalid username or password!"

    return render_template("login.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)