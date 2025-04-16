import React from 'react';
import { motion } from "framer-motion";

function Experience(props) {
    const { experience } = props.data;
    return (
        <section id="experience">
            <h3>Experience</h3>
            {experience.map((job, index) => (
                <motion.div
                    className="job"
                    key={index}
                    whileHover={{ y: -5 }}
                    transition={{ duration: 0.2 }}
                >
                    <div className="job-header">
                        <h4>{job.company}</h4>
                        <p className="dates">{job.dates}</p>
                    </div>
                    <h5>{job.title}</h5>
                    <ul>
                        {job.description.map((item, i) => (
                            <li key={i}>{item}</li>
                        ))}
                    </ul>
                </motion.div>
            ))}
        </section>
    );
}

export default Experience;