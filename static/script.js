// Ця функція надсилає повідомлення
function sendMessage() {
  // Беремо значення з полів
  const from = document.getElementById("yourEmail").value;
  const to = document.getElementById("toEmail").value;
  const message = document.getElementById("message").value;

  // Відправляємо POST-запит на сервер
  fetch("/send", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ from, to, message })  // Передаємо JSON
  }).then(res => res.json()).then(data => {
    alert("Повідомлення надіслано!");
    document.getElementById("message").value = "";  // Очищуємо поле
  });
}

// Ця функція завантажує вхідні листи
function loadInbox() {
  const email = document.getElementById("yourEmail").value;

  // GET-запит на сервер
  fetch(`/inbox/${email}`)
    .then(res => res.json())
    .then(messages => {
      const inboxDiv = document.getElementById("inbox");
      inboxDiv.innerHTML = "";  // Очищаємо старі повідомлення

      // Виводимо кожне повідомлення
      messages.forEach(msg => {
        const el = document.createElement("div");
        el.innerHTML = `<b>Від:</b> ${msg.from}<br>${msg.message}<hr>`;
        inboxDiv.appendChild(el);
      });
    });
}

