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

  const [isLoadingProfile, setIsLoadingProfile] = useState(true);
  const [isLoadingBarberProfiles, setIsLoadingBarberProfiles] = useState(true);

  const [barbers, setBarbers] = useState({}); // barberId -> profile

  /**
   * Defines fetching all barber profiles needed for reviews  and appointments (only unique barber IDs)
   */
  const fetchBarberProfiles = useCallback(
    async (latest_reviews = [], recent_appointments = []) => {
      setIsLoadingBarberProfiles(true);

      try {
        const reviewBarberIds = (latest_reviews || []).map((r) => r.barber_id); // Get barbers from reviews
        const appointmentBarberIds = (recent_appointments || []).map((a) => a.barber_id); // Get barbers from appointments
        const allBarberIds = Array.from(new Set([...reviewBarberIds, ...appointmentBarberIds])); // Combine both

        // Only fetch the barbers that aren't in our barbers cache yet
        const barberIdsToFetch = allBarberIds.filter((id) => !(id in barbers));

        if (barberIdsToFetch.length === 0) {
          setIsLoadingBarberProfiles(false);
          return;
        }

        const entries = await Promise.all(
          barberIdsToFetch.map(async (id) => {
            try {
              const { profile } = await api.pub.getBarberProfilePublic(id);
              return [id, profile];
            } catch {
              return [id, null];
            }
          }),
        );

        setBarbers((prev) => ({ ...prev, ...Object.fromEntries(entries) })); // includes barbers in deps to always know which barber ids are loaded
      } finally {
        setIsLoadingBarberProfiles(false);
      }
    },
    [barbers],
  );

  /**
   * Defines fetching latest profile data
   */
  const fetchProfile = useCallback(async () => {
    setIsLoadingProfile(true);

    try {
      const { profile } = await api.client.getClientProfile();
      setProfile(profile);
    } finally {
      setIsLoadingProfile(false);
    }
  }, [setProfile]);

  /**
   *  Fetches on mount to keep profile data always up to date
   */
  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  /**
   * Only run when reviews or recent appointments change
   */
  useEffect(() => {
    if (profile?.latest_reviews || profile?.recent_appointments) {
      fetchBarberProfiles(profile?.latest_reviews, profile?.recent_appointments);
    }
  }, [profile?.latest_reviews, profile?.recent_appointments, fetchBarberProfiles]);

  // While fetching latest profile data show loading spinner
  if (isLoadingProfile) return <Spinner />;

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

      {/* Recent Appointments */}
      <Pagination
        icon="date"
        label="Recent Appointments"
        itemsPerPage={5}
        emptyMessage="No appointments found." //
      >
        <Pagination.Action>
          <div className={styles.action}></div>
        </Pagination.Action>

        {/* Table headers */}
        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="client" size="ty" black />
            <span className={styles.tableTitleName}>Barber</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="calendar" size="ty" black />
            <span className={styles.tableTitleName}>Date</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="revenue" size="ty" black />
            <span className={styles.tableTitleName}>Spent</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="service" size="ty" black />
            <span className={styles.tableTitleName}>Services</span>
          </div>
        </Pagination.Column>

        {/* Table rows */}
        {profile.recent_appointments.map((appointment) => (
          <Pagination.Row key={appointment.id}>
            <Pagination.Cell>
              <Profile profile={barbers[appointment.barber_id]} loading={isLoadingBarberProfiles} />
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.dateContainer}>
                <div className={styles.date}>
                  <span className={styles.date}>{appointment.date.replaceAll('-', ' / ')}</span>
                  <span className={styles.slot}>( {appointment.slot} )</span>
                </div>
              </div>
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.amountSpent}>
                <span className={styles.amount}>${appointment.amount_spent}</span>
              </div>
            </Pagination.Cell>

            <Pagination.Cell>
              <span className={styles.services}>{appointment.services.map((service) => service.name).join(', ')}</span>
            </Pagination.Cell>
          </Pagination.Row>
        ))}
      </Pagination>

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
              <Profile profile={barbers[review.barber_id]} loading={isLoadingBarberProfiles} />
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
