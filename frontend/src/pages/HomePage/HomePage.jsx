import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';

import Button from '@components/common/Button/Button';
import styles from './HomePage.module.scss';

export default function HomePage() {
  const { isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && isAuthenticated) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, loading, navigate]);

  // Don't show landing if redirecting (optional guard):
  if (loading || isAuthenticated) return null; // Or a spinner

  return (
    <div className={styles.homeContainer}>
      <h1>Welcome to Barber Manager!</h1>
      <p>This page is styled using a SASS module 🎉</p>
      <Button href="/login/">Login</Button>
    </div>
  );
}
