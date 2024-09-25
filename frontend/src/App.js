// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { ApolloWrapper } from './apolloClient';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Subscriptions from './components/Subscriptions';

function App() {
  return (
    <ApolloWrapper>
      <Router>
        <Navbar />
        <div className="uk-container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/subscriptions" element={<Subscriptions />} />
          </Routes>
        </div>
      </Router>
    </ApolloWrapper>
  );
}

export default App;