import { Routes, Route } from 'react-router-dom';

import LoginPage from '@pages/auth/Login/LoginPage';

// TODO: Import create and import ProtectedRoute component

export default function AppRoutes() {
  return (
    <Routes>
      {/*<Route path="/" element={<HomePage />} />*/}
      <Route path="/login" element={<LoginPage />} />
      {/* <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} /> */}
      {/*<Route path="*" element={<NotFound />} />*/}

      {/* Catch all unmatched routes */}
      {/*<Route path="*" element={<NotFound />} />*/}
    </Routes>
  );
}
