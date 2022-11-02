from flask import Flask, request, render_template
from datetime import datetime
import json

app = Flask(__name__)
DATA_FILE = "data.json"

def load_messages():
    with open(DATA_FILE, "r") as json_file:
        data = json.load(json_file)
        return data["all_messages"]



all_messages = load_messages()

def save_messages():
    with open(DATA_FILE, "w") as json_file:
        data = {"all_messages": all_messages}
        json.dump(data, json_file)


@app.route("/")
def hello_world():
    return "<p>hello, welcome</p>"
@app.route("/get_messages")
def get_messages():
    return {"messages": all_messages}

def add_message(sender, text):
  # time: подставить автоматически
  new_message = {
      "sender": sender,
      "text": text,
      "time": datetime.now().strftime("%H:%M"),
  }
  all_messages.append(new_message)
  save_messages()


add_message("Iana", "Do you understand anything?")
add_message("Rhys", "Everything, yes, it's easy")

# /send_message?sender=Iana&text=Hello
@app.route("/send_message")
def send_message():
    sender = request.args["sender"]
    text = request.args["text"]
    add_message(sender, text)

    return {"result": True}

@app.route("/chat")
def chat_page():
    return render_template("form.html")


app.run(debug=True)
