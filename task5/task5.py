from flask import Flask, request, jsonify
from db import init_db, add_url, get_urls

app = Flask(__name__)

@app.route('/urls/', methods=['POST'])
def create_url():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    if add_url(url):
        return jsonify({"message": "URL added", "url": url}), 201
    return jsonify({"error": "URL already exists"}), 400

@app.route('/urls/', methods=['GET'])
def get_all_urls():
    urls = get_urls()
    return jsonify(urls)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)