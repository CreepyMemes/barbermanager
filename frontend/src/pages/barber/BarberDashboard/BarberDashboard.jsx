import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './BarberDashboard.module.scss';
import api from '@api';

import Icon from '@components/common/Icon/Icon';
import StatCard from '@components/ui/StatCard/StatCard';
import Pagination from '@components/common/Pagination/Pagination';
import RadialChart from '@components/ui/RadialChart/RadialChart';
import Rating from '@components/ui/Rating/Rating';
import Spinner from '@components/common/Spinner/Spinner';
import Profile from '@components/ui/Profile/Profile';

function BarberDashboard() {
  const { profile, setProfile } = useAuth();

  const [isLoadingProfile, setIsLoadingProfile] = useState(true);
  const [isLoadingClientProfiles, setIsLoadingClientProfiles] = useState(true);

  const [clients, setClients] = useState({}); // clientId -> profile

  /**
   * Defines fetching all client profiles needed for reviews and appointments (only unique client IDs)
   */
  const fetchClientProfiles = useCallback(
    async (reviews = [], upcoming_appointments = []) => {
      setIsLoadingClientProfiles(true);

      try {
        const reviewClientIds = (reviews || []).map((r) => r.client_id); // Get clients from reviews
        const appointmentClientIds = (upcoming_appointments || []).map((a) => a.client_id); // Get clients from appointments
        const allClientIds = Array.from(new Set([...reviewClientIds, ...appointmentClientIds])); // Combine both
        const clientIds = allClientIds.filter((id) => !(id in clients)); // Only get those not already in our clients cache

        if (clientIds.length === 0) return;

        const entries = await Promise.all(
          clientIds.map(async (id) => {
            try {
              const { profile } = await api.pub.getClientProfilePublic(id);
              return [id, profile];
            } catch {
              return [id, null];
            }
          }),
        );

        setClients((prev) => ({ ...prev, ...Object.fromEntries(entries) })); // includes clients in deps to always know which client ids are loaded
      } finally {
        setIsLoadingClientProfiles(false);
      }
    },
    [clients],
  );

  /**
   * Defines fetching latest profile data
   */
  const fetchProfile = useCallback(async () => {
    setIsLoadingProfile(true);

    try {
      const { profile } = await api.barber.getBarberProfile();
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
   *  Only run when reviews or appointments change
   */
  useEffect(() => {
    if (profile?.reviews || profile?.upcoming_appointments) {
      fetchClientProfiles(profile?.reviews, profile?.upcoming_appointments);
    }
  }, [profile?.reviews, profile?.upcoming_appointments, fetchClientProfiles]);

  // While fetching latest profile data show loading spinner
  if (isLoadingProfile) return <Spinner />;

  return (
    <div className={styles.barberDashboard}>
      {/* Total Revenue */}
      <StatCard icon="revenue" label="Total Revenue">
        <span className={styles.value}>{`$${profile.total_revenue}`}</span>
      </StatCard>

      {/* Completed Appointments */}
      <StatCard icon="completed" label="Completed Appointments">
        <span className={styles.value}>{profile.completed_appointments}</span>
      </StatCard>

      {/* Average Rating */}
      <StatCard icon="rating" label="Average Rating">
        <span className={styles.value}>
          <RadialChart value={profile.average_rating} max={5} size="70" />
        </span>
      </StatCard>

      {/* Upcoming Appointments */}
      <Pagination
        icon="date"
        label="Upcoming Appointments"
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
            <span className={styles.tableTitleName}>Client</span>
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
        {profile.upcoming_appointments.map((appointment) => (
          <Pagination.Row key={appointment.id}>
            <Pagination.Cell>
              <Profile profile={clients[appointment.client_id]} loading={isLoadingClientProfiles} />
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
        itemsPerPage={3}
        emptyMessage="No reviews yet" //
      >
        <Pagination.Action>
          <div className={styles.action}></div>
        </Pagination.Action>

        {/* Table headers */}
        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="client" size="ty" black />
            <span className={styles.tableTitleName}>Client</span>
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
              <Profile profile={clients[review.client_id]} loading={isLoadingClientProfiles} />
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

export default BarberDashboard;
