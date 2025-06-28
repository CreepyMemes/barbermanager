import { useAuth } from '@hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import defaultAvatar from '@assets/images/default-avatar.jpg';
import styles from './Header.module.scss';

import Logo from '@components/common/Logo/Logo';
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
      <Logo size="lg" />

      <div className={styles.actions}>
        {isAuthenticated && user && (
          <>
            <Button onClick={handleLogout} color="primary">
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

            <Button href="/register" color="secondary">
              Register
            </Button>
          </>
        )}
      </div>
    </header>
  );
}
