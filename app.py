from flask import Flask, render_template, request,session, redirect, url_for, flash
import pymysql
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'your_secret_key'

def sql_connector():
    conn = pymysql.connect(user='root', password='', db='User_authentication_prj_inflask', host='localhost')
    c = conn.cursor()
    return conn, c

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("homepage.html")

        # @app.route('/signup', methods=['GET', 'POST'])
        # def signup():
        #     if request.method == "POST":
        #         Username = request.form['Username']
        #         Password = request.form['Password']
        #         Email = request.form['Email']
        #         Photo = request.files['Photo']

        #         # Check if the 'photos' directory exists, if not, create it
        #         if not os.path.exists('photos'):
        #             os.makedirs('photos')

        #         # Save the photo to the 'photos' directory
        #         photo_path = os.path.join('photos', Photo.filename)
        #         Photo.save(photo_path)

        #         # Connect to MySQL and insert user data
        #         conn, c = sql_connector()
        #         c.execute("INSERT INTO user_data (Username, Password, Email, Photo) VALUES (%s, %s, %s, %s)", (Username, Password, Email, Photo.filename))
        #         conn.commit()
        #         conn.close()
                
        #         flash('User signed up successfully!')
        #         return redirect(url_for('home'))
        #     return render_template('signup.html')

        # @app.route('/login', methods=['GET', 'POST'])
        # def login():
        #     if request.method == 'POST':
        #         Email = request.form['Email']
        #         Password = request.form['Password']

        #         conn, c = sql_connector()
        #         c.execute("SELECT * FROM user_data WHERE Email = %s AND Password = %s", (Email, Password))
        #         user_data = c.fetchone()  # Fetch all data for the user
        #         conn.close()

        #         if user_data:
        #             # Successful login, pass user data to profile page
        #             return render_template('profile.html', user_data=user_data)


        #         else:
        #             # Invalid credentials, show error message
        #             # return "Invalid email or password. "
        #             flash('Invalid email or password. Please try again.', 'error')
        #     return render_template('login.html',)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']

        # Connect to the database and retrieve user data
        conn, c = sql_connector()
        c.execute("SELECT * FROM user_data WHERE Email = %s AND Password = %s", (email, password))
        user_data = c.fetchone()
        conn.close()

        if user_data:
            # Store user data in the session
            session['user_data'] = user_data
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        # Check if the user is logged in
        if 'user_data' in session:
            # Retrieve user data from session
            user_data = session['user_data']
            return render_template('profile.html', user_data=user_data)
        else:
            # If user is not logged in, redirect to login page
            return redirect(url_for('login'))
    else:
        # Handle POST request (if any)
        pass  # Add your logic for handling POST requests here


@app.route('/update', methods=['GET', 'POST']) 
def update():
    # if request.method == 'GET':
    #     Email = request.args.get('Email')
    #     conn, c = sql_connector()
    #     c.execute("SELECT * FROM user_data WHERE Email = %s", (Email,))
    #     user_data = c.fetchone()
    #     conn.close()
    #     return render_template('update.html', user_data=user_data)
    if request.method == 'GET':
        # Check if the user is logged in
        if 'user_data' in session:
            # Retrieve user data from session
            user_data = session['user_data']
            return render_template('update.html', user_data=user_data)
        else:
            # If user is not logged in, redirect to login page
            return redirect(url_for('login'))

    elif request.method == 'POST':

        Username = request.form['Username']
        Password = request.form['Password']
        Email = request.form['Email']
        Photo = request.files['Photo']

        if 'Photo' in request.files:
            Photo = request.files['Photo']
            images_dir = os.path.join('static', 'images')
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)

            # Save the photo to the 'images' directory
            photo_path = os.path.join(images_dir, secure_filename(Photo.filename))
            Photo.save(photo_path)
        else:
            photo_path = None


        conn, c = sql_connector()
        c.execute("UPDATE user_data SET Username = %s, Password = %s, Photo = %s WHERE Email = %s", (Username, Password, Photo.filename, Email,))

    
        conn.commit()
        conn.close()

        print(f"Email: {Email}, Username: {Username}, Password: {Password}, Photo: {Photo.filename}")
        # print(f"Email: {Email}, Username: {Username}, Password: {Password}, ")


        return redirect(url_for('profile'))



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        Username = request.form['Username']
        Password = request.form['Password']
        Email = request.form['Email']
        Photo = request.files['Photo']

        # Ensure the 'images' directory exists in the 'static' folder
        images_dir = os.path.join('static', 'images')
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        # Save the photo to the 'images' directory
        photo_path = os.path.join(images_dir, Photo.filename)
        Photo.save(photo_path)

        # Connect to MySQL and insert user data
        conn, c = sql_connector()
        c.execute("INSERT INTO user_data (Username, Password, Email, Photo) VALUES (%s, %s, %s, %s)",
                  (Username, Password, Email, Photo.filename))
        conn.commit()
        conn.close()

        flash('User signed up successfully!')
        return redirect(url_for('home'))
    return render_template('signup.html')




if __name__ == '__main__':
    app.run(debug=True)

