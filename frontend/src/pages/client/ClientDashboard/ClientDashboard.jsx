import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './ClientDashboard.module.scss';
import api from '@api';

import Icon from '@components/common/Icon/Icon';
import StatCard from '@components/common/StatCard/StatCard';
import Pagination from '@components/common/Pagination/Pagination';
import Rating from '@components/common/Rating/Rating';
import Spinner from '@components/common/Spinner/Spinner';
import Profile from '@components/common/Profile/Profile';

function ClientDashboard() {
  const { profile } = useAuth();

  const [barbers, setBarbers] = useState({}); // barberId -> profile

  /**
   * Defines fetching all barber profiles needed for reviews (only unique barber IDs)
   */
  const fetchBarberProfiles = useCallback(async (reviews) => {
    if (!reviews) return;

    const barberIds = [...new Set(reviews.map((r) => r.barber_id))];

    const entries = await Promise.all(
      barberIds.map(async (id) => {
        try {
          const { profile } = await api.pub.getBarberProfilePublic(id);
          return [id, profile];
        } catch {
          return [id, null];
        }
      }),
    );

    setBarbers(Object.fromEntries(entries)); // assembles into { [id]: profile }
  }, []);

  /**
   *  Only run on reviews change
   */
  useEffect(() => {
    if (profile?.reviews?.length > 0) {
      fetchBarberProfiles(profile.reviews);
    }
  }, [profile?.reviews, fetchBarberProfiles]);

  return (
    <div className={styles.clientDashboard}>
      {/* Next Appointment */}
      <StatCard icon="availability" label="Next Appointment" emptyMessage="No future appointment">
        <div className={styles.nextAppointmentValue}>
          <span className={styles.nextAppointmentSlot}>{profile.next_appointment.slot}</span>
          <span className={styles.nextAppointmentDate}>{profile.next_appointment.date.replaceAll('-', ' / ')}</span>
        </div>
      </StatCard>

      {/* Total Appointments */}
      <StatCard icon="calendar" label="Total Appointments">
        <span className={styles.value}>{profile?.appointments?.length}</span>
      </StatCard>

      {/* Completed Appointments */}
      <StatCard icon="completed" label="Completed Appointments">
        <span className={styles.value}>{profile.completed_appointments}</span>
      </StatCard>

      {/* Posted Reviews */}
      <Pagination
        icon="review"
        label="Posted Reviews"
        itemsPerPage={5}
        emptyMessage="No reviews yet" //
      >
        <Pagination.Action>
          <div className={styles.action}></div>
        </Pagination.Action>

        {/* Table headers */}
        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="barber" size="ty" black />
            <span className={styles.tableTitleName}>Barber</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="rating" size="ty" black />
            <span className={styles.tableTitleName}>Rating</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="comment" size="ty" black />
            <span className={styles.tableTitleName}>Comment</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="date" size="ty" black />
            <span className={styles.tableTitleName}>Date</span>
          </div>
        </Pagination.Column>

        {/* Table rows */}
        {profile.reviews.map((review) => (
          <Pagination.Row key={review.id}>
            <Pagination.Cell>
              {barbers[review.barber_id] ? <Profile profile={barbers[review.barber_id]} /> : <Spinner size="sm" />}
            </Pagination.Cell>

            <Pagination.Cell>
              <Rating rating={review.rating} />
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.reviewComment}>
                <span className={styles.comment}>{review.comment}</span>
              </div>
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.reviewDate}>
                <span className={styles.date}>{review.created_at.replaceAll('-', ' / ')}</span>
              </div>
            </Pagination.Cell>
          </Pagination.Row>
        ))}
      </Pagination>
    </div>
  );
}

export default ClientDashboard;
