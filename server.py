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
        response = "python\n" + response + "\n"
    return jsonify({"response": response})

@app.route("/chat/image", methods=["POST"])
def chat_image():
    data = request.get_json()
    encoded_image = data.get("image", "")
    return jsonify({"response": "Изображение получено и обработано."})
