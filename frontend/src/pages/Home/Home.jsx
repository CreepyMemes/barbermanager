import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import styles from './Home.module.scss';

import Spinner from '@components/common/Spinner/Spinner';
import Button from '@components/common/Button/Button';

export default function Home() {
  const { isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();

  /**
   * On authentication state change, redirect authenticated users away from home.
   */
  useEffect(() => {
    if (!loading && isAuthenticated) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, loading, navigate]);

  // Don't show landing if redirecting
  if (loading || isAuthenticated) return <Spinner />;

  return (
    <div className={styles.homeContainer}>
      <div className={styles.text}>
        <h1>Welcome to Barber Manager!</h1>
        <p>A barber shop management software!</p>
        <Button href="/login/" size="md" width="content" color="primary">
          Get Started!
        </Button>
      </div>
    </div>
  );
}
