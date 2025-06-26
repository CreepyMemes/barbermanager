import { useAuth } from '@hooks/useAuth';
import Spinner from '@components/common/Spinner/Spinner';
import styles from './Dashboard.module.scss';

// TODO: This is just a proof of concept that authenticated data is retreived
export default function Dashboard() {
  const { user, profile, loading } = useAuth();

  if (loading) return <Spinner />; // TODO: make a skeleton

  return (
    <div className={styles.dashboardWrapper}>
      <h1 className={styles.heading}>Dashboard</h1>
      {user && (
        <div className={styles.top}>
          <p>
            Welcome, <strong>{user?.username || user?.email}</strong>!
          </p>
          <p>
            Role: <strong>{user.role}</strong>
          </p>
        </div>
      )}
      {profile && (
        <div className={styles.profileSection}>
          <h2>Your Profile</h2>
          <pre className={styles.profileJson}>{JSON.stringify(profile, null, 2)}</pre>
        </div>
      )}
      {!profile && (
        <div className={styles.noProfile}>
          <em>Profile loading or unavailable.</em>
        </div>
      )}
    </div>
  );
}
