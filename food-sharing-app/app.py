from flask import Flask, render_template, request, redirect
import pymysql
import os
from werkzeug.utils import secure_filename

connection = pymysql.connect(
    host="foodsharingmysql.cixkummayyzb.us-east-1.rds.amazonaws.com",
    user="kajolini",
    password="Food12345",
    database="foodapp"
)

cursor = connection.cursor()

cursor.execute("SELECT * FROM foods")

rows = cursor.fetchall()

for row in rows:
    print(row)

app = Flask(__name__)

food_items = []

@app.route('/')
def home():
    return render_template("index.html")

UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "uploads")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':

        food = request.form['food']
        quantity = request.form['quantity']
        location = request.form['location']

        image = request.files['image']

        filename = secure_filename(image.filename)

        image_path = os.path.join(UPLOAD_FOLDER, filename)

        image.save(image_path)

        cursor.execute(
            "INSERT INTO foods(food_name, quantity, location, image) VALUES (%s,%s,%s,%s)",
            (food, quantity, location, filename)
        )

        connection.commit()

        return redirect('/foods')

    return render_template("upload.html")

@app.route('/foods')
def foods():
    cursor.execute("SELECT * FROM foods")
    foods = cursor.fetchall()
    return render_template("food_list.html", foods=foods)
    
@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM foods WHERE id = %s", (id,))
    connection.commit()
    return redirect('/foods')

if __name__ == "__main__":
    app.run(debug=True)
