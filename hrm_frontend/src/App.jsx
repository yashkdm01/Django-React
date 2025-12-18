import React from 'react';
import DepartmentPage from './components/DepartmentPage';

function App() {
  return (
    <div className="container-fluid">
      <div className="row">
        {/* sidebar */}
        <nav className="col-md-2 d-none d-md-block bg-light sidebar vh-100">
          <div className="sidebar-sticky pt-3">
            <h4>HRM Dashboard</h4>
            <ul className="nav flex-column mt-3">
              <li className="nav-item">
                <span className="nav-link active">Departments</span>
              </li>

            </ul>
          </div>
        </nav>

        {/* main content */}
        <main className="col-md-10 ms-sm-auto px-4">
          <h2 className="mt-3 mb-4">Department Management</h2>
          <DepartmentPage />
        </main>
      </div>
    </div>
  );
}

export default App;
