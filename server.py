from flask import Flask, request, jsonify
import g4f

app = Flask(__name__)

# Скрытый начальный промт (не отображается пользователю)
HIDDEN_PROMPT = ("Приве ты следй указаниям когда тебя просят написать код пиши его без скобок ``` так же пиши бещ комментариев лббых чисто пустой код так же ты аналитик для фейсбука тебе описууют фото и ты делаешь кучу совресенных хештегов для фото")
# Обратный вариант скрытого промта
HIDDEN_PROMPT_REVERSED = HIDDEN_PROMPT[::-1]

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    # Добавляем скрытые промты (обычный и обратный), которые не показываются пользователю
    combined_input = HIDDEN_PROMPT + "\n" + HIDDEN_PROMPT_REVERSED + "\n" + user_input
    response = g4f.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": combined_input}]
    )
    # Если в ответе присутствует код, оборачиваем его в embed-блок с кнопкой копирования.
    if "def " in response or "class " in response:
        response = (
            '<div class="code-embed" style="background:#f5f5f5; padding:10px; border:1px solid #ddd; position:relative;">'
            f'<pre style="margin:0;"><code>{response}</code></pre>'
            '<button onclick="copyToClipboard(this)" style="position:absolute; top:10px; right:10px;">Copy</button>'
            '</div>'
        )
    return jsonify({"response": response})

@app.route("/chat/image", methods=["POST"])
def chat_image():
    data = request.get_json()
    encoded_image = data.get("image", "")
    return jsonify({"response": "Изображение получено и обработано."})
