from flask import Flask, request, jsonify
import pandas as pd
import openai

# Set your OpenAI API key
openai.api_key = 'sk-proj-21ryPMQK6y1we9UbNt3LT3BlbkFJfqLSk6HN41LATwwlZgUv'

def load_data(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.json'):
        return pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format. Please use CSV or JSON.")

def generate_insights(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

def analyze_individual_performance(data, rep_id):
    rep_data = data[data['employee_id'] == rep_id]
    if rep_data.empty:
        return "No data found for the given sales representative."

    prompt = f"Analyze the performance of sales representative with ID {rep_id} based on the following data:\n{rep_data.to_string(index=False, columns=['employee_name', 'lead_taken', 'tours_booked', 'applications', 'revenue_confirmed'])}"
    return generate_insights(prompt)

def analyze_team_performance(data):
    prompt = f"Analyze the performance of the sales team based on the following data:\n{data.to_string(index=False, columns=['employee_name', 'lead_taken', 'tours_booked', 'applications', 'revenue_confirmed'])}"
    return generate_insights(prompt)

def analyze_performance_trends(data, time_period):
    if time_period == 'monthly':
        data['period'] = pd.to_datetime(data['dated']).dt.to_period('M')
    elif time_period == 'quarterly':
        data['period'] = pd.to_datetime(data['dated']).dt.to_period('Q')
    else:
        return "Unsupported time period. Please use 'monthly' or 'quarterly'."

    trends = data.groupby('period').sum()
    prompt = f"Analyze sales trends over the {time_period} period based on the following data:\n{trends.to_string(index=True, columns=['lead_taken', 'tours_booked', 'applications', 'revenue_confirmed'])}"
    return generate_insights(prompt)


app = Flask(__name__)

@app.route('/api/rep_performance', methods=['GET'])
def rep_performance():
    # Load the data dynamically
    data = load_data('C:\\Users\\HP\\Desktop\\data.csv')
    rep_id = request.args.get('rep_id')
    if not rep_id:
        return jsonify({'error': 'rep_id is required'}), 400
    insights = analyze_individual_performance(data, rep_id)
    return jsonify({'insights': insights})

@app.route('/api/team_performance', methods=['GET'])
def team_performance():
    # Load the data dynamically
    data = load_data('C:\\Users\\HP\\Desktop\\data.csv')
    insights = analyze_team_performance(data)
    return jsonify({'insights': insights})

@app.route('/api/performance_trends', methods=['GET'])
def performance_trends():
    # Load the data dynamically
    data = load_data('C:\\Users\\HP\\Desktop\\data.csv')
    time_period = request.args.get('time_period')
    if not time_period:
        return jsonify({'error': 'time_period is required'}), 400
    insights = analyze_performance_trends(data, time_period)
    return jsonify({'insights': insights})

if __name__ == '__main__':
    app.run(debug=True)
