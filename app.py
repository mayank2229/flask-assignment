from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import os

app = Flask(__name__)

client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017/"))
db = client["tododb"]
collection = db["todos"]

data = {
    "message": "Hello from Flask API",
    "status": "success",
    "version": "1.0"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api")
def api():
    return jsonify(data)

@app.route("/todo")
def todo():
    return render_template("todo.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo():
    item_data = request.json
    item_name = item_data.get("itemName")
    item_description = item_data.get("itemDescription")
    if not item_name or not item_description:
        return jsonify({"error": "Required fields missing"}), 400
    collection.insert_one({
        "itemName": item_name,
        "itemDescription": item_description,
        "itemId": item_data.get("itemId", ""),
        "itemUuid": item_data.get("itemUuid", ""),
        "itemHash": item_data.get("itemHash", "")
    })
    return jsonify({"message": "Todo item submitted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)