import { useAuth } from '@hooks/useAuth';

/**
 * Just dispatches Page based on role, (NO loading/auth logic)
 */
function RoleSwitch({ admin, barber, client, fallback = null }) {
  const { profile } = useAuth();

  switch (profile.role) {
    case 'ADMIN':
      return admin;
    case 'BARBER':
      return barber;
    case 'CLIENT':
      return client;
    default:
      return fallback;
  }
}

export default RoleSwitch;
