import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './ClientDashboard.module.scss';
import api from '@api';

import Icon from '@components/common/Icon/Icon';
import StatCard from '@components/ui/StatCard/StatCard';
import Pagination from '@components/common/Pagination/Pagination';
import Rating from '@components/ui/Rating/Rating';
import Spinner from '@components/common/Spinner/Spinner';
import Profile from '@components/ui/Profile/Profile';

function ClientDashboard() {
  const { profile, setProfile } = useAuth();
  const [isLoading, setIsLoading] = useState(true);

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
   * Defines fetching latest profile data
   */
  const fetchProfile = useCallback(async () => {
    setIsLoading(true);

    try {
      const { profile } = await api.client.getClientProfile();
      setProfile(profile);
    } finally {
      setIsLoading(false);
    }
  }, [setProfile]);

  /**
   *  Fetches on mount to keep profile data always up to date
   */
  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  /**
   *  Only run on reviews change
   */
  useEffect(() => {
    if (profile?.reviews?.length > 0) {
      fetchBarberProfiles(profile.reviews);
    }
  }, [profile?.reviews, fetchBarberProfiles]);

  // While fetching latest profile data show loading spinner
  if (isLoading) return <Spinner />;

  return (
    <div className={styles.clientDashboard}>
      {/* Upcoming Appointment */}
      <StatCard icon="availability" label="Upcoming Appointment">
        {profile.upcoming_appointment ? (
          <div className={styles.upcomingAppointmentValue}>
            <span className={styles.upcomingAppointmentSlot}>{profile.upcoming_appointment?.slot}</span>
            <span className={styles.upcomingAppointmentDate}>{profile.upcoming_appointment?.date.replaceAll('-', ' / ')}</span>
          </div>
        ) : (
          <span className={styles.empty}>No future appointment</span>
        )}
      </StatCard>

      {/* Total Appointments */}
      <StatCard icon="calendar" label="Total Appointments">
        <span className={styles.value}>{profile.total_appointments}</span>
      </StatCard>

      {/* Completed Appointments */}
      <StatCard icon="completed" label="Completed Appointments">
        <span className={styles.value}>{profile.completed_appointments}</span>
      </StatCard>

      {/* Latest Reviews */}
      <Pagination
        icon="review"
        label="Latest Reviews"
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
        {profile.latest_reviews.map((review) => (
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
