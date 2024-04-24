from flask import Flask, request, render_template, redirect, abort
import csv
from datetime import datetime
app = Flask(__name__)

def validate(form_data):
    title = form_data['Title']
    type = form_data['Transaction_Type']
    amount = form_data['Amount']
    date = form_data['Date']
    try:
        amount = float(amount)
    except ValueError:
        abort(500, "Input is not a valid number.")
              
    if type == "expense":
        amount *= -1
    
    try:
        date = datetime.strptime(date, "%m-%d-%Y")
    except ValueError:
        abort(500, "Invalid date format. Please enter the date in MM-DD-YYYY form.")

    return {
        'Title': title,
        'Transaction_Type': type,
        'Amount': amount,
        'Date': date,
    }

def last_line_number():
    line_number = 2
    with open('transaction.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            line_number = reader.line_num

    return line_number

# write the data to the CSV
# return the line number of the new item written to the CSV
def save_data(form_data):
    with open('transaction.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            form_data['Title'],
            form_data['Transaction_Type'], 
            form_data['Amount'],
            form_data['Date']
            ])
        
    return last_line_number()

@app.route('/')
def index():
    items = []  # Initialize an empty list to store dictionaries
    # Open the CSV file in read mode
    with open('transaction.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(row | {'id': reader.line_num})
    # Pass the list of dictionaries to the template
    return render_template('index.html', items=items)

@app.route('/show/<line_number>')
def show(line_number):
    item = {}
    with open('transaction.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(line_number) == reader.line_num:
                item = row

    return render_template('show.html', item=item)

@app.route('/new', methods=['POST','GET'])
def new():
    if request.method == 'POST':
        valid_data = validate(request.form)
        new_id = save_data(valid_data)
        return redirect(f'/show/{new_id}')
    else:
        return render_template('new.html')

if __name__ == '__main__':
    app.run(port=9001) # Start the server listening for requests
          