import React, { useEffect, useState } from 'react';
import axios from 'axios';

function DepartmentPage() {
  const [departments, setDepartments] = useState([]);
  const [formData, setFormData] = useState({
    dept_name: '',
    description: '',
    status: true,
  });
  const [editingId, setEditingId] = useState(null);
  const [search, setSearch] = useState('');

  const API_BASE = process.env.REACT_APP_API_BASE;
;    

  // load departments on first render
  useEffect(() => {
    fetchDepartments();
  }, []);

  const fetchDepartments = async () => {
  try {
    const response = await axios.get(API_BASE);
    setDepartments(response.data);
  } catch (error) {
    console.error('Error fetching departments:', error);
    alert('Could not load departments. Check console for details.');
  }
};

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    if (editingId) {
      await axios.put(`${API_BASE}${editingId}/`, formData);
    } else {
      await axios.post(API_BASE, formData);
    }
    setFormData({ dept_name: '', description: '', status: true });
    setEditingId(null);
    fetchDepartments();
  } catch (error) {
    console.error('Error saving department:', error);
    alert('Could not save department. Check console for details.');
  }
};

  const handleEdit = (dept) => {
    setEditingId(dept.dept_id);
    setFormData({
      dept_name: dept.dept_name,
      description: dept.description,
      status: dept.status,
    });
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Mark this department as inactive?')) return;
    await axios.delete(`${API_BASE}${id}/`);
    fetchDepartments();
  };

  const filteredDepartments = departments.filter((d) =>
    d.dept_name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      {/* Search + table */}
      <div className="mb-4">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h4 className="mb-0">Department List</h4>
          <input
            type="text"
            className="form-control w-25"
            placeholder="Search by name"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <table className="table table-bordered table-striped">
          <thead className="table-light">
            <tr>
              <th>#</th>
              <th>Department Name</th>
              <th>Description</th>
              <th>Status</th>
              <th style={{ width: '160px' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredDepartments.map((dept, index) => (
              <tr key={dept.dept_id}>
                <td>{index + 1}</td>
                <td>{dept.dept_name}</td>
                <td>{dept.description}</td>
                <td>{dept.status ? 'Active' : 'Inactive'}</td>
                <td>
                  <button
                    className="btn btn-sm btn-warning me-2"
                    onClick={() => handleEdit(dept)}
                  >
                    Edit
                  </button>
                  <button
                    className="btn btn-sm btn-danger"
                    onClick={() => handleDelete(dept.dept_id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
            {filteredDepartments.length === 0 && (
              <tr>
                <td colSpan="5" className="text-center">
                  No departments found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* create / update form */}
      <div className="card">
        <div className="card-header">
          {editingId ? 'Update Department' : 'Create Department'}
        </div>
        <div className="card-body">
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="form-label">Department Name</label>
              <input
                type="text"
                name="dept_name"
                className="form-control"
                value={formData.dept_name}
                onChange={handleChange}
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Description</label>
              <textarea
                name="description"
                className="form-control"
                value={formData.description}
                onChange={handleChange}
                rows="3"
                required
              />
            </div>

            <div className="form-check mb-3">
              <input
                className="form-check-input"
                type="checkbox"
                id="statusCheck"
                name="status"
                checked={formData.status}
                onChange={handleChange}
              />
              <label className="form-check-label" htmlFor="statusCheck">
                Active
              </label>
            </div>

            <button type="submit" className="btn btn-primary">
              {editingId ? 'Update' : 'Create'}
            </button>
            {editingId && (
              <button
                type="button"
                className="btn btn-secondary ms-2"
                onClick={() => {
                  setEditingId(null);
                  setFormData({ dept_name: '', description: '', status: true });
                }}
              >
                Cancel
              </button>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}

export default DepartmentPage;
