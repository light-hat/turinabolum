// src/components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav className="uk-navbar-container" uk-navbar="true">
            <div className="uk-navbar-left">
                <ul className="uk-navbar-nav">
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/subscriptions">Subscriptions</Link></li>
                </ul>
            </div>
        </nav>
    );
};

export default Navbar;
