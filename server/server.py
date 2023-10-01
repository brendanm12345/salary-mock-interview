from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai
from langchain.chat_models import ChatOpenAI
from fastapi import HTTPException

load_dotenv("../.env")

openai_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_key

chat_model = ChatOpenAI(openai_api_key=openai_key)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        print(request.files)  # See if the files are actually being received.
        print('hi')
        if 'audio' not in request.files:
            print('no audio found')
            return jsonify(error="No audio file"), 400

        audio_file = request.files['audio']
        print('trying to transcribe')
        # Transcribing the audio to text using Whisper ASR
        try:
            transcript = openai.Audio.transcribe(
                "whisper-1", audio_file, api_key=openai_key)
        except Exception as e:
            print('error', e)
            raise HTTPException(
                status_code=400, detail="Could not transcribe audio")

        print(transcript)
        question = transcript["text"]
        
        # Getting a response for the transcribed text
        chat_response = chat_model.predict(question)
        
        return jsonify(response=chat_response)

    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/')
def hello_world():
    return {'message': 'Hello, World!'}

if __name__ == '__main__':
    app.run(port=5000)
