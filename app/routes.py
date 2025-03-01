import json
import os
import secrets

import requests
from dotenv import load_dotenv
<<<<<<< HEAD
from flask import Flask, request, stream_with_context, render_template
=======
from flask import Flask, render_template, request, stream_with_context
>>>>>>> 83f41731e22bf5b4c2ad1079436a8b24ce2549ec
from flask_cors import CORS
from huggingface_hub import InferenceClient

load_dotenv()

law = os.getenv("LAW")
hf = os.getenv("HF")

client = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.3",
    api_key=hf,
)


bp = Flask(__name__, template_folder="../templates", static_folder="../static")
CORS(bp)

<<<<<<< HEAD
tagp = """Write a keyword for a legal database based on the chat history and the current question.
f
=======
tagp = """
Intersections: AND or &
This connector is used by default, and so is not usually needed. However, some operators, like the negation operator, can change the default operator to OR. Therefore, in more complicated queries it is good practice to explicitly intersect your tokens by using the AND or & operator between all words e.g:

(immigration AND asylum) AND (border OR patrol) or

(immigration & asylum) & (border OR patrol)

Unions: OR
Creates an OR comparison between words (e.g. immigration OR asylum).

Negation/Exclusion: -
Requires that a word or phrase be excluded from the returned results. For example, this finds documents containing "immigration" but not "border patrol":

immigration -"border patrol"

This operator makes other tokens in your query fuzzy. Therefore, to do a boolean search, use the intersection operator (AND) between all your other tokens. For example, this searches for items containing both "immigration" and "border," but not "border patrol":

immigration AND border AND -"border patrol"

This query does "immigration" or "border" but not "border patrol":

immigration border -"border patrol".

But not : NOT or %
The NOT operator or % serves as an alternative way to exclude terms from your search results. This operator is particularly useful when combined with other boolean operators or grouped queries to refine your search precision:

"border patrol" NOT (immigration OR asylum) or

"border patrol" % (immigration OR asylum)

Phrase and Exact Queries: " "
Creates a phrase search (e.g. "border patrol").

You can also use " " to perform an exact query, which will not apply stemming or match synonyms.

For instance: "Inform" people will return results containing only inform and people, thus avoiding results that include information. Conversely, "Information" people, will exclude results containing inform.

It's important to notice that a phrase query behaves as an exact query for each term within the phrase. Therefore, avoid nesting quotes, such as ""Inform" people" as all the quotes will be ignored.

In the case that quotation marks are not balanced (i.e. there is an odd number of them), they will be ignored.

Grouped Queries and subqueries: ( )
Using parentheses will group parts of a query (e.g. (customs OR "border patrol") AND asylum). Parentheses can be nested as deeply as needed.

Wildcards and Fuzzy Search: *, !, ? and ~
Using an asterisk (*) allows for wildcard searches. For example, immigra* finds all words that begin with "immigra". Alternatively, you can use an exclamation mark (!) at the beginning of a word for the same purpose. For instance, !immigra matches words that start with "immigra".

* can also be used inside words, where it acts as a single-character wildcard. For example, a query like gr*mm*r would match cases containing both "grammar" and "grimmer".

The question mark character (?) can be used similarly as a single-character wildcard. Unlike *, it is allowed at the beginning of words. For example, this would find cases containing the word "immigrant" or "emmigration": ?mmigra*.

Fuzzy search can be applied using the tilde character (~) after a word. This is an advanced parameter that allows searches for misspellings or variations in a word's spelling. For example, searching for immigrant~ would find words similar to "immigrant." Values can also be added after the tilde to specify the maximum number of changes allowed, where a change refers to the insertion, deletion, substitution of a single character, or transposition of two adjacent characters. The default value, if none is given, is 2. Allowed values are 1 and 2. Fuzzy searches tend to broaden the result set, thus lowering precision, but also casting a wider net.

Disallowed Wildcards
The following types of wildcard queries are disabled due to performance issues:

* at the beginning of terms
Queries like *ing are disallowed because they require examining all terms in the index, which is highly resource-intensive.

Multiple endings with * or ! in short terms
Queries that match multiple endings are only allowed if the base word has at least three characters. Therefore, queries like a*, bc*, !a, or !bc are disallowed due to performance issues.

Performing a query like these will throw an error with the message:

The query contains a disallowed wildcard pattern.

Proximity: ~
Using a tilde character (~) after a phrase will ensure that the words in the phrase are within a desired distance of each other. For example "border fence"~50 would find the words border and fence within 50 words of each other.

Range Queries: [ ]
Ranges can be queried by using brackets. For example, a search for [1939 TO 1945] would find all cases that contained the numbers 1939 to 1945, inclusive. Range queries can also be fielded, allowing searches like citation:([22 TO 23] F2), which would find all cases from volumes 22 and 23 of the second series of the Federal Reporter. In range queries, the word 'TO' must be uppercase.

Date Queries
Date queries require the ISO-8601 standard date formatting. This means that dates must be formatted as follows:

YYYY-MM-DD

In English that's year-month-day. For example, here's a date range that finds all docket filings from October 2018:

dateFiled:[2018-10-01 TO 2018-10-31]


Write a query for a legal database based on the chat history and the current question and the operators above.

>>>>>>> 83f41731e22bf5b4c2ad1079436a8b24ce2549ec
Do not answer anything else, no explanation, just the keyword or keywords.

Example: "What is the consensus on abortion?" -> abortion, roe v. wade, planned parenthood v. casey"""
casep = """Write a response for the user's question, which is after all the URLs and SNIPPETs.

Reference the cases given in your response, embedding the links like [case name](url).

Write your answer in markdown."""


@bp.route("/")
def home():
    return render_template("home.html")


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/search", methods=["POST"])
async def search_get():
    data = request.data.decode("utf-8")
    print(data)
    return search(data)


def search(data):
    headers = {"Authorization": f"Token {law}"}
    params = {"q": data, type: "o", "highlight": "on"}

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
            [{"role": "system", "content": tagp}]
            + session[:-1]
            + [{"role": "user", "content": f"{data['content']}"}]
        )
        print(response.choices[0].message.content)
        cases = json.loads(search(response.choices[0].message.content))["results"][:25]

        with open("cases.json", "w") as f:
            f.write(json.dumps(cases))

        castr = ""
        for case in cases:
            castr += f'NAME: {case["caseName"]}\nURL: "https://www.courtlistener.com{case["absolute_url"]}"\nSNIPPET: "{case["opinions"][0]["snippet"]}"\n\n'

        casefull = {
            "role": "user",
            "content": data["content"],
        }
        total = ""
        for s in client.chat_completion(
            [{"role": "system", "content": castr + "\n\n" + casep}]
            + session[:-1]
            + [casefull],
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
                {"type": "response", "session_id": session_id, "response": total}
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
