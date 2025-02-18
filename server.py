from flask import Flask, request, jsonify
import g4f

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    response = g4f.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}]
    )
    # Если ответ содержит признаки кода, оборачиваем его в embed (code block)
    if "def " in response or "class " in response:
        # можно улучшить определение по необходимости
        response = "```python\n" + response + "\n```"
    return jsonify({"response": response})

@app.route("/chat/image", methods=["POST"])
def chat_image():
    data = request.get_json()
    # Ожидается получение Base64-кодированного изображения в поле 'image'
    encoded_image = data.get("image", "")
    # Для изображений можно возвращать стандартное сообщение или обрабатывать и генерировать текст, если требуется
    # В данном примере возвращаем стандартное сообщение, но можно реализовать OCR или другую обработку
    return jsonify({"response": "Изображение получено и обработано."})
