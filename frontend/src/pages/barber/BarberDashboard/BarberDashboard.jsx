import { useAuth } from '@hooks/useAuth';
import styles from './BarberDashboard.module.scss';

import StatCard from '@components/common/StatCard/StatCard';
import Pagination from '@components/common/Pagination/Pagination';
import RadialChart from '@components/common/RadialChart/RadialChart';

function BarberDashboard() {
  const { profile } = useAuth();

  return (
    <div className={styles.barberDashboard}>
      {/* Total Revenue */}
      <StatCard icon="revenue" label="Total Revenue" value={`$${profile.total_revenue}`} />

      {/* Completed Appointments */}
      <StatCard icon="completed" label="Completed Appointments" value={profile.completed_appointments} />

      {/* Services */}
      <Pagination icon="service" label="Services" emptyMessage="No services">
        {profile?.services?.map((service) => (
          <div key={service.id} className={styles.serviceRow}>
            <span className={styles.serviceName}>{service.name}</span>
            <span className={styles.servicePrice}>${service.price}</span>
          </div>
        ))}
      </Pagination>

      {/* Upcoming Availabilities */}
      <Pagination icon="availability" label="Upcoming Availabilities" emptyMessage="No availabilities">
        {profile?.availabilities?.map((availability) => (
          <div key={availability.id} className={styles.availabilityRow}>
            <span className={styles.availabilityDate}>{availability.date}</span>
            <span className={styles.availabilitySlots}>{availability.slots.join(', ')}</span>
          </div>
        ))}
      </Pagination>

      {/* Ongoing Appointments */}
      <Pagination icon="calendar" label="Ongoing Appointments" emptyMessage="No appointments">
        {profile.ongoing_appointments?.map((appointment) => (
          <div key={appointment.id} className={styles.appointmentRow}>
            <span className={styles.appointmentDate}>{appointment.date}</span>
            <span className={styles.appointmentSlot}>{appointment.slot}</span>
          </div>
        ))}
      </Pagination>

      {/* Received Reviews */}
      <Pagination icon="review" label="Received Reviews" emptyMessage="No reviews yet">
        {profile?.reviews?.map((review) => (
          <div key={review.id} className={styles.reviewRow}>
            <span className={styles.stars}>
              {'★'.repeat(review.rating)}
              {'☆'.repeat(5 - review.rating)}
            </span>
            <span className={styles.reviewComment}>
              {review.comment?.length > 30 ? review.comment.slice(0, 30) + '…' : review.comment}
            </span>
            <span className={styles.reviewDate}>{review.created_at}</span>
          </div>
        ))}
      </Pagination>

      {/* Average Rating */}
      <StatCard icon="rating" label="Average Rating">
        <RadialChart value={profile.average_rating} max={5} size="70" />
      </StatCard>
    </div>
  );
}
export default BarberDashboard;
