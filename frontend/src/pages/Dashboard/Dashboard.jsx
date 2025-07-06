import { useAuth } from '@hooks/useAuth';

import Spinner from '@components/common/Spinner/Spinner';
import RoleSwitch from '@components/common/RoleSwitch/RoleSwitch';

import AdminDashboard from '@pages/admin/AdminDashboard/AdminDashboard';
import BarberDashboard from '@pages/barber/BarberDashboard/BarberDashboard';
import ClientDashboard from '@pages/client/ClientDashboard/ClientDashboard';

export default function Dashboard() {
  const { isFetchingProfile, profile } = useAuth();

  // Show skeleton while loading profile data
  if (isFetchingProfile || !profile) return <Spinner />;

  return (
    <RoleSwitch
      admin={<AdminDashboard />} // Role based page switch
      barber={<BarberDashboard />}
      client={<ClientDashboard />}
    />
  );
}
