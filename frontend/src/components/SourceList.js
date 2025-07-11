import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const SourceList = () => {
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSources();
  }, []);

  const fetchSources = async () => {
    try {
      const response = await axios.get('/api/sources');
      setSources(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching sources:', error);
      setLoading(false);
    }
  };

  const deleteSource = async (id) => {
    if (window.confirm('Are you sure you want to delete this source?')) {
      try {
        await axios.delete(`/api/sources/${id}`);
        fetchSources();
      } catch (error) {
        console.error('Error deleting source:', error);
      }
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Sources</h2>
      <Link to="/add" className="button">Add New Source</Link>
      <div className="source-list">
        {sources.map(source => (
          <div key={source.id} className="source-card">
            <h3>{source.title}</h3>
            <p><strong>Type:</strong> {source.source_type || 'N/A'}</p>
            <p><strong>Date:</strong> {source.date || 'N/A'}</p>
            <p><strong>Location:</strong> {source.location || 'N/A'}</p>
            <p><strong>Created:</strong> {new Date(source.created_at).toLocaleDateString()}</p>
            <div>
              <Link to={`/source/${source.id}`} className="button secondary">View</Link>
              <Link to={`/edit/${source.id}`} className="button secondary" style={{marginLeft: '10px'}}>Edit</Link>
              <button 
                onClick={() => deleteSource(source.id)} 
                className="button danger" 
                style={{marginLeft: '10px'}}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
      {sources.length === 0 && <p>No sources found. Add your first source!</p>}
    </div>
  );
};

export default SourceList;
