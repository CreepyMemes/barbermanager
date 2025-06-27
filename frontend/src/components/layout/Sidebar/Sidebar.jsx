import { NavLink } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import defaultAvatar from '@assets/images/default-avatar.jpg';
import styles from './Sidebar.module.scss';

import Spinner from '@components/common/Spinner/Spinner';

// Define role-based navigation
const adminNav = [
  { to: '/dashboard/admin', label: 'Dashboard' },
  { to: '/dashboard/admin/appointments', label: 'Appointments' },
  { to: '/dashboard/admin/barbers', label: 'Barbers' },
  { to: '/dashboard/admin/clients', label: 'Clients' },
  { to: '/dashboard/admin/settings', label: 'Settings' },
];

const barberNav = [
  { to: '/dashboard/barber', label: 'Dashboard' },
  { to: '/dashboard/barber/services', label: 'Services' },
  { to: '/dashboard/barber/appointments', label: 'Appointments' },
  { to: '/dashboard/barber/reviews', label: 'Reviews' },
  { to: '/dashboard/barber/settings', label: 'Settings' },
];

const clientNav = [
  { to: '/dashboard/client', label: 'Dashboard' },
  { to: '/dashboard/client/appointments', label: 'Appointments' },
  { to: '/dashboard/client/reviews', label: 'Reviews' },
  { to: '/dashboard/client/settings', label: 'Settings' },
];

export default function Sidebar() {
  const { isAuthenticated, user, profile, loading } = useAuth();

  if (loading) return <Spinner />;

  // Get role specific nav items
  let navItems;

  if (!loading && user) {
    if (user.role === 'ADMIN') navItems = adminNav;
    else if (user.role === 'BARBER') navItems = barberNav;
    else if (user.role === 'CLIENT') navItems = clientNav;
  }

  return (
    <aside className={styles.sidebar}>
      <div className={styles.top}>
        {isAuthenticated && user && (
          <div className={styles.profile}>
            <img src={profile.profile_image || defaultAvatar} alt="Profile" />

            <div>
              <div className={styles.username}>{user.username || user.email}</div>
              <div className={styles.role}>{user.role?.toLowerCase() || ''}</div>
            </div>
          </div>
        )}
      </div>

      <nav className={styles.nav}>
        <ul>
          {navItems.map((item) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                className={({ isActive }) => [styles.link, isActive && styles.active].filter(Boolean).join(' ')}
                end
              >
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}
