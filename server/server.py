from flask import Flask
from flask_cors import CORS
from langchain.chat_models import ChatOpenAI   
from flask import request, jsonify
from dotenv import load_dotenv
import os

load_dotenv("../.env")

openai_key = os.getenv('OPENAI_API_KEY')

chat_model = ChatOpenAI(openai_api_key=openai_key)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # This will allow all origins for all routes

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        prompt = data['text']
        print(prompt)
        response = chat_model.predict(prompt)
        return jsonify(response=response)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/')
def hello_world():
    return {'message': 'Hello, World!'}

if __name__ == '__main__':
    app.run(port=5000)
