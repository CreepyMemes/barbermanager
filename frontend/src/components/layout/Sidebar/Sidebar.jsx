import { NavLink } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import defaultAvatar from '@assets/images/default-avatar.jpg';
import styles from './Sidebar.module.scss';

import Spinner from '@components/common/Spinner/Spinner';

// Define role-based navigation
const adminNav = [
  { to: '/admin/dashboard', label: 'Dashboard' },
  { to: '/admin/appointments', label: 'Appointments' },
  { to: '/admin/barbers', label: 'Barbers' },
  { to: '/admin/clients', label: 'Clients' },
  { to: '/admin/settings', label: 'Settings' },
];
const barberNav = [
  { to: '/barber/dashboard', label: 'Dashboard' },
  { to: '/barber/services', label: 'Services' },
  { to: '/barber/appointments', label: 'Appointments' },
  { to: '/barber/reviews', label: 'Reviews' },
  { to: '/barber/settings', label: 'Settings' },
];
const clientNav = [
  { to: '/client/dashboard', label: 'Dashboard' },
  { to: '/client/appointments', label: 'Appointments' },
  { to: '/client/reviews', label: 'Reviews' },
  { to: '/client/settings', label: 'Settings' },
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
    <aside className={styles.sidebar} aria-label="Sidebar navigation">
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
      <nav className={styles.nav} aria-label="Main navigation">
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
