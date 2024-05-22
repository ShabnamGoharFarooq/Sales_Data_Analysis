# Sales Performance Analysis API

This project is a Flask-based web application that analyzes sales performance data using OpenAI's GPT-3.5-turbo model. The application provides endpoints to analyze individual sales representative performance, team performance, and performance trends over time.

## Features

- **Individual Performance Analysis**: Analyze the performance of a specific sales representative.
- **Team Performance Analysis**: Analyze the overall performance of the sales team.
- **Performance Trends Analysis**: Analyze sales trends over monthly or quarterly periods.

## Prerequisites

- Python 3.7+
- Flask
- Pandas
- OpenAI Python client library
- An OpenAI API key

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/sales-performance-analysis.git
    cd sales-performance-analysis
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your OpenAI API key:**

    - Add your OpenAI API key to an environment variable:

    ```bash
    export OPENAI_API_KEY='your-openai-api-key'
    ```

    On Windows:

    ```bash
    set OPENAI_API_KEY=your-openai-api-key
    ```

## Usage

1. **Start the Flask application:**

    ```bash
    python app.py
    ```

2. **Access the API endpoints:**

    - **Individual Performance Analysis:**

        ```http
        GET /api/rep_performance?file_path=path/to/data.csv&rep_id=1
        ```

    - **Team Performance Analysis:**

        ```http
        GET /api/team_performance?file_path=path/to/data.csv
        ```

    - **Performance Trends Analysis:**

        ```http
        GET /api/performance_trends?file_path=path/to/data.csv&time_period=monthly
        ```

## API Endpoints

### `GET /api/rep_performance`

Analyze the performance of a specific sales representative.

- **Query Parameters:**
  - `file_path` (string): The path to the CSV or JSON file containing sales data.
  - `rep_id` (int): The ID of the sales representative to analyze.

- **Response:**
  - `insights` (string): Analysis of the sales representative's performance.

### `GET /api/team_performance`

Analyze the overall performance of the sales team.

- **Query Parameters:**
  - `file_path` (string): The path to the CSV or JSON file containing sales data.

- **Response:**
  - `insights` (string): Analysis of the team's performance.

### `GET /api/performance_trends`

Analyze sales trends over a specified time period.

- **Query Parameters:**
  - `file_path` (string): The path to the CSV or JSON file containing sales data.
  - `time_period` (string): The time period for trend analysis (`monthly` or `quarterly`).

- **Response:**
  - `insights` (string): Analysis of sales trends.

## Example Data Format

The input data file should be in CSV or JSON format and include the following columns:

- `employee_id` (int)
- `employee_name` (string)
- `lead_taken` (int)
- `tours_booked` (int)
- `applications` (int)
- `revenue_confirmed` (float)
- `dated` (string, date format)

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
