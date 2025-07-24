import { useAuth } from '@hooks/useAuth';

import Spinner from '@components/common/Spinner/Spinner';
import RoleSwitch from '@components/common/RoleSwitch/RoleSwitch';

import AdminSettings from '@pages/admin/AdminSettings/AdminSettings';
import BarberSettings from '@pages/barber/BarberSettings/BarberSettings';
import ClientSettings from '@pages/client/ClientSettings/ClientSettings';

export default function Settings() {
  const { isFetchingProfile, profile } = useAuth();

  // Show skeleton while loading profile data
  if (isFetchingProfile || !profile) return <Spinner />;

  return (
    <RoleSwitch
      admin={<AdminSettings />} // Role based page switch
      barber={<BarberSettings />}
      client={<ClientSettings />}
    />
  );
}
