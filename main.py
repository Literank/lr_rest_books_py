from flask import Flask, jsonify

app = Flask(__name__)

# Define a health endpoint handler, use `/health` or `/`
@app.route('/')
def health():
    # Return a simple response indicating the server is healthy
    return jsonify({"status": "ok"})

