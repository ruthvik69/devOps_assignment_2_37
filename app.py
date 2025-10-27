from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'ruthvik-secret-key'

# Simulated ticket data
TICKETS = []

@app.route('/')
def index():
    return render_template('index.html', tickets=TICKETS)

@app.route('/book', methods=['POST'])
def book_ticket():
    name = request.form.get('name')
    email = request.form.get('email')
    count = request.form.get('count')
    if not name or not email or not count or int(count) < 1:
        flash('Please provide valid booking details')
        return redirect(url_for('index'))

    ticket = {
        'name': name,
        'email': email,
        'count': int(count)
    }
    TICKETS.append(ticket)
    flash('Ticket successfully booked for {}!'.format(name))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
