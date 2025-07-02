import { useAuth } from '@hooks/useAuth';
import styles from './BarberDashboard.module.scss';
import Card from '@components/common/Card/Card';
import Icon from '@components/common/Icon/Icon';
import CakeChart from '@components/common/CakeChart/CakeChart';

function BarberDashboard() {
  const { profile } = useAuth();

  return (
    <>
      {/* Services */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="service" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Offered Services</div>
          <ul className={styles.list}>
            {profile?.services?.length > 0 ? (
              profile.services.map((service) => (
                <li className={styles.listItem} key={service.id}>
                  <span className={styles.serviceName}>{service.name}</span>
                  <span className={styles.servicePrice}>${service.price}</span>
                </li>
              ))
            ) : (
              <li className={styles.empty}>No services</li>
            )}
          </ul>
        </div>
      </Card>

      {/* Availabilities */}
      <Card className={styles.card}>
        <div className={styles.icon}>
          <Icon name="availability" size="sm" black />
        </div>
        <div className={styles.content}>
          <div className={styles.label}>Upcoming Availabilities</div>
          <ul className={styles.list}>
            {profile?.availabilities?.length > 0 ? (
              profile.availabilities.slice(0, 3).map((av) => (
                <li className={styles.listItem} key={av.id}>
                  <span className={styles.availabilityDate}>{av.date}</span>
                  <span className={styles.availabilitySlots}>{av.slots.join(', ')}</span>
                </li>
              ))
            ) : (
              <li className={styles.empty}>No availabilities</li>
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
          <div className={styles.label}>Received Reviews</div>
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
export default BarberDashboard;
