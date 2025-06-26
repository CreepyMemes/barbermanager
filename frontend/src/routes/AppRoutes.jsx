import { Routes, Route } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';

import HomePage from '@pages/home/HomePage';
import LoginPage from '@pages/login/LoginPage';
import DashboardPage from '@pages/dashboard/DashboardPage';
import NotFoundPage from '@pages/not-found/NotFoundPage';

// TODO: Import create and import ProtectedRoute component

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      />

      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
