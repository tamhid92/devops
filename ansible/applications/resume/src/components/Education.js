import React from 'react';

function Education(props) {
    const { education } = props.data;
    return (
        <section id="education">
            <h3>Education</h3>
            <h4>{education.university}</h4>
            <p className="dates">{education.dates}</p>
            <p><strong></strong> {education.degree}</p>
            <p><strong>Relevant Coursework:</strong> {education.relevant_coursework}</p>
        </section>
    );
}

export default Education;