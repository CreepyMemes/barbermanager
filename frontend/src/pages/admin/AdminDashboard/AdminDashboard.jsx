import { useAuth } from '@hooks/useAuth';
import styles from './AdminDashboard.module.scss';
import Card from '@components/common/Card/Card';
import Icon from '@components/common/Icon/Icon';
import CakeChart from '@components/common/CakeChart/CakeChart';

function AdminDashboard() {
  const { profile } = useAuth();

  return (
    <>
      {/* Clients */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="client" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Total Clients</div>
          <div className={styles.value}>{profile?.total_clients ?? 0}</div>
        </div>
      </Card>

      {/* Barbers */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="barber" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Total Barbers</div>
          <div className={styles.value}>{profile?.total_barbers ?? 0}</div>
        </div>
      </Card>

      {/* Appointments */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="appointment" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Total Appointments</div>
          <div className={styles.value}>{profile?.total_appointments ?? 0}</div>
        </div>
      </Card>

      {/* Revenue */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="revenue" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Total Revenue</div>
          <div className={styles.value}>${profile?.total_revenue ?? 0}</div>
        </div>
      </Card>

      {/* Reviews */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="review" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Total Reviews</div>
          <div className={styles.value}>{profile?.total_reviews ?? 0}</div>
        </div>
      </Card>

      {/* Average Rating */}
      <Card className={styles.cardRating}>
        <div className={styles.chart}>
          <div className={styles.label}>Average Rating</div>
          <CakeChart value={profile?.average_rating ?? 0} max={5} />
        </div>
      </Card>
    </>
  );
}

export default AdminDashboard;
