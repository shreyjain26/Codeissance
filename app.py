from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
import matplotlib.pyplot as plt
import io
import seaborn as sns
import base64
import pandas as pd
import random
from utils import call_gemini_api
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users = {
    'admin@example.com': {'password': 'admin123', 'role': 'Admin'},
    'fieldengineer@example.com': {'password': 'engineer123', 'role': 'Field Engineer'},
    'manager@example.com': {'password': 'manager123', 'role': 'Manager'}
}

rail = pd.read_csv(r"C:\Users\shery\Downloads\Railway_Infra_Final.csv")

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

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html', traffic_data="Traffic Data", weather_data="Weather Data")

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

@app.route('/predictions')
def maintenance_prediction_form():
    return render_template('predictions.html')

# Route to handle prediction logic
@app.route('/predict_maintenance', methods=['POST'])
def predict_maintenance():
    # Get form data
    equipment_type = request.form.get('equipment_type')
    usage_time = int(request.form.get('usage_time'))
    last_maintenance_date = request.form.get('last_maintenance_date')
    failure_history = int(request.form.get('failure_history'))
    environmental_factors = int(request.form.get('environmental_factors'))

    # Simulate a prediction (replace this with real ML model prediction logic)
    maintenance_level = random.choice(['Low', 'Moderate', 'High'])

    # Render the form again and display the prediction
    return render_template('predictions.html', prediction=maintenance_level)

# @app.route("/chatbot", methods=["POST"])
# def chatbot():
#     data = request.get_json()
#     user_message = data.get("message", "")

#     # Example OpenAI GPT-3.5 API call (you can modify this based on your chatbot logic)
#     openai.api_key = "YOUR_API_KEY"

#     response = openai.Completion.create(
#         engine="gpt-3.5-turbo",
#         prompt=f"User: {user_message}\nBot:",
#         max_tokens=150
#     )

#     bot_response = response.choices[0].text.strip()

#     # Send back the bot's response to the frontend
#     return jsonify({"response": bot_response})

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # traffic_data = "Sample traffic data"
    # weather_data = "Sample weather data"
    
    plot_url = None
    response = None

    # If a POST request is made (form submission), generate the selected plot
    if request.method == 'POST':
        plot_type = request.form.get('plot_type')
        plot_url, response = generate_plot(plot_type)  # Generate the plot and get its base64 URL
    
    return render_template('dashboard.html', plot_url=plot_url, response = response)


# @app.route('/generate_plot', methods=['POST'])
def generate_plot(plot_type):
    # plot_type = request.form.get('plot_type')

    # fig, ax = plt.subplots(figsize=(10, 6))
    df = rail

    if plot_type == 'life':
        plt.figure(figsize=(12, 6))
        start_percentage = 0
        # if 
        life_data = df['Life_Left_Percentage'].sort_values()

    # Filter to show 10 at a time
        # filtered_data = life_data[(life_data >= start_percentage) & (life_data < start_percentage + 10)]
        
        sns.barplot(life_data, color='purple', edgecolor='black')
        plt.title(f'Health Life Plot ({start_percentage}-{start_percentage+10}% Life Left)')
        plt.xlabel('Life Left Percentage')
        plt.ylabel('Frequency')
        plt.tight_layout()

    
    if plot_type == "defects":
        plt.figure(figsize=(12, 6))
        sns.barplot(data=rail, x='State', y='Defect_Count', estimator=sum, ci=None)
        plt.title('State-wise Comparison of Defect Counts')
        plt.xlabel('State')
        plt.ylabel('Total Defect Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        # plt.show()

    elif plot_type == 'traffic_infra':
        plt.figure(figsize=(14, 6))
        sns.lineplot(data=rail, x='Date', y='Traffic_Volume', hue='Infrastructure_Type', marker='o')
        plt.title('Traffic Volume Over Time by Infrastructure Type')
        plt.xlabel('TIme')
        plt.ylabel('Traffic Volume')
        plt.xticks([])
        plt.legend(title='Infrastructure Type')
        plt.tight_layout()
        # plt.show()

    elif plot_type == 'traffic_state':
        plt.figure(figsize=(14, 6))
        sns.lineplot(data=rail, x='Date', y='Traffic_Volume', hue='State', marker='o')
        plt.title('Traffic Volume Over Time by Infrastructure Type')
        plt.xlabel('TIme')
        plt.ylabel('Traffic Volume')
        plt.xticks([])
        plt.legend(title='Infrastructure Type')
        plt.tight_layout()
        # plt.show()

    elif plot_type == 'age_dist':
        plt.figure(figsize=(12, 6))
        sns.histplot(data=rail, x='Age', bins=30, kde=True)
        plt.title('Distribution of Age of Infrastructure')
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        plt.tight_layout()
        # plt.show()

    elif plot_type == "maintenance":
        plt.figure(figsize=(12, 6))
        sns.barplot(data=rail, x='State', y='Maintenance_Count', estimator=sum, ci=None)
        plt.title('State-wise Comparison of Maintenance Counts')
        plt.xlabel('State')
        plt.ylabel('Total Maintenance Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        # plt.show()

    elif plot_type == "failures":
        plt.figure(figsize=(12, 6))
        sns.barplot(data=rail, x='State', y='Failure_Count', estimator=sum, ci=None)
        plt.title('State-wise Comparison of Failure Counts')
        plt.xlabel('State')
        plt.ylabel('Total Failure Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        # plt.show()

    # Save plot to a BytesIO object and return it as a response
    # img = io.BytesIO()
    url = 'static/images/plot.png'
    plt.savefig(url)
    response = call_gemini_api("Understand the graph thoroughly and provide relevant inferences. Recommend some actions to be taken. If there are state mentioned, based on the plot data, rcommend which states should be given priority for resource allocation", url)

    return url, response

@app.route('/chatbot', methods=['POST'])
def handle_message():
    data = request.get_json() 
    user_message = data.get('message')
    response_message = call_gemini_api(user_message)
    if response_message:
        return jsonify({'response': response_message})
    return jsonify({'error': 'Invalid data received'}), 400


if __name__ == '__main__':
    app.run(debug=True)
