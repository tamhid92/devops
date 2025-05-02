import React from 'react';
import { motion } from "framer-motion";

function Projects(props) {
    const { personal_project } = props.data;
    return (
        <section id="projects">
            <h3>Personal Project</h3>
            <motion.div
                className="project-item"
                whileHover={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
            >
                <h4>{personal_project.name}</h4>
                <p>{personal_project.description}</p>
            </motion.div>
        </section>
    );
}

export default Projects;