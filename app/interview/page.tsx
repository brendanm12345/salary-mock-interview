// interview/page.tsx
'use client';
import React, { useEffect, useState } from 'react';

const InterviewPage: React.FC = () => {
    const [data, setData] = useState({ message: '' });

    // Fetch data from the server
    async function fetchDataFromServer() {
        try {
            console.log('1')
            const response = await fetch('http://127.0.0.1:5000/');
            console.log('2')

            const data = await response.json();
            console.log(data);
            setData(data);
        } catch (error) {
            console.error(error);
        }      
    }

    useEffect(() => {
        fetchDataFromServer();
    }, []);

    return <div>Interview: {data.message}</div>;
};

export default InterviewPage;

