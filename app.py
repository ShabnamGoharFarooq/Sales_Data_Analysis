from flask import Flask, request, jsonify
import pandas as pd
from openai import OpenAI
import os

# Set your OpenAI API key
api_key = os.getenv("OPENAI_API_KEY", default='sk-proj-PKRSgoCdgmHQ8YXqVzLyT3BlbkFJlZEN8ShL9day42Q9n2pI')

def load_data(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.json'):
        return pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format. Please use CSV or JSON.")

def generate_insights(prompt):
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # Correctly access the response content
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return str(e)

def analyze_individual_performance(data, rep_id):
    rep_data = data[data['employee_id'] == int(rep_id)]
    if rep_data.empty:
        return "No data found for the given sales representative."

    # Limiting the data to fit the token limit
    rep_data_summary = rep_data[['employee_name', 'lead_taken', 'tours_booked', 'applications', 'revenue_confirmed']].head(10).to_string(index=False)
    prompt = f"Analyze the performance of sales representative with ID {rep_id} based on the following data:\n{rep_data_summary}"
    return generate_insights(prompt)

def analyze_team_performance(data):
    # Limiting the data to fit the token limit
    data_summary = data[['employee_name', 'lead_taken', 'tours_booked', 'applications', 'revenue_confirmed']].head(10).to_string(index=False)
    prompt = f"Analyze the performance of the sales team based on the following data:\n{data_summary}"
    return generate_insights(prompt)

def analyze_performance_trends(data, time_period):
    data['dated'] = pd.to_datetime(data['dated'], errors='coerce')
    if time_period == 'monthly':
        data['period'] = data['dated'].dt.to_period('M')
    elif time_period == 'quarterly':
        data['period'] = data['dated'].dt.to_period('Q')
    else:
        return "Unsupported time period. Please use 'monthly' or 'quarterly'."

    numerical_columns = ['lead_taken', 'tours_booked', 'applications', 'revenue_confirmed']
    trends = data.groupby('period')[numerical_columns].sum()

    # Limiting the data to fit the token limit
    trends_summary = trends.head(10).to_string(index=True, columns=numerical_columns)
    prompt = f"Analyze sales trends over the {time_period} period based on the following data:\n{trends_summary}"
    return generate_insights(prompt)

app = Flask(__name__)

@app.route('/api/rep_performance', methods=['GET'])
def rep_performance():
    try:
        file_path = request.args.get('file_path', 'C:\\Users\\HP\\Desktop\\data.csv')
        data = load_data(file_path)
        rep_id = request.args.get('rep_id')
        if not rep_id:
            return jsonify({'error': 'rep_id is required'}), 400

        insights = analyze_individual_performance(data, rep_id)
        return jsonify({'insights': insights})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/team_performance', methods=['GET'])
def team_performance():
    try:
        file_path = request.args.get('file_path', 'C:\\Users\\HP\\Desktop\\data.csv')
        data = load_data(file_path)
        insights = analyze_team_performance(data)
        return jsonify({'insights': insights})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance_trends', methods=['GET'])
def performance_trends():
    try:
        file_path = request.args.get('file_path', 'C:\\Users\\HP\\Desktop\\data.csv')
        data = load_data(file_path)
        time_period = request.args.get('time_period')
        if not time_period:
            return jsonify({'error': 'time_period is required'}), 400

        insights = analyze_performance_trends(data, time_period)
        return jsonify({'insights': insights})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
