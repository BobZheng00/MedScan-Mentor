import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Auth from './auth';



const rootElement = document.getElementById('root') as HTMLElement;
const root = ReactDOM.createRoot(rootElement);

root.render(
    <React.StrictMode>
        <Router>
            <Routes>
                <Route path="/" element={<Auth />} />
                
            </Routes>
        </Router>
    </React.StrictMode>
);
