import React from 'react';
import { motion } from "framer-motion";

function Skills(props) {
    const { technical_skills } = props.data;
    return (
        <section id="skills">
            <h3>Technical Skills</h3>
            <div className="skills-list">
                {technical_skills.map((skill, index) => (
                    <motion.div
                        className="skill-item"
                        key={index}
                        whileHover={{ scale: 1.1 }}
                        transition={{ duration: 0.2 }}
                    >
                        {skill}
                    </motion.div>
                ))}
            </div>
        </section>
    );
}

export default Skills;