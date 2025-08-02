import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return {"message": os.getenv("APP_MESSAGE", "Default message")}

@app.route('/health')
def health():
    return {"status": "healthy", "env": os.getenv("FLASK_ENV")}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
