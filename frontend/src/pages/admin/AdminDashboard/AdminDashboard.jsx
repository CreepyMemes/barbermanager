import { useAuth } from '@hooks/useAuth';
import styles from './AdminDashboard.module.scss';
import Card from '@components/common/Card/Card';
import Icon from '@components/common/Icon/Icon';
import RadialChart from '@components/common/RadialChart/RadialChart';

function AdminDashboard() {
  const { profile } = useAuth();

  return (
    <>
      {/* Revenue */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="revenue" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Total Revenue</div>
          <div className={styles.value}>${profile.total_revenue}</div>
        </div>
      </Card>

      {/* Barbers */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="barber" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Total Barbers</div>
          <div className={styles.value}>{profile.total_barbers}</div>
        </div>
      </Card>

      {/* Appointments */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="appointment" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Total Appointments</div>
          <div className={styles.value}>{profile.total_appointments}</div>
        </div>
      </Card>

      {/* Completed Appointments */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="completed" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Completed Appointments</div>
          <div className={styles.value}>{profile.completed_appointments}</div>
        </div>
      </Card>

      {/* Ongoing Appointments */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="calendar" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Ongoing Appointments</div>
          <div className={styles.value}>{profile.ongoing_appointments}</div>
        </div>
      </Card>

      {/* Cancelled Appointments */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="cancelled" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Cancelled Appointments</div>
          <div className={styles.value}>{profile.cancelled_appointments}</div>
        </div>
      </Card>

      {/* Clients */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="client" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Total Clients</div>
          <div className={styles.value}>{profile.total_clients}</div>
        </div>
      </Card>

      {/* Reviews */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="review" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Total Reviews</div>
          <div className={styles.value}>{profile.total_reviews}</div>
        </div>
      </Card>

      {/* Average Rating */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="rating" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Average Rating</div>
          <RadialChart value={profile.average_rating} max={5} size="70" />
        </div>
      </Card>
    </>
  );
}

export default AdminDashboard;
