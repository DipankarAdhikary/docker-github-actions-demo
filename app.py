import os
from flask import Flask, render_template_string
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

    # Define model
    class Message(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        content = db.Column(db.String(200), nullable=False)

        def __repr__(self):
            return f"<Message {self.content}>"

    with app.app_context():
        db.create_all()
        # Seed only if empty
        if not Message.query.first():
            sample = Message(content="Hello from Postgres!")
            db.session.add(sample)
            db.session.commit()
else:
    db = None
    Message = None


@app.route("/health")
def health():
    return {"status": "healthy"}


@app.route("/")
def home():
    if db and Message:
        messages = Message.query.all()
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Flask + Postgres Demo</title>
        </head>
        <body>
            <h1>Messages from Postgres</h1>
            <ul>
            {% for msg in messages %}
                <li>{{ msg.content }}</li>
            {% endfor %}
            </ul>
        </body>
        </html>
        """
        return render_template_string(template, messages=messages)
    else:
        return "<h1>No database connected</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
