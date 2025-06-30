import { useAuth } from '@hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import defaultAvatar from '@assets/images/default-avatar.jpg';
import styles from './Header.module.scss';

import Logo from '@components/common/Logo/Logo';
import Spinner from '@components/common/Spinner/Spinner';
import Button from '@components/common/Button/Button';

function Header() {
  const { isAuthenticated, user, profile, logout, loading } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className={styles.headerArea}>
      {isAuthenticated && loading ? (
        <Spinner />
      ) : (
        <div className={styles.header}>
          <Logo size="lg" button />

          <div className={styles.actions}>
            {isAuthenticated && user && (
              <>
                <Button onClick={handleLogout} size="md" color="primary">
                  Logout
                </Button>

                <div className={styles.profile}>
                  <img src={profile.profile_image || defaultAvatar} alt="Profile" />
                </div>
              </>
            )}

            {!isAuthenticated && (
              <>
                <Button href="/login" size="md" color="primary">
                  Login
                </Button>

                <Button href="/register" size="md" color="secondary">
                  Register
                </Button>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
}

export default Header;
