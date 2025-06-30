import { Routes, Route } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';
import RoleRedirect from './RoleRedirect';

import Layout from '@components/layout/Layout/Layout';

import Home from '@pages/Home/Home';
import Login from '@pages/Login/Login';
import NotFound from '@pages/NotFound/NotFound';
import Dashboard from '@pages/Dashboard/Dashboard';

// Helper for cleaner protected route declaration
const protectedRoute = (element, role) => <ProtectedRoute role={role}>{element}</ProtectedRoute>;

function AppRoutes() {
  return (
    <Routes>
      <Route element={<Layout />}>
        {/* Public pages (no need to be authenticated) */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />

        {/* Shortcut redirects (from /:page to  /:role/:page) */}
        <Route path="dashboard" element={protectedRoute(<RoleRedirect />)} />
        {/* <Route path="settings" element={protectedRoute(<RoleRedirect />)} /> */}

        {/* Role based pages */}
        <Route path=":role/dashboard" element={protectedRoute(<Dashboard />)} />
        {/* <Route path=":role/settings" element={protectedRoute(<Settings />)} /> */}

        {/* Unique role protected pages */}
        {/* <Route path="admin/barbers" element={protectedRoute(<div>hello</div>, 'ADMIN')} /> */}

        {/* 404 page (this must be last) */}
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default AppRoutes;
