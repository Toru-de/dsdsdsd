from flask import Flask, request, jsonify
import g4f

app = Flask(__name__)

# Этот скрытый начальный промт не показывается пользователю,
# но добавляется к каждому сообщению перед отправкой в модель.
HIDDEN_PROMPT = ("Приве ты следй указаниям когда тебя просят написать код пиши его без скобок "
                 "``` так же пиши бещ комментариев лббых чисто пустой код так же ты аналитик для фейсбука "
                 "тебе описууют фото и ты делаешь кучу совресенных хештегов для фото")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    # Соединяем скрытый промт с сообщением пользователя
    combined_input = HIDDEN_PROMPT + "\n" + user_input
    response = g4f.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": combined_input}]
    )
    # Возвращаем только ответ от модели, скрытый промт не показывается
    return jsonify({"response": response})

@app.route("/chat/image", methods=["POST"])
def chat_image():
    data = request.get_json()
    encoded_image = data.get("image", "")
    return jsonify({"response": "Изображение получено и обработано."})
