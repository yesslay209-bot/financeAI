from flask import Flask, render_template, request, jsonify
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
   - <strong> for headings (e.g., 'Simple Advice', 'Debt Check')
   - <em> for key numbers, amounts, or important terms
   - <br> for line breaks and spacing


BEHAVIOR RULES:
- Base advice on the user's actual spending habits and situation.
- Keep explanations practical, gentle, and easy to follow.
- Focus on budgeting, saving, spending habits, and debt patterns.


MENU RULES:
- When the user says what they need help with (ex: "budgeting", "saving", "debt"):
   - Respond with a short, tailored 3-option menu.
   - Keep the menu simple and relevant.
Example:
User: "budgeting"
Menu
1) Discuss Goals
2) Review Budget
3) Explore Other Options


FINAL ANSWER FORMAT:
- After the user chooses a menu option, ALWAYS reply using this format:


<strong>Answer:</strong> <subject><br><br>


<strong>🌟 Simple Advice</strong><br>
<description in short, clear sentences, <em>highlighting amounts or important terms</em>><br><br>


<strong>🧩 What’s Happening</strong><br>
<simple breakdown of the user’s financial situation><br><br>


<strong>💳 Debt Check</strong><br>
<debt notes or reassurance, <em>highlight key numbers</em>><br><br>


<strong>💰 Easy Saving Plan</strong><br>
<small, realistic steps the user can try today, <em>highlight amounts</em>><br><br>
------------------------------------------------

"""

chat_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

# -------------------------
# PAGES
# -------------------------

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/chat")
def chat_page():
    return render_template("index.html")

@app.route("/finance101")
def finance_101():
    return render_template("finance101.html")

# -------------------------
# API ROUTES
# -------------------------

@app.route("/start_chat", methods=["POST"])
def start_chat():
    data = request.json
    bio = "\n".join(data.values())

    chat_history.append({"role": "user", "content": bio})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history
    )

    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})

@app.route("/send_message", methods=["POST"])
def send_message():
    msg = request.json.get("message")

    chat_history.append({"role": "user", "content": msg})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history
    )

    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})

@app.route("/clear", methods=["POST"])
def clear():
    global chat_history
    chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    return jsonify({"status": "cleared"})

# -------------------------
# ARTICLE PAGES
# -------------------------

@app.route("/article/budgeting")
def budgeting_article():
    return render_template("articles/budgeting.html")

@app.route("/article/debt")
def debt_article():
    return render_template("articles/debt.html")

@app.route("/article/saving")
def saving_article():
    return render_template("articles/saving.html")

@app.route("/article/bills")
def bills_article():
    return render_template("articles/bills.html")

# -------------------------
# RUN
# -------------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)