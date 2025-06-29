import { Routes, Route } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';
import RoleRedirect from './RoleRedirect';

import Layout from '@components/layout/Layout/Layout';

import Home from '@pages/Home/Home';
import Login from '@pages/Login/Login';
import NotFound from '@pages/NotFound/NotFound';

import AdminDashboard from '@pages/admin/Dashboard/AdminDashboard';
import BarberDashboard from '@pages/barber/Dashboard/BarberDashboard';
import ClientDashboard from '@pages/client/Dashboard/ClientDashboard';

// Helper for cleaner protected route declaration
const protectedRoute = (element, role) => <ProtectedRoute role={role}>{element}</ProtectedRoute>;

function AppRoutes() {
  return (
    <Routes>
      <Route element={<Layout />}>
        {/* Public pages */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        {/* <Route path="/register" element={<Register />} /> */}

        {/* Shortcut redirects for dashboard, settings, profile */}
        <Route path="dashboard" element={protectedRoute(<RoleRedirect />)} />
        {/* <Route path="profile" element={protectedRoute(<RoleRedirect />)} /> */}

        {/* Admin pages */}
        <Route path="admin">
          <Route path="dashboard" element={protectedRoute(<AdminDashboard />, 'ADMIN')} />
          {/* <Route path="profile" element={protectedRoute(<AdminProfile />, 'ADMIN')} /> */}
        </Route>

        {/* Barber pages */}
        <Route path="barber">
          <Route path="dashboard" element={protectedRoute(<BarberDashboard />, 'BARBER')} />
        </Route>

        {/* Client pages */}
        <Route path="client">
          <Route path="dashboard" element={protectedRoute(<ClientDashboard />, 'CLIENT')} />
        </Route>

        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default AppRoutes;
