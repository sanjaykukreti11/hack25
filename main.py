import json
import random

from flask import Flask, request, jsonify
from flask_cors import CORS
from app1 import generate_custom_prompt
from chat import query_gemini_with_prompt

from models.test_cred import test_connection

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes and origins

file_prompt_map = {
    "first_screen": "ops_ui.txt",
    "second_screen": "ops_ui_2.txt",
    "third_screen": "ops_ui_3.txt"
}

@app.route("/")
def home():
    return "Flask API is live"

@app.route('/getting_query', methods=['POST'])
def get_query():
    data = request.get_json()
    prompt = data.get("prompt")
    query = data.get("query")
    type_ = data.get("type")  # Avoid shadowing built-in 'type'
    print(prompt)
    if not query:
        return jsonify({"error": "No query provided"}), 400

    if type_ in ("Integrate", "Test"):
        with open("./prompts/channel_info1.txt", "w") as f:
            f.write(prompt + "\n")
        return jsonify({"message": f"Query saved for type '{type_}'"}), 200
    else:
        return jsonify(query_gemini_with_prompt(prompt,query)), 200


@app.route("/ops_ui_config", methods=["POST"])
def create_item():

    data = request.json
    file_key = data.get("name")
    intId = data.get("intId", "")
    actionId = data.get("actionId", "")

    if intId:
        intId = f"intPartnerId = {intId}"
    else :
        random_id = random.randint(10**9, 10**10 - 1)
        intId = f"intPartnerId = {random_id}"
    if actionId:
        actionId = f"actionId = {actionId}"

    if file_key not in file_prompt_map:
        return jsonify({"error": f"Unknown file_name '{file_key}'"}), 400

    file_name = file_prompt_map[file_key]
    generated = generate_custom_prompt(file_name, intId, actionId)

    return jsonify({"received_item": json.loads(generated)})


@app.route("/ath", methods=["POST"])
def get_code():
    data = request.get_json()  # or request.json
    query = data.get("query")
    with open("./prompts/channel_info2.txt", "r") as f:
        text = f.read()

    res = test_connection(query, text)

    return res

if __name__ == "__main__":
    app.run(debug=True)