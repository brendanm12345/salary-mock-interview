// interview/page.tsx
'use client';
import React, { useEffect, useState } from 'react';
import { ReactMediaRecorder } from 'react-media-recorder';
import axios from 'axios';

const InterviewPage: React.FC = () => {
    const [data, setData] = useState({ message: '' });
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [messages, setMessages] = useState<Array<string>>([]);
    const [inputValue, setInputValue] = useState('');

    // Fetch the initial greeting from the server
    async function fetchDataFromServer() {
        try {
            const response = await fetch('http://127.0.0.1:5000/');
            const data = await response.json();
            setData(data);
        } catch (error) {
            console.error(error);
        }
    }

    const handleStopRecording = async (mediaBlobUrl: string | undefined) => {
        try {
            if (!mediaBlobUrl) {
                console.error('No media blob URL available');
            }
            const blob = await fetch(mediaBlobUrl!).then(res => res.blob());
            // const correctedBlob = new Blob([blob], { type: 'audio/wav' });
            const formData = new FormData();
            formData.append('file', blob, 'myAudio.wav');
            console.log('formdata', formData);

            // Send audio blob to your backend
            const response = await axios.post('http://127.0.0.1:5000/chat', formData, {
                headers: {
                    'Content-Type': 'audio/mpeg',
                },
            });
            const responseData = response.data;

            // Set the response (the transcribed text) as the input value
            setInputValue(responseData.response || '');

            setMessages([...messages, `You: ${inputValue}`, `AI: ${responseData.response}`]);
            setIsLoading(false); // reset loading state to false

        } catch (e) {
            console.error('There was an error sending the audio file!', e);
            setIsLoading(false); // reset loading state to false
        }
    };


    useEffect(() => {
        fetchDataFromServer();
    }, []);

    return (
        <div className='p-8'>
            <div className="h-96 overflow-y-auto border border-black p-2.5 rounded-md">
                {messages.map((msg, idx) => (
                    <div key={idx}>{msg}</div>
                ))}
            </div>
            <div className='flex flex-row justify-between mt-4 rounded-md space-x-4'>
                <input
                    type="text"
                    value={inputValue}
                    onChange={e => setInputValue(e.target.value)}
                    placeholder="Type your message..."
                    className='w-full p-4 flex-direction bg-slate-100 '
                />
                {/* <button className='p-4 bg-black text-white' onClick={handleSendMessage}>Send</button> */}
            </div>
            <ReactMediaRecorder
                audio
                render={({ status, startRecording, stopRecording, mediaBlobUrl }) => (
                    <div>
                        <p>{status}</p>
                        <button onClick={startRecording}>Start Recording</button>
                        <button onClick={() => {
                            stopRecording();
                            handleStopRecording(mediaBlobUrl);
                        }}>Stop Recording</button>
                        <audio src={mediaBlobUrl} controls />
                    </div>
                )}
            />
        </div>
    );
};

export default InterviewPage;
