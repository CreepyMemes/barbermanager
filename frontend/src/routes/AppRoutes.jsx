import { Routes, Route } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';

import Home from '@pages/Home/Home';
import Login from '@pages/Login/Login';
import Dashboard from '@pages/Dashboard/Dashboard';
import AdminDashboard from '@pages/Dashboard/AdminDashboard/AdminDashboard';
import BarberDashboard from '@pages/Dashboard/BarberDashboard/BarberDashboard';
import ClientDashboard from '@pages/Dashboard/ClientDashboard/ClientDashboard';
import NotFound from '@pages/NotFound/NotFound';

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      >
        <Route path="admin" element={<AdminDashboard />} />
        <Route path="barber" element={<BarberDashboard />} />
        <Route path="client" element={<ClientDashboard />} />
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
