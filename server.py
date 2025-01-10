from flask import Flask, render_template, url_for, request, redirect
import csv
import os

app = Flask(__name__)

@app.route("/")
def my_home():
    return render_template("index.html")

@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/index2.html')
        except Exception as e:
            print(f"Error occurred: {e}")
            return 'did not save to database'
    else:
        return 'something went wrong. Try again!'

def write_to_csv(data):
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'database.csv')
        with open(file_path, mode='a', newline='') as database:
            email = data.get("email", "").strip()
            subject = data.get("subject", "").strip()
            message = data.get("message", "").strip()
            name = data.get("name", "").strip()
            if email and subject and message and name:
                csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([email, subject, message, name])
            else:
                print("Missing required fields!")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

if __name__ == "__main__":
    app.run(debug=True)
