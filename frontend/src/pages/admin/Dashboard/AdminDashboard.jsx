import { useAuth } from '@hooks/useAuth';
import styles from './AdminDashboard.module.scss';
import defaultAvatar from '@assets/images/default-avatar.jpg';

import Spinner from '@components/common/Spinner/Spinner';

function AdminDashboard() {
  const { profile } = useAuth();

  console.log(profile);
  if (!profile) return <Spinner />;

  return (
    <div className={styles.adminDashboard}>
      <div className={styles.profileHeader}>
        <img className={styles.profileImg} src={profile.profile_image || defaultAvatar} alt="Profile" />
        <div className={styles.bigTitle}>
          Welcome back {profile.name} {profile.surname}
          <p>{profile.username}</p>
        </div>
      </div>

      <div className={styles.profileStats}>
        <div className={styles.stat}>
          <div className={styles.statValue}>{profile.total_clients}</div>
          <div className={styles.statLabel}>Clients</div>
        </div>
        <div className={styles.stat}>
          <div className={styles.statValue}>{profile.total_barbers}</div>
          <div className={styles.statLabel}>Barbers</div>
        </div>
        <div className={styles.stat}>
          <div className={styles.statValue}>{profile.total_appointments}</div>
          <div className={styles.statLabel}>Appointments</div>
        </div>
        <div className={styles.stat}>
          <div className={styles.statValue}>${profile.total_revenue}</div>
          <div className={styles.statLabel}>Revenue</div>
        </div>
        <div className={styles.stat}>
          <div className={styles.statValue}>{profile.total_reviews}</div>
          <div className={styles.statLabel}>Reviews</div>
        </div>
        <div className={styles.stat}>
          <div className={styles.statValue}>{profile.average_rating}</div>
          <div className={styles.statLabel}>Avg Rating</div>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
