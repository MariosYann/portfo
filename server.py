from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

@app.route("/")
def my_home():
    return render_template("index.html")

@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            print(f"Form data received: {data}")  # Log the received data for debugging
            write_to_csv(data)
            return redirect('/index2.html')  # Redirect to another page after successful form submission
        except Exception as e:
            print(f"Error occurred: {e}")
            return 'did not save to database'
    else:
        return 'something went wrong. Try again!'

def write_to_csv(data):
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'database.csv')
        print(f"File path: {file_path}")  # Log the file path
        
        email = data.get("email", "").strip()
        subject = data.get("subject", "").strip()
        message = data.get("message", "").strip()
        name = data.get("name", "").strip()

        # Ensure all required fields are filled
        if not email or not subject or not message or not name:
            print("Error: One or more fields are empty.")  # Log if any required field is missing
            return

        # Open the CSV file in append mode and write the data
        with open(file_path, mode='a', newline='') as database:
            csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([email, subject, message, name])
            print("Data successfully written to CSV.")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

if __name__ == "__main__":
    app.run(debug=True)

