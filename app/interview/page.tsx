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
        <div>
            <h1>AI Chat Agent</h1>
            <div style={{ height: '400px', overflowY: 'auto', border: '1px solid black', padding: '10px' }}>
                {messages.map((msg, idx) => (
                    <div key={idx}>{msg}</div>
                ))}
            </div>
            <div style={{ marginTop: '10px' }}>
                <input 
                    type="text" 
                    value={inputValue} 
                    onChange={e => setInputValue(e.target.value)}
                    placeholder="Type your message..."
                    style={{ width: '80%', marginRight: '10px' }}
                />
                <button onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    );
};

export default InterviewPage;
