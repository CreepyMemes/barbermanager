import { useAuth } from '@hooks/useAuth';
import styles from './ClientDashboard.module.scss';
import Card from '@components/common/Card/Card';
import Icon from '@components/common/Icon/Icon';
import CakeChart from '@components/common/CakeChart/CakeChart';

function ClientDashboard() {
  const { profile } = useAuth();
  const appointments = profile?.appointments ?? [];
  const reviews = profile?.reviews ?? [];

  // Completed and future appointments
  const futureAppointments = appointments.filter((a) => new Date(a.date) >= new Date());
  const completedAppointments = appointments.filter((a) => a.status === 'COMPLETED');

  // Last appointment
  const lastAppointment = appointments.length
    ? appointments.slice().sort((a, b) => new Date(b.date) - new Date(a.date))[0]
    : null;

  // Average rating (from client's reviews)
  const averageRating = reviews.length ? reviews.reduce((s, r) => s + r.rating, 0) / reviews.length : 0;

  return (
    <>
      {/* Appointment Count */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="appointment" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Total Appointments</div>
          <div className={styles.value}>{appointments.length}</div>
        </div>
      </Card>

      {/* Next Appointment */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="calendar" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Next Appointment</div>
          {futureAppointments.length > 0 ? (
            <div className={styles.nextAppointment}>
              <span className={styles.nextAppointmentDate}>
                {futureAppointments.sort((a, b) => new Date(a.date) - new Date(b.date))[0].date}
              </span>
              <span className={styles.nextAppointmentSlot}>
                {futureAppointments.sort((a, b) => new Date(a.date) - new Date(b.date))[0].slot}
              </span>
            </div>
          ) : (
            <div className={styles.empty}>No future appointment</div>
          )}
        </div>
      </Card>

      {/* Last Review */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="review" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Last Review</div>
          {reviews.length > 0 ? (
            <div className={styles.lastReview}>
              <span className={styles.stars}>
                {'★'.repeat(reviews[0].rating)}
                {'☆'.repeat(5 - reviews[0].rating)}
              </span>
              <span className={styles.reviewComment}>
                {reviews[0].comment?.length > 24 ? reviews[0].comment.slice(0, 24) + '…' : reviews[0].comment}
              </span>
              <span className={styles.reviewDate}>{reviews[0].created_at}</span>
            </div>
          ) : (
            <div className={styles.empty}>No reviews yet</div>
          )}
        </div>
      </Card>

      {/* Most Recent Appointment */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="availability" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Last Appointment</div>
          {lastAppointment ? (
            <div className={styles.lastAppointment}>
              <span className={styles.lastAppointmentDate}>{lastAppointment.date}</span>
              <span className={styles.lastAppointmentSlot}>{lastAppointment.slot}</span>
              <span className={styles.lastAppointmentStatus}>{lastAppointment.status}</span>
            </div>
          ) : (
            <div className={styles.empty}>No appointments</div>
          )}
        </div>
      </Card>

      {/* Average Rating (as reviewer) */}
      <Card className={styles.cardRating}>
        <div className={styles.chart}>
          <div className={styles.label}>Your Average Review</div>
          <CakeChart value={averageRating} max={5} />
        </div>
      </Card>
    </>
  );
}

export default ClientDashboard;
