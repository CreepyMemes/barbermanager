import { useAuth } from '@hooks/useAuth';
import defaultAvatar from '@assets/images/default-avatar.jpg';
import styles from './Sidebar.module.scss';

import Spinner from '@components/common/Spinner/Spinner';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';

// Define role-based navigation
const adminNav = [
  { to: '/admin/dashboard', label: 'Dashboard', icon: 'dashboard' },
  { to: '/admin/appointments', label: 'Appointments', icon: 'appointment' },
  { to: '/admin/barbers', label: 'Barbers', icon: 'dashboard' },
  { to: '/admin/clients', label: 'Clients', icon: 'dashboard' },
  { to: '/admin/settings', label: 'Settings', icon: 'dashboard' },
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
              <Button
                nav
                href={item.to}
                size="md"
                // className={styles.link}
                activeClassName={styles.active}
                // width="content"    // Optional, removes block fill if you want it
                color="borderless" // Or as you like
              >
                <span className={styles.line}>
                  <Icon name={item.icon} size={'md'} />
                  {item.label}
                </span>
              </Button>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}
