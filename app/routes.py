import json
import os
import secrets

import requests
from dotenv import load_dotenv
<<<<<<< HEAD
from flask import Flask, request, stream_with_context, render_template
=======
from flask import Flask, request, stream_with_context
from flask_cors import CORS
>>>>>>> ab99b05351cf93186c91f490a39d36150ced30e7
from huggingface_hub import InferenceClient

load_dotenv()

law = os.getenv("LAW")
hf = os.getenv("HF")

client = InferenceClient(
    "meta-llama/Llama-3.2-3B-Instruct",
    api_key=hf,
)


bp = Flask(__name__)
CORS(bp)

tagp = """Write a keyword for a legal database based on the chat history and the current question.

Do not answer anything else, no explanation, just the keyword or keywords.

Example: "What is the consensus on abortion?" -> abortion"""
casep = """Write a response for the user's question, which is after all the URLs and SNIPPETs. Do not answer anything else, only reference cases given. Wrap your references each in <ref> and </ref> tags at the start of your response in the format <ref>{name}|||{url}</ref> where name is the case name, url is the relative url."""


@bp.route("/")
def home():
    return render_template('home.html')


@bp.route("/about")
def about():
    return render_template('about.html')


@bp.route("/search", methods=["POST"])
async def search_get():
    data = request.data.decode("utf-8")
    print(data)
    return search(data)


def search(data):
    headers = {"Authorization": f"Token {law}"}
    params = {"q": data}

    response = requests.get(
        "https://www.courtlistener.com/api/rest/v4/search/",
        params=params,
        headers=headers,
    )
    response.raise_for_status()
    return response.text


@bp.route("/session", methods=["POST"])
def session():
    data = json.loads(request.data.decode("utf-8"))

    def generate(data):
        yield ""
        if "session_id" not in data:
            session_id = secrets.token_urlsafe(16)
            sessions = json.loads(open("sessions.json").read())
            sessions[session_id] = []
            with open("sessions.json", "w") as f:
                f.write(json.dumps(sessions))
        else:
            session_id = data["session_id"]

        session = json.loads(open("sessions.json").read()).get(session_id, -1)
        if session == -1:
            yield json.dumps({"error": "Session not found"})
            return
        if len(session) == 0 or session[-1] != "user":
            pass
        else:
            yield json.dumps({"error": "Erm... you already sent a message."})

        session.append({"role": "user", "content": data["content"]})
        sessions = json.loads(open("sessions.json").read())
        sessions[session_id] = session
        with open("sessions.json", "w") as f:
            f.write(json.dumps(sessions))
        response = client.chat_completion(
            session[:-1] +
            [{"role": "user", "content": f"{data['content']}\n{tagp}"}]
        )
        print(response.choices[0].message.content)
        cases = json.loads(search(response.choices[0].message.content))[
            "results"][:25]

        with open("cases.json", "w") as f:
            f.write(json.dumps(cases))

        castr = ""
        for case in cases:
            castr += f'NAME: {case["caseName"]}\nURL: "https://www.courtlistener.com{case["absolute_url"]}"\nSNIPPET: "{case["opinions"][0]["snippet"]}"\n\n'

        casefull = {
            "role": "user",
            "content": f"{castr}\n\n{data['content']}\n\n{casep}",
        }
        total = ""
        for s in client.chat_completion(
            session[:-1] + [casefull],
            stream=True,
        ):
            if s is None:
                continue
            if "choices" not in s:
                continue
            if "delta" not in s["choices"][0]:
                continue
            if "content" not in s["choices"][0]["delta"]:
                continue
            response = s["choices"][0]["delta"]["content"]
            total += response
            yield json.dumps(
                {"type": "response", "session_id": session_id, "response": response}
            )
        sessions = json.loads(open("sessions.json").read())
        sessions[session_id].append({"role": "assistant", "content": total})
        with open("sessions.json", "w") as f:
            f.write(json.dumps(sessions))
        return

    return bp.response_class(
        stream_with_context(generate(data)), mimetype="application/json"
    )


if __name__ == "__main__":
    bp.run(host="0.0.0.0", port=5000, debug=True)
