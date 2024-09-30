from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users = {
    'admin@example.com': {'password': 'admin123', 'role': 'Admin'},
    'fieldengineer@example.com': {'password': 'engineer123', 'role': 'Field Engineer'},
    'manager@example.com': {'password': 'manager123', 'role': 'Manager'}
}

@app.route('/')
def home():
    if 'email' in session:
        role = session['role']
        return render_template('home.html', role=role)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        if email in users:
            flash('Email already registered!', 'danger')
        else:
            users[email] = {'password': password, 'role': role}
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and users[email]['password'] == password:
            session['email'] = email
            session['role'] = users[email]['role']
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', traffic_data="Traffic Data", weather_data="Weather Data")

@app.route('/alerts')
def alerts():
    alerts = ["Roadwork on Highway 1", "Heavy rain expected", "Equipment maintenance needed"]
    return render_template('alerts.html', alerts=alerts)

@app.route('/map')
def map_display():
    return render_template('map.html')

@app.route('/resource-scheduling', methods=['GET', 'POST'])
def resource_scheduling():
    if request.method == 'POST':
        resources = request.form['resources']
        budget = request.form['budget']
        flash(f"Schedule submitted!\nResources: {resources}\nBudget: {budget}", 'success')
        return redirect(url_for('resource_scheduling'))
    return render_template('resource-scheduling.html')

if __name__ == '__main__':
    app.run(debug=True)
