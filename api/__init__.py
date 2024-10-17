from flask import Flask, jsonify
from api.db.test_db import persons_db

app = Flask(__name__)

@app.route('/test')
def test():
    return jsonify({"mesagge" : "test ok"})