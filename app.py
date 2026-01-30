from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# System prompt
SYSTEM_PROMPT = """
You are a personal finance assistant. Your job is to give clear, accurate, and beginner-friendly advice about budgeting, saving, debt control, and healthy money habits.

STYLE RULES:
- Explain concepts simply, like teaching a young learner, but NEVER sound childish.
- Keep answers short, clean, and friendly.
- Use a supportive, non-judgmental tone.
- Avoid investment advice, legal guidance, or anything requiring a professional license.
- Do not invent numbers or details the user did not provide.
- Always format output in HTML-friendly style using:
    - <strong> for headings
    - <em> for key numbers or terms
    - <br> for spacing
"""

chat_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/chat", methods=["GET"])
def home():
    return render_template("index.html")


# ✅ NEW ROUTE — Finance 101 page
@app.route("/finance101")
def finance_101():
    return render_template("finance101.html")


@app.route("/start_chat", methods=["POST"])
def start_chat():
    data = request.json
    u1 = data.get("u1", "")
    u2 = data.get("u2", "")
    u3 = data.get("u3", "")
    u4 = data.get("u4", "")
    u5 = data.get("u5", "")

    user_bio = f"{u1}\n{u2}\n{u3}\n{u4}\n{u5}"
    chat_history.append({"role": "user", "content": user_bio})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history
    )

    assistant_reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": assistant_reply})

    return jsonify({"reply": assistant_reply})


@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    user_msg = data.get("message", "")
    chat_history.append({"role": "user", "content": user_msg})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history
    )

    assistant_reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": assistant_reply})

    return jsonify({"reply": assistant_reply})


@app.route("/clear", methods=["POST"])
def clear():
    global chat_history
    chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
