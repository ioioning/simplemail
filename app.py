# Імпортуємо бібліотеки Flask для створення веб-сервера
from flask import Flask, request, render_template, jsonify

# Створюємо екземпляр додатку Flask
app = Flask(__name__)

# Це словник, який зберігатиме всі повідомлення для кожної адреси
inbox = {}  # Формат: { 'email@site.com': [ { 'from': ..., 'message': ... }, ... ] }

# Головна сторінка — показує HTML інтерфейс
@app.route("/")
def index():
    return render_template("index.html")  # Повертаємо HTML-файл

# API для надсилання листа
@app.route("/send", methods=["POST"])
def send_email():
    data = request.json  # Отримуємо JSON-дані з запиту
    to = data["to"].strip().lower()      # Кому
    sender = data["from"].strip().lower()  # Від кого
    message = data["message"].strip()    # Повідомлення

    # Додаємо лист у список одержувача
    inbox.setdefault(to, []).append({ "from": sender, "message": message })
    return jsonify({ "status": "ok" })  # Повертаємо успішну відповідь

# API для перегляду вхідних повідомлень
@app.route("/inbox/<email>")
def get_inbox(email):
    email = email.strip().lower()  # Нормалізуємо адресу
    messages = inbox.get(email, [])  # Отримуємо повідомлення
    return jsonify(messages)  # Повертаємо їх як JSON

if __name__ == "__main__":
    app.run(debug=True)

