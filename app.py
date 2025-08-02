import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Check if DB_HOST is available (e.g., in Kubernetes) 
db_host = os.getenv("DB_HOST")

if db_host:
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{db_host}/{os.getenv('DB_NAME')}"
    )
    db = SQLAlchemy(app)
    with app.app_context():
        db.create_all()
else:
    db = None  # Skip DB setup in CI if env vars are missing

@app.route("/health")
def health():
    return {"status": "healthy"}
