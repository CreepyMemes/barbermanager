import { useAuth } from '@hooks/useAuth';
import styles from './ClientDashboard.module.scss';

import StatCard from '@components/common/StatCard/StatCard';
import Pagination from '@components/common/Pagination/Pagination';
import Rating from '@components/common/Rating/Rating';

function ClientDashboard() {
  const { profile } = useAuth();

  return (
    <div className={styles.clientDashboard}>
      {/* Next Appointment */}
      <Pagination icon="availability" label="Next Appointment" emptyMessage="No future appointment">
        <div className={styles.nextAppointmentValue}>
          <span className={styles.nextAppointmentSlot}>{profile.next_appointment.slot}</span>
          <span className={styles.nextAppointmentDate}>{profile.next_appointment.date.replaceAll('-', ' / ')}</span>
        </div>
      </Pagination>

      {/* Total Appointments */}
      <StatCard icon="calendar" label="Total Appointments">
        <span className={styles.value}>{profile?.appointments?.length}</span>
      </StatCard>

      {/* Completed Appointments */}
      <StatCard icon="completed" label="Completed Appointments">
        <span className={styles.value}>{profile.completed_appointments}</span>
      </StatCard>

      {/* Booked Appointments */}
      <Pagination icon="appointment" label="Booked Appointments" emptyMessage="No appointments">
        {profile?.appointments?.map((appointment) => (
          <div key={appointment.id} className={styles.appointmentRow}>
            <span className={styles.appointmentDate}>{appointment.date}</span>
            <span className={styles.appointmentSlot}>{appointment.slot}</span>
            <span className={styles.appointmentStatus}>{appointment.status}</span>
          </div>
        ))}
      </Pagination>

      {/* Posted Reviews */}
      <Pagination icon="review" label="Posted Reviews" emptyMessage="No reviews yet">
        {profile?.reviews?.map((review) => (
          <div key={review.id} className={styles.reviewRow}>
            <Rating rating={review.rating} />

            <span className={styles.reviewComment}>
              {review.comment?.length > 30 ? review.comment.slice(0, 30) + '…' : review.comment}
            </span>
            <span className={styles.reviewDate}>{review.created_at}</span>
          </div>
        ))}
      </Pagination>
    </div>
  );
}

export default ClientDashboard;
