import React from 'react';
import profilePic from '../IMG_6804.jpg';
import { motion } from "framer-motion";

function Header(props) {
    const { personal_info } = props.data;
    return (
        <motion.header
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <div className="profile-pic-container">
                <img src={profilePic} alt={personal_info.name} className="profile-pic" />
            </div>
            <h1>{personal_info.name}</h1>
            <h2>{personal_info.title}</h2>
            <p className="summary">{personal_info.summary}</p>
        </motion.header>
    );
}

export default Header;