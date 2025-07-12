import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import SourceList from './components/SourceList';
import SourceForm from './components/SourceForm';
import SourceDetail from './components/SourceDetail';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Genealogical Sources Manager</h1>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<SourceList />} />
            <Route path="/add" element={<SourceForm />} />
            <Route path="/source/:id" element={<SourceDetail />} />
            <Route path="/edit/:id" element={<SourceForm />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
