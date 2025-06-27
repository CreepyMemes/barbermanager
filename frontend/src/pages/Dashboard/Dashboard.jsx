import { useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import styles from './Dashboard.module.scss';

import Spinner from '@components/common/Spinner/Spinner';

// TODO: This is just a proof of concept that authenticated data is retreived
export default function Dashboard() {
  const { user, profile, loading } = useAuth();
  const navigate = useNavigate();

  /**
   * Redirect to correct dashboard on mount
   */
  useEffect(() => {
    if (!loading && user) {
      if (user.role === 'ADMIN') navigate('admin', { replace: true });
      else if (user.role === 'BARBER') navigate('barber', { replace: true });
      else if (user.role === 'CLIENT') navigate('client', { replace: true });
    }
  }, [loading, user, navigate]);

  if (loading) return <Spinner />; // TODO: make a skeleton
  if (!profile) return <div className={styles.noProfile}>Profile loading or unavailable.</div>;

  return (
    <div className={styles.dashboardWrapper}>
      <Outlet />
    </div>
  );
}
