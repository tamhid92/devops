import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Contact from './components/Contact';
import Experience from './components/Experience';
import Skills from './components/Skills';
import Education from './components/Education';
import Projects from './components/Projects';
import Languages from './components/Languages';
import { motion } from "framer-motion";
import './App.css';

function App() {
    const [data, setData] = useState(null);

    useEffect(() => {
        fetch('/resume_data.json')
            .then(response => response.json())
            .then(data => setData(data))
            .catch(error => console.error('Error fetching data:', error));
    },);

    if (!data) {
        return <div>Loading...</div>;
    }

    return (
        <motion.div
            className="container dark"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
        >
            <Header data={data} />
            <Contact data={data} />
            <Experience data={data} />
            <Skills data={data} />
            <Education data={data} />
            <Projects data={data} />
            <Languages data={data} />
        </motion.div>
    );
}

export default App;