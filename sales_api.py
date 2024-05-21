
from flask import Flask, request, jsonify

app = Flask(__name__)

data = load_data('C:\\Users\\HP\\Desktop\\data.csv')

@app.route('/api/rep_performance', methods=['GET'])
def rep_performance():
    response = {"message": "Representative performance"}
    return jsonify(response)


@app.route('/api/team_performance', methods=['GET'])
def team_performance():
    response = {"message": "Team Performance"}
    return jsonify(response)


@app.route('/api/performance_trends', methods=['GET'])
def performance_trends():
    response = {"message": "Performance Trends"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)


