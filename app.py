from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy  # Імпортуємо SQLAlchemy
import os

app = Flask(__name__)

# Налаштування SQLite — створює файл бази у цій же папці
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Створюємо обʼєкт БД

# Модель таблиці "messages"
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Унікальний ID
    sender = db.Column(db.String(120), nullable=False)  # Від кого
    recipient = db.Column(db.String(120), nullable=False)  # Кому
    content = db.Column(db.Text, nullable=False)  # Повідомлення

# Головна сторінка
@app.route("/")
def index():
    return render_template("index.html")

# Надсилання листа
@app.route("/send", methods=["POST"])
def send_email():
    data = request.json
    to = data["to"].strip().lower()
    sender = data["from"].strip().lower()
    message = data["message"].strip()

    # Створюємо обʼєкт повідомлення
    new_msg = Message(sender=sender, recipient=to, content=message)
    db.session.add(new_msg)  # Додаємо в сесію
    db.session.commit()      # Зберігаємо в базу

    return jsonify({ "status": "ok" })

# Отримати вхідні для конкретної адреси
@app.route("/inbox/<email>")
def get_inbox(email):
    email = email.strip().lower()
    messages = Message.query.filter_by(recipient=email).all()

    # Перетворюємо на словники
    result = []
    for m in messages:
        result.append({ "from": m.sender, "message": m.content })

    return jsonify(result)

if __name__ == "__main__":
    if not os.path.exists("emails.db"):
        with app.app_context():
            db.create_all()
    app.run(debug=True)

