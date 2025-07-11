import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const SourceDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [source, setSource] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSource();
  }, [id]);

  const fetchSource = async () => {
    try {
      const response = await axios.get(`/api/sources/${id}`);
      setSource(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching source:', error);
      setLoading(false);
    }
  };

  const deleteSource = async () => {
    if (window.confirm('Are you sure you want to delete this source?')) {
      try {
        await axios.delete(`/api/sources/${id}`);
        navigate('/');
      } catch (error) {
        console.error('Error deleting source:', error);
      }
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!source) {
    return <div>Source not found</div>;
  }

  return (
    <div className="form-container">
      <h2>{source.title}</h2>
      <div>
        <p><strong>Type:</strong> {source.source_type || 'N/A'}</p>
        <p><strong>Date:</strong> {source.date || 'N/A'}</p>
        <p><strong>Location:</strong> {source.location || 'N/A'}</p>
        <p><strong>Created:</strong> {new Date(source.created_at).toLocaleDateString()}</p>
        <p><strong>Description:</strong></p>
        <p>{source.description || 'No description provided'}</p>
      </div>
      <div>
        <button 
          onClick={() => navigate(`/edit/${id}`)} 
          className="button"
        >
          Edit
        </button>
        <button 
          onClick={deleteSource} 
          className="button danger"
          style={{marginLeft: '10px'}}
        >
          Delete
        </button>
        <button 
          onClick={() => navigate('/')} 
          className="button secondary"
          style={{marginLeft: '10px'}}
        >
          Back to List
        </button>
      </div>
    </div>
  );
};

export default SourceDetail;
