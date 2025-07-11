import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const SourceForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    source_type: '',
    date: '',
    location: ''
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (id) {
      fetchSource();
    }
  }, [id]);

  const fetchSource = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/sources/${id}`);
      setFormData({
        title: response.data.title,
        description: response.data.description || '',
        source_type: response.data.source_type || '',
        date: response.data.date ? response.data.date.split('T')[0] : '',
        location: response.data.location || ''
      });
      setLoading(false);
    } catch (error) {
      console.error('Error fetching source:', error);
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (id) {
        await axios.put(`/api/sources/${id}`, formData);
      } else {
        await axios.post('/api/sources', formData);
      }
      navigate('/');
    } catch (error) {
      console.error('Error saving source:', error);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="form-container">
      <h2>{id ? 'Edit Source' : 'Add New Source'}</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title *</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="4"
          />
        </div>
        <div className="form-group">
          <label htmlFor="source_type">Source Type</label>
          <select
            id="source_type"
            name="source_type"
            value={formData.source_type}
            onChange={handleChange}
          >
            <option value="">Select type</option>
            <option value="document">Document</option>
            <option value="photo">Photo</option>
            <option value="record">Record</option>
            <option value="book">Book</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="date">Date</label>
          <input
            type="date"
            id="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label htmlFor="location">Location</label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleChange}
          />
        </div>
        <div>
          <button type="submit" className="button">
            {id ? 'Update Source' : 'Add Source'}
          </button>
          <button
            type="button"
            className="button secondary"
            onClick={() => navigate('/')}
            style={{marginLeft: '10px'}}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default SourceForm;
