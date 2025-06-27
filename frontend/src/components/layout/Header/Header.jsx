import { useAuth } from '@hooks/useAuth';
import { Link, useNavigate } from 'react-router-dom';
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
      <nav className={styles.container}>
        <Link className={styles.logo} to="/">
          <img className={styles.logoIcon} src={logo} alt="BarberManager Logo" />
          Barber<span>Manager</span>
        </Link>

        {/* <ul className={styles.navLinks}>
          <li>
            <Link to="/">Home</Link>
          </li>

          {isAuthenticated && (
            <li>
              <Link to="/dashboard">Dashboard</Link>
            </li>
          )}
        </ul> */}

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
              <Link to="/login" className={styles.authBtn}>
                Login
              </Link>
              <Link to="/register" className={styles.authBtnAlt}>
                Register
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
