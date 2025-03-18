import React from 'react';
import { motion } from "framer-motion";

function Languages(props) {
    const { languages } = props.data;
    return (
        <section id="languages">
            <h3>Languages</h3>
            <ul>
                {languages.map((lang, index) => (
                    <motion.li
                        key={index}
                        whileHover={{ scale: 1.05 }}
                        transition={{ duration: 0.2 }}
                    >
                        {lang}
                    </motion.li>
                ))}
            </ul>
        </section>
    );
}

export default Languages;