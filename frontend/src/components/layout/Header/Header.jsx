import { useAuth } from '@hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import styles from './Header.module.scss';

import Logo from '@components/common/Logo/Logo';
import Spinner from '@components/common/Spinner/Spinner';
import Button from '@components/common/Button/Button';
import ProfileImage from '@components/ui/ProfileImage/ProfileImage';

function Header() {
  const { isAuthenticated, profile, logout, isFetchingProfile } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className={styles.headerArea}>
      {isFetchingProfile ? (
        <Spinner />
      ) : (
        <div className={styles.header}>
          <Logo size="lg" button />

          <div className={styles.actions}>
            {isAuthenticated && profile && (
              <>
                <Button onClick={handleLogout} size="md" color="transdark">
                  Logout
                </Button>

                <ProfileImage src={profile.profile_image} />
              </>
            )}

            {!isAuthenticated && (
              <>
                <Button href="/login" size="md" color="transdark">
                  Login
                </Button>

                <Button href="/register" size="md" color="secondary">
                  Sign up
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
