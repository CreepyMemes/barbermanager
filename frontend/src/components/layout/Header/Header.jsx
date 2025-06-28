import { useAuth } from '@hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import defaultAvatar from '@assets/images/default-avatar.jpg';
import logo from '@assets/icons/barbermanager.svg';
import styles from './Header.module.scss';

import Spinner from '@components/common/Spinner/Spinner';
import Button from '@components/common/Button/Button';

export default function Header() {
  const { isAuthenticated, user, profile, logout, loading } = useAuth();
  const navigate = useNavigate();

  if (loading) return <Spinner />;

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className={styles.header}>
      <Button href="/" className={styles.logo}>
        <img className={styles.logoIcon} src={logo} alt="BarberManager Logo" />
        Barber<span>Manager</span>
      </Button>
      <div className={styles.actions}>
        {isAuthenticated && user && (
          <>
            <Button onClick={handleLogout} color="accent">
              Logout
            </Button>
            <div className={styles.profile}>
              <img src={profile.profile_image || defaultAvatar} alt="Profile" />
            </div>
          </>
        )}
        {!isAuthenticated && (
          <>
            <Button href="/login" color="primary">
              Login
            </Button>
            <Button href="/register" color="accent">
              Register
            </Button>
          </>
        )}
      </div>
    </header>
  );
}
