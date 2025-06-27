import { useAuth } from '@hooks/useAuth';
import styles from './BarberDashboard.module.scss';
import defaultAvatar from '@assets/images/default-avatar.jpg';

import Spinner from '@components/common/Spinner/Spinner';

export default function BarberDashboard() {
  const { profile, loading } = useAuth();

  if (loading) return <Spinner />;
  if (!profile) return null;

  return (
    <div className={styles.barberDashboard}>
      <div className={styles.profileHeader}>
        <img className={styles.profileImg} src={profile.profile_image || defaultAvatar} alt="Profile" />
        <div>
          <div className={styles.bigTitle}>
            Welcome back {profile.name} {profile.surname}
            <p>{profile.username}</p>
          </div>
        </div>
      </div>

      <div>
        <div className={styles.sectionTitle}>Services</div>
        <ul className={styles.serviceList}>
          {profile.services.map((s) => (
            <li key={s.id}>
              <b>{s.name}</b> — ${s.price}
            </li>
          ))}
        </ul>
      </div>

      <div>
        <div className={styles.sectionTitle}>Availabilities</div>
        <ul className={styles.availList}>
          {profile.availabilities.map((av) => (
            <li key={av.id}>
              {av.date} ({av.slots.join(', ')})
            </li>
          ))}
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
