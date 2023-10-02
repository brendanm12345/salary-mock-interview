from langchain.schema import AIMessage, HumanMessage, SystemMessage

import json
import sys
from flask import Flask
from flask_cors import CORS
from langchain.chat_models import ChatOpenAI
from flask import request, jsonify
from dotenv import load_dotenv
import os
from uuid import uuid4
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS


import requests
from util.prompt import get_final_prompt, get_initial_prompt, get_second_prompt
from util.scrape import parse_url

load_dotenv("../.env")

openai_key = os.getenv("OPENAI_API_KEY")

sessions = {}

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ("*", "localhost:3000", "127.0.0.1:3000")}})


@app.route("/new", methods=["POST"])
def new_chat():
    try:
        app.logger.warning("GOT NEW CHAT REQ")
        data = request.get_json()
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

        sessions[session_id]["session_id"] = session_id

        chat_model = ChatOpenAI(openai_api_key=openai_key)
        candidate = parse_url(data["candidate_url"])
        job_description = parse_url(data["job_description_url"])
        initial_prompt = get_initial_prompt(
            candidate, job_description, data["minimum_salary"], data["maximum_salary"]
        )

        app.logger.warning(initial_prompt)
        metadata_response = chat_model.predict(initial_prompt)
        app.logger.warning(f"{metadata_response=}")
        second_prompt = get_second_prompt()
        app.logger.warning(second_prompt)
        response = chat_model.predict(second_prompt)

        sessions[session_id]["chat_model"] = chat_model
        sessions[session_id]["messages"] = [response]

        return jsonify(
            response={
                k: v for (k, v) in sessions[session_id].items() if k != "chat_model"
            }
        )
    except Exception as e:
        return jsonify(error=str(e)), 500


# Load the document and set up the retriever
# documents = TextLoader("path_to_your_document.txt").load() # Update the path to the actual file location
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
# texts = text_splitter.split_documents(documents)
# retriever = FAISS.from_documents(texts, OpenAIEmbeddings()).as_retriever(search_kwargs={"k": 5}) # We'll retrieve top 5 relevant chunks


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data["text"]
        app.logger.warning(user_input)
        if "session_id" not in data and len(list(sessions.keys())) == 0:
            data = {
                "candidate_url": "https://s3.amazonaws.com/nicbor.com/sample_resume.html",
                "job_description_url": "https://s3.amazonaws.com/nicbor.com/sample_job_description.html",
                "maximum_salary": 200000,
                "minimum_salary": 100000,
            }
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

            sessions[session_id]["session_id"] = session_id
            sessions[session_id]["messages"] = []

            chat_model = ChatOpenAI(openai_api_key=openai_key)
            candidate = parse_url(data["candidate_url"])
            job_description = parse_url(data["job_description_url"])
            initial_prompt = get_initial_prompt(
                candidate,
                job_description,
                data["minimum_salary"],
                data["maximum_salary"],
            )

            app.logger.warning(initial_prompt)
            sessions[session_id]["messages"].append(
                HumanMessage(content=initial_prompt)
            )

            metadata_response = chat_model.predict_messages(
                sessions[session_id]["messages"]
            )
            sessions[session_id]["messages"].append(metadata_response)
            app.logger.warning(f"{metadata_response=}")
            second_prompt = get_second_prompt()
            sessions[session_id]["messages"].append(HumanMessage(content=second_prompt))
            app.logger.warning(second_prompt)
            response = chat_model.predict_messages(sessions[session_id]["messages"])

            sessions[session_id]["chat_model"] = chat_model

            sessions[session_id]["messages"].append(response)

            data["session_id"] = session_id
            app.logger.warning("INIT SESSION")

        session_id = data.get("session_id", list(sessions.keys())[0])
        chat_model = sessions[session_id]["chat_model"]
        sessions[session_id]["messages"].append(HumanMessage(content=user_input))
        response = chat_model.predict_messages(sessions[session_id]["messages"])

        sessions[session_id]["messages"].append(response)
        try:
            response = json.loads(str(response.content))["message"]
            if response.get("event", None) == "interview_finished":
                third_prompt = get_final_prompt()
                sessions[session_id]["messages"].append(
                    HumanMessage(content=third_prompt)
                )

                final_response = chat_model.predict_messages(
                    sessions[session_id]["messages"]
                )
                response += final_response
        except Exception as e:
            app.logger.warning("RECOVERED")
            app.logger.warning(e)
            pass

        print(response)
        return jsonify(response=str(response))
    except Exception as e:
        return jsonify(error=str(e)), 500


# @app.route("/chat", methods=["POST"])
# def chat():
#     try:
#         data = request.get_json()
#         user_input = data["text"]
#         print(user_input)
#         chat_model = sessions[data.get("session_id", list(sessions.keys())[0])]["chat_model"]
#         response = chat_model.predict(user_input)
#         try:
#             parsed = json.parse(response)
#             if parsed.get("event", None) == "interview_finished":
#                 third_prompt = get_final_prompt()
#                 final_response = chat_model.predict(third_prompt)
#                 response += final_response
#         except Exception as e:
#             pass

#         return jsonify(response=response)
#     except Exception as e:
#         return jsonify(error=str(e)), 500


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

        app.logger.warning(json.dumps(args))
        resp = requests.post(
            "http://localhost:5000/new",
            json=args,
            headers={"Content-Type": "application/json"},
        )
        app.logger.warning(f"{resp.text=}")
        app.logger.warning(f"{resp.status_code=}")
    else:
        app.run(port=5000)
