// interview/page.tsx
'use client';
import React, { useEffect, useState } from 'react';

const InterviewPage: React.FC = () => {
    const [data, setData] = useState({ message: '' });
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

    // Send the current input value to the server and get AI's response
    async function handleSendMessage() {
        try {
            const response = await fetch(`http://127.0.0.1:5000/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: inputValue })
            });
            const responseData = await response.json();
            setMessages([...messages, `You: ${inputValue}`, `AI: ${responseData.response}`]);
            setInputValue('');
        } catch (error) {
            console.error(error);
        }
    }

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
                <button className='p-4 bg-black text-white' onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    );
};

export default InterviewPage;
