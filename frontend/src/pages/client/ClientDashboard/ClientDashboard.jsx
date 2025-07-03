import { useAuth } from '@hooks/useAuth';
import styles from './ClientDashboard.module.scss';
import Card from '@components/common/Card/Card';
import Icon from '@components/common/Icon/Icon';

function ClientDashboard() {
  const { profile } = useAuth();

  return (
    <>
      {/* Next Appointment */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="availability" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Next Appointment</div>
          {profile.next_appointment ? (
            <div className={styles.value}>
              <span>{profile.next_appointment.date.replaceAll('-', ' / ')}</span>
              <span>{profile.next_appointment.slot}</span>
            </div>
          ) : (
            <div className={styles.empty}>No future appointment</div>
          )}
        </div>
      </Card>

      {/* Total Appointment */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="calendar" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Total Appointments</div>
          <div className={styles.value}>{profile?.appointments?.length}</div>
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

      {/* Booked Appointments */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="appointment" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Booked Appointments</div>
          <ul className={styles.list}>
            {profile?.appointments?.length > 0 ? (
              profile.appointments.map((appointment) => (
                <li className={styles.listItem} key={appointment.id}>
                  <span className={styles.appointmentDate}>{appointment.date}</span>
                  <span className={styles.appointmentSlot}>{appointment.slot}</span>
                  <span className={styles.appointmentStatus}>{appointment.status}</span>
                </li>
              ))
            ) : (
              <div className={styles.empty}>No appointments</div>
            )}
          </ul>
        </div>
      </Card>

      {/* Reviews */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="review" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Posted Reviews</div>
          <ul className={styles.list}>
            {profile?.reviews?.length > 0 ? (
              profile.reviews.slice(0, 3).map((review) => (
                <li className={styles.listItem} key={review.id}>
                  <span className={styles.stars}>
                    {'★'.repeat(review.rating)}
                    {'☆'.repeat(5 - review.rating)}
                  </span>
                  <span className={styles.reviewComment}>
                    {review.comment?.length > 30 ? review.comment.slice(0, 30) + '…' : review.comment}
                  </span>
                  <span className={styles.reviewDate}>{review.created_at}</span>
                </li>
              ))
            ) : (
              <li className={styles.empty}>No reviews yet</li>
            )}
          </ul>
        </div>
      </Card>
    </>
  );
}

export default ClientDashboard;
