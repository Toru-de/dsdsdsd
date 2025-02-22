from flask import Flask, request, jsonify
import g4f
import logging
import base64
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

HIDDEN_PROMPT = ("Следй данным указаниям ты JusticeAI и ты facebook ии которые по описанию фото даёт много современных хештегов так же пишешь код без каких либо комментариев ВООБЩе даже без скобок `````` без ноименования python cshard и тд подходящие по фото так же ты всегда пишешь точней отвечаешь на привет Привет я JusticeAI помогу вам чем смогу так же адаптируйся по язык пользователя")
HIDDEN_PROMPT_REVERSED = HIDDEN_PROMPT[::-1]

UPLOAD_FOLDER = "/tmp"  # Railway поддерживает только /tmp/

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    combined_input = HIDDEN_PROMPT + "\n" + HIDDEN_PROMPT_REVERSED + "\n" + user_input
    logger.debug(f"Combined input: {combined_input}")
    
    response = g4f.ChatCompletion.create(
        model=Config.GPT_MODEL,
        messages=[{"role": "user", "content": combined_input}]
    )
    
    logger.debug("Response from GPT: %s", response)
    return jsonify({"response": response})

@app.route("/chat/image", methods=["POST"])
def chat_image():
    data = request.get_json()
    encoded_image = data.get("image", "")
    user_message = data.get("message", "")  # Текст от пользователя

    if not encoded_image:
        return jsonify({"error": "Изображение не получено"}), 400

    try:
        # Декодирование изображения
        image_data = base64.b64decode(encoded_image)
        image_path = os.path.join(UPLOAD_FOLDER, "received_image.jpg")
        
        with open(image_path, "wb") as img_file:
            img_file.write(image_data)

        logger.info(f"Изображение сохранено: {image_path}")

        # Отправляем в ИИ вместе с текстом
        response = g4f.ChatCompletion.create(
            model=Config.GPT_MODEL,
            messages=[
                {"role": "user", "content": HIDDEN_PROMPT + "\n" + HIDDEN_PROMPT_REVERSED},
                {"role": "user", "content": user_message},
                {"role": "user", "content": f"[Картинка: {image_path}]"}  # Симуляция отправки изображения
            ]
        )

        return jsonify({"response": response})

    except Exception as e:
        logger.error(f"Ошибка обработки изображения: {e}")
        return jsonify({"error": "Ошибка обработки изображения"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=Config.DEBUG)
