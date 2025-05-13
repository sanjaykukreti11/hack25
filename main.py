import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from app import generate_custom_prompt

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes and origins

file_prompt_map = {
    "first_screen": "/Users/sanjaykukreti/Desktop/zeotap_repo/Hack2025/prompts/ops_ui.txt",
    "second_screen": "/Users/sanjaykukreti/Desktop/zeotap_repo/Hack2025/prompts/ops_ui_2.txt",
    "third_screen": "/Users/sanjaykukreti/Desktop/zeotap_repo/Hack2025/prompts/ops_ui_3.txt"
}

@app.route("/")
def home():
    return "Flask API is live"

@app.route("/ops_ui_config", methods=["POST"])
def create_item():
    data = request.json
    file_key = data.get("name")

    if file_key not in file_prompt_map:
        return jsonify({"error": f"Unknown file_name '{file_key}'"}), 400

    file_name = file_prompt_map[file_key]
    generated = generate_custom_prompt(file_name)

    return jsonify({"received_item": json.loads(generated)})

if __name__ == "__main__":
    app.run(debug=True)
