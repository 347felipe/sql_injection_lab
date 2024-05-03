import sqlite3
from flask import Flask, render_template, url_for, request, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
show_login_error = False

def create_table():
    sqliteConnection = sqlite3.connect('sql.db')
    cursor = sqliteConnection.cursor()
    
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS login
                          (username TEXT PRIMARY KEY NOT NULL,
                           password TEXT NOT NULL)''')
        sqliteConnection.commit()
        
        cursor.execute("INSERT OR IGNORE INTO login (username, password) VALUES (?, ?)", ('felipe', '1234'))
        cursor.execute("INSERT OR IGNORE INTO login (username, password) VALUES (?, ?)", ('felipe', 'felipe123'))
        sqliteConnection.commit()
        
    except sqlite3.Error as error:
        print("Error while creating a sqlite table:", error)
    finally:
        cursor.close()
        sqliteConnection.close()

create_table()

@app.route("/", methods=["GET"])
def dnm():
    if show_login_error == True:
        return render_template('index.html',response='wrong user or pass :(')
    else:
        return render_template('index.html',response='')
    

@app.route("/home", methods=["GET"])
def home():
    return render_template('home.html')



@app.route("/login", methods=["POST"])
def UserLogin():
    global show_login_error
    sqliteConnection = sqlite3.connect('sql.db')
    cursor = sqliteConnection.cursor()
    mydata = request.json

    username = mydata["username"]
    input_pass = mydata["password"]
    
    query = f"SELECT * FROM login WHERE username = '{username}' AND password = '{input_pass}'"
    
    print(query)
    cursor.execute(query)

    result = cursor.fetchall()
    if result:
        show_login_error = False
        cursor.close()
        sqliteConnection.close()
        return redirect(url_for("home"))
    else:
        cursor.close()
        sqliteConnection.close()
        show_login_error = True
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)