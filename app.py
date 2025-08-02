import os
from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_host = os.getenv("DB_HOST")
if db_host:
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{db_host}/{os.getenv('DB_NAME')}"
    )
    db = SQLAlchemy(app)

    class Note(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        content = db.Column(db.String(200), nullable=False)

    with app.app_context():
        db.create_all()
else:
    db = None
    Note = None

@app.route("/health")
def health():
    return {"status": "healthy"}

@app.route("/", methods=["GET", "POST"])
def home():
    if not db:
        return "Database not configured"

    if request.method == "POST":
        content = request.form.get("content")
        if content:
            new_note = Note(content=content)
            db.session.add(new_note)
            db.session.commit()

    notes = Note.query.all()
    return render_template_string('''
        <h2>My Notes</h2>
        <form method="POST">
            <input type="text" name="content" placeholder="Write a note" required>
            <button type="submit">Add</button>
        </form>
        <ul>
            {% for note in notes %}
              <li>{{ note.content }}</li>
            {% endfor %}
        </ul>
    ''', notes=notes)
