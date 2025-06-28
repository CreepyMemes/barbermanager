import { useAuth } from '@hooks/useAuth';
import styles from './ClientDashboard.module.scss';
import defaultAvatar from '@assets/images/default-avatar.jpg';

import Spinner from '@components/common/Spinner/Spinner';

export default function ClientDashboard() {
  const { profile, loading } = useAuth();

  if (loading | !profile) return <Spinner />;

  return (
    <div className={styles.clientDashboard}>
      <div className={styles.profileHeader}>
        <img className={styles.profileImg} src={profile.profile_image || defaultAvatar} alt="Profile" />
        <div className={styles.bigTitle}>
          Welcome back {profile.name} {profile.surname}
          <p>{profile.username}</p>
        </div>
      </div>

      <div>
        <div className={styles.sectionTitle}>Appointments</div>
        <ul className={styles.appointList}>
          {profile.appointments && profile.appointments.length > 0 ? (
            profile.appointments.map((app) => (
              <li key={app.id}>
                <b>{app.date}</b> at <b>{app.slot}</b>
                <span style={{ marginLeft: '1.1rem', color: '#94928a' }}>Status: {app.status}</span>
              </li>
            ))
          ) : (
            <li>No appointments yet.</li>
          )}
        </ul>
      </div>

      <div>
        <div className={styles.sectionTitle}>Reviews</div>
        <ul className={styles.reviewList}>
          {profile.reviews && profile.reviews.length > 0 ? (
            profile.reviews.map((r) => (
              <li key={r.id}>
                <b>{r.rating}★</b> {r.comment}
                <span style={{ color: '#94928a', marginLeft: '1rem' }}>({r.created_at})</span>
              </li>
            ))
          ) : (
            <li>No reviews yet.</li>
          )}
        </ul>
      </div>
    </div>
  );
}
