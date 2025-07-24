import { Routes, Route } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';
import RoleRedirect from './RoleRedirect';

import Layout from '@components/layout/Layout/Layout';

import Home from '@pages/Home/Home';
import Login from '@pages/Login/Login';
import RegisterClient from '@pages/RegisterClient/RegisterClient';
import RegisterBarber from '@pages/RegisterBarber/RegisterBarber';
import VerifyEmail from '@pages/VerifyEmail/VerifyEmail';
import RequestPasswordReset from '@pages/RequestPasswordReset/RequestPasswordReset';
import ConfirmPasswordReset from '@pages/ConfirmPasswordReset/ConfirmPasswordReset';
import NotFound from '@pages/NotFound/NotFound';

import Dashboard from '@pages/Dashboard/Dashboard';
import Settings from '@pages/Settings/Settings';

import AdminBarbers from '@pages/admin/AdminBarbers/AdminBarbers';
import AdminClients from '@pages/admin/AdminClients/AdminClients';
import AdminAppointments from '@pages/admin/AdminAppointments/AdminAppointments';
import BarberServices from '@pages/barber/BarberServices/BarberServices';
import BarberAppointments from '@pages/barber/BarberAppointments/BarberAppointments';
import BarberAvailabilities from '@pages/barber/BarberAvailabilities/BarberAvailabilities';
import BarberReviews from '@pages/barber/BarberReviews/BarberReviews';

// Helper for cleaner protected route declaration
const protectedRoute = (element, role) => <ProtectedRoute role={role}>{element}</ProtectedRoute>;

function AppRoutes() {
  return (
    <Routes>
      <Route element={<Layout />}>
        {/* Public pages (no need to be authenticated) */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register/" element={<RegisterClient />} />
        <Route path="/register/:uidb64/:token" element={<RegisterBarber />} />
        <Route path="/verify/:uidb64/:token" element={<VerifyEmail />} />
        <Route path="/reset-password" element={<RequestPasswordReset />} />
        <Route path="/reset-password/:uidb64/:token" element={<ConfirmPasswordReset />} />

        {/* Shortcut redirects (from /:page to  /:role/:page) */}
        <Route path="dashboard" element={protectedRoute(<RoleRedirect />)} />
        <Route path="settings" element={protectedRoute(<RoleRedirect />)} />

        {/* Role based pages */}
        <Route path=":role/dashboard" element={protectedRoute(<Dashboard />)} />
        <Route path=":role/settings" element={protectedRoute(<Settings />)} />

        {/* Unique role protected pages */}
        <Route path="admin/barbers" element={protectedRoute(<AdminBarbers />, 'ADMIN')} />
        <Route path="admin/clients" element={protectedRoute(<AdminClients />, 'ADMIN')} />
        <Route path="admin/appointments" element={protectedRoute(<AdminAppointments />, 'ADMIN')} />

        <Route path="barber/services" element={protectedRoute(<BarberServices />, 'BARBER')} />
        <Route path="barber/appointments" element={protectedRoute(<BarberAppointments />, 'BARBER')} />
        <Route path="barber/availabilities" element={protectedRoute(<BarberAvailabilities />, 'BARBER')} />
        <Route path="barber/reviews" element={protectedRoute(<BarberReviews />, 'BARBER')} />

        {/* 404 page (this must be last) */}
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default AppRoutes;
