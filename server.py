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
    return jsonify({"response": response})

@app.route("/chat/image", methods=["POST"])
def chat_image():
    data = request.get_json()
    # Ожидается получение Base64-кодированного изображения в поле 'image'
    encoded_image = data.get("image", "")
    # Здесь можно добавить логику для обработки изображения (например, сохранить или провести анализ)
    # В данном примере просто возвращаем подтверждение получения изображения.
    return jsonify({"response": "Изображение получено и обработано."})
