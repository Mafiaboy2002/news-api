from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Root route to avoid 404 on "/"
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the News API!"})

# /news route that serves the news.json content
@app.route('/news')
def get_news():
    with open('news.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
