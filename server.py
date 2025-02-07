from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Load job domains from headings.json
def load_job_domains():
    try:
        with open("jobs_domain.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

job_domains = load_job_domains()

# Load raw user data from data.json
def load_raw_data():
    try:
        with open("input_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}

# Save processed data to processed_data.json
def save_processed_data(data):
    with open("processed_data.json", "w") as file:
        json.dump(data, file, indent=4)

# Load processed data
def load_processed_data():
    try:
        with open("processed_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}

# Calculate age from date_of_birth
def calculate_age(dob):
    birth_date = datetime.strptime(dob, "%Y-%m-%d")
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

# Classify salary status
def classify_salary(salary):
    if salary > 150000:
        return "high"
    elif salary > 100000:
        return "normal"
    else:
        return "low"

# Calculate experience assuming career starts at 22
def calculate_experience(age):
    years_experience = max(0, age - 22)
    if years_experience < 3:
        return "Junior"
    elif years_experience <= 7:
        return "Mid"
    else:
        return "Senior"

# Determine job domain
def get_job_domain(job_title):
    return job_domains.get(job_title, "Unknown")

# Process user data
def process_user_data(user):
    age = calculate_age(user["date_of_birth"])
    salary_status = classify_salary(user["job"]["salary"])
    experience = calculate_experience(age)
    job_domain = get_job_domain(user["job"]["title"])

    return {
        **user,
        "age": age,
        "status": salary_status,
        "experience": experience,
        "job_domain": job_domain
    }

# API Endpoints
@app.route("/fetch-data", methods=["GET"])
def fetch_data():
    data = load_raw_data()
    return jsonify(data)

@app.route("/process-data", methods=["POST"])
def process_data():
    data = load_raw_data()
    processed_users = [process_user_data(user) for user in data["users"]]

    processed_data = {"users": processed_users}
    save_processed_data(processed_data)
    
    return jsonify(processed_data)

@app.route("/get-processed-data", methods=["GET"])
def get_processed_data():
    data = load_processed_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True,port="2000")
