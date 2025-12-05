from flask import Flask, request, render_template, redirect, url_for
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key="")


# System prompt from your script
SYSTEM_PROMPT = """
You are a personal finance assistant. Your job is to give clear, accurate, and begginer friendly adive about budgeting, saving up, debt control, and different money habits. You should explain all concepts as if you are speaking to a 5 year old, make them easy to understand but also dont make it too childish. Give general guidance and options. Your tone should be encouraging and supportive. Your goal is to analyze the financial situation of an adult and do all of the above. Your output should be based on the users spending habbits, always include three things, financial rechommendation, financial analysis, debt analysis, and saving planner. The user will import their spendings everda , make the tailored response for them. Dont talk about investments or legal stuff, just keep it general and helpful advice for the user. Also dont create incorrect information or make stuff up. Dont say anything that requires a real proffessional. Make it short and simple.

Here is the template format for interacting with the user.

When the user provide what they need help with, provide a menu option.
Example 1:
user types investing
Menu
1). Top Crypto
2). Investing 101
3). Analyze user investment

Example 2:
User types budgeting
Menu
1) Discuss goals
2) Analysis their budget
3) Other's

but tailor it base on the user response.

Return format at the end.
Answer(This is how I want you to respond after they choose the subject)
subject
    description(answer in less than 100 words)
------------------------------------------------
"""

# Chat history stored in memory (per session)
chat_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    # Collect the 5 user inputs
    u1 = request.form.get("u1", "")
    u2 = request.form.get("u2", "")
    u3 = request.form.get("u3", "")
    u4 = request.form.get("u4", "")
    u5 = request.form.get("u5", "")

    user_bio = f"{u1}\n{u2}\n{u3}\n{u4}\n{u5}"

    chat_history.append({"role": "user", "content": user_bio})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history
    )

    assistant_reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": assistant_reply})

    return render_template("chat.html", history=chat_history)


@app.route("/message", methods=["POST"])
def message():
    user_msg = request.form.get("message", "")
    chat_history.append({"role": "user", "content": user_msg})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history
    )

    assistant_reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": assistant_reply})

    return render_template("chat.html", history=chat_history)


if __name__ == "__main__":
    app.run(debug=True)
