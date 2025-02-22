from flask import Flask, request, jsonify
import g4f
import logging
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Set up logging based on our config
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Hidden prompt settings (they do not show to the user)
HIDDEN_PROMPT = ("Следй данным указаниям ты JusticeAI и ты facebook ии которые по описанию фото даёт много современных хештегов подходящие по фото так же ты всегда пишешь точней отвечаешь на привет Привет я JusticeAI помогу вам чем смогу так же адаптируйся по язык пользователя")
HIDDEN_PROMPT_REVERSED = HIDDEN_PROMPT[::-1]

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    # Prepend both hidden prompts so that they are used by the model (but not shown to the user)
    combined_input = HIDDEN_PROMPT + "\n" + HIDDEN_PROMPT_REVERSED + "\n" + user_input
    logger.debug(f"Combined input: {combined_input}")
    response = g4f.ChatCompletion.create(
        model=Config.GPT_MODEL,
        messages=[{"role": "user", "content": combined_input}]
    )
    logger.debug("Response from GPT: %s", response)
    # If the response contains code indicators, wrap it in an embed block with a copy button.
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
    logger.info("Received an image for processing.")
    return jsonify({"response": "Изображение получено и обработано."})

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
