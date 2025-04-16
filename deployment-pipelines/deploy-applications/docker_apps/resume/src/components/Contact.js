import React from 'react';
import { MdLocationOn, MdPhone, MdEmail, MdLink } from 'react-icons/md';

function Contact(props) {
    const { personal_info } = props.data;
    return (
        <section id="contact">
            <h3>Contact</h3>
            <div className="contact-items">
                <p><MdLocationOn /> {personal_info.location}</p>
                <p><MdPhone /> {personal_info.phone}</p>
                <p><MdEmail /> <a href={`mailto:${personal_info.email}`}>{personal_info.email}</a></p>
                <p><MdLink /> <a href={personal_info.github}>{personal_info.github}</a></p>
            </div>
        </section>
    );
}

export default Contact;