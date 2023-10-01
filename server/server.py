import sys
from flask import Flask
from flask_cors import CORS
from langchain.chat_models import ChatOpenAI
from flask import request, jsonify
from dotenv import load_dotenv
import os
from uuid import uuid4

import requests
from util.prompt import get_initial_prompt
from util.scrape import parse_url

load_dotenv("../.env")

openai_key = os.getenv("OPENAI_API_KEY")

sessions = {}

app = Flask(__name__)
CORS(
    app, resources={r"/*": {"origins": "*"}}
)  # This will allow all origins for all routes


@app.route("/new", methods=["POST"])
def new_chat():
    try:
        app.logger.info("GOT NEW CHAT REQ")
        data = request.get_json()
        candidate_url = data["candidate_url"]
        job_description_url = data["job_description_url"]
        minimum_salary = data.get("minimum_salary", None)
        maximum_salary = data.get("maximum_salary", None)
        session_id = uuid4()

        sessions[session_id] = {
            k: data[k]
            for k in (
                "candidate_url",
                "job_description_url",
                "minimum_salary",
                "maximum_salary",
            )
        }

        chat_model = ChatOpenAI(openai_api_key=openai_key)
        candidate = parse_url(candidate_url)
        job_description = parse_url(job_description_url)
        initial_prompt = get_initial_prompt(
            candidate, job_description, minimum_salary, maximum_salary
        )

        metadata_response = chat_model.predict(initial_prompt)
        print(metadata_response)
        response = chat_model.predict("")

        sessions[session_id]["chat_model"] = chat_model

        return jsonify(response=response)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data["text"]
        print(user_input)
        chat_model = sessions[data["session_id"]]["chat_model"]
        response = chat_model.predict(user_input)
        return jsonify(response=response)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/")
def hello_world():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    if sys.argv[-1] == "test":
        args = {
            "candidate_url": "https://s3.amazonaws.com/nicbor.com/sample_resume.html",
            "job_description_url": "https://s3.amazonaws.com/nicbor.com/sample_job_description.html",
            "minimum_salary": 100000,
            "maximum_salary": 200000,
        }

        resp = requests.post("http://localhost:5000/new", json=args)
        print(f"{resp.text=}")
    else:
        app.run(port=5000)
