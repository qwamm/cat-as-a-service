from flask import Flask, send_file, request
from flask_cors import CORS
import requests
import tempfile
import os

app = Flask(__name__)
CORS(app)

@app.route("/download_feed_stat", methods=["GET"])
def download_feed_stat():
    filepath = "/home/icehookies/cat-as-a-service/feed_stat.txt"

    if not os.path.exists(filepath):
        abort(404, decription="File feed_stat.txt not found")

    return send_file(filepath, as_attachment=True, download_name='feed_stat.txt')

@app.route("/download_pet_stat", methods=["GET"])
def download_pet_stat():
    filepath = "/home/icehookies/cat-as-a-service/pet_stat.txt"

    if not os.path.exists(filepath):
        abort(404, decription="File pet_stat.txt not found")

    return send_file(filepath, as_attachment=True, download_name='pet_stat.txt')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)