import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './BarberDashboard.module.scss';
import api from '@api';

import Icon from '@components/common/Icon/Icon';
import StatCard from '@components/common/StatCard/StatCard';
import Pagination from '@components/common/Pagination/Pagination';
import RadialChart from '@components/common/RadialChart/RadialChart';
import Rating from '@components/common/Rating/Rating';
import Spinner from '@components/common/Spinner/Spinner';
import Profile from '@components/common/Profile/Profile';

function BarberDashboard() {
  const { profile } = useAuth();

  const [clients, setClients] = useState({}); // clientId -> profile

  /**
   * Defines fetching all client profiles needed for reviews (only unique client IDs)
   */
  const fetchClientProfiles = useCallback(async (reviews) => {
    if (!reviews) return;

    const clientIds = [...new Set(reviews.map((r) => r.client_id))];

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

    setClients(Object.fromEntries(entries)); // assembles into { [id]: profile }
  }, []);

  /**
   *  Only run on reviews change
   */
  useEffect(() => {
    if (profile?.reviews?.length > 0) {
      fetchClientProfiles(profile.reviews);
    }
  }, [profile?.reviews, fetchClientProfiles]);

  return (
    <div className={styles.barberDashboard}>
      {/* Total Revenue */}
      <StatCard icon="revenue" label="Total Revenue">
        <span className={styles.value}>{`$${profile.total_revenue}`}</span>
      </StatCard>

      {/* Ongoing Appointments */}
      <StatCard icon="calendar" label="Ongoing Appointments">
        <span className={styles.value}>{profile.ongoing_appointments}</span>
      </StatCard>

      {/* Completed Appointments */}
      <StatCard icon="completed" label="Completed Appointments">
        <span className={styles.value}>{profile.completed_appointments}</span>
      </StatCard>

      {/* Upcoming Availabilities */}
      <Pagination
        icon="availability"
        label="Upcoming Availabilities"
        itemsPerPage={5}
        emptyMessage="No availabilities" //
      >
        <Pagination.Action>
          <div className={styles.action}></div>
        </Pagination.Action>

        {/* Table headers */}
        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="date" size="ty" black />
            <span className={styles.tableTitleName}>Date</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="hourglass" size="ty" black />
            <span className={styles.tableTitleName}>Slots</span>
          </div>
        </Pagination.Column>

        {/* Table rows */}
        {(profile?.availabilities || []).map((availability) => (
          <Pagination.Row key={availability.id}>
            <Pagination.Cell>
              <span className={styles.availabilityDate}>{availability.date.replaceAll('-', ' / ')}</span>
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.availabilitySlots}>
                <span className={styles.slots}>{availability.slots.join(', ')}</span>
              </div>
            </Pagination.Cell>
          </Pagination.Row>
        ))}
      </Pagination>

      {/* Services */}
      <Pagination
        icon="service"
        label="Services"
        itemsPerPage={5}
        emptyMessage="No services" //
      >
        <Pagination.Action>
          <div className={styles.action}></div>
        </Pagination.Action>

        {/* Table headers */}
        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="scissors" size="ty" black />
            <span className={styles.tableTitleName}>Name</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="revenue" size="ty" black />
            <span className={styles.tableTitleName}>Price</span>
          </div>
        </Pagination.Column>

        {/* Table rows */}
        {profile?.services?.map((service) => (
          <Pagination.Row key={service.id}>
            <Pagination.Cell>
              <span className={styles.serviceName}>{service.name}</span>
            </Pagination.Cell>

            <Pagination.Cell>
              <span className={styles.servicePrice}>${service.price}</span>
            </Pagination.Cell>
          </Pagination.Row>
        ))}
      </Pagination>

      {/* Received Reviews */}
      <Pagination
        icon="review"
        label="Received Reviews"
        itemsPerPage={5}
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
        {profile.reviews.map((review) => (
          <Pagination.Row key={review.id}>
            <Pagination.Cell>
              {clients[review.client_id] ? <Profile profile={clients[review.client_id]} /> : <Spinner size="sm" />}
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

      {/* Average Rating */}
      <StatCard icon="rating" label="Average Rating">
        <span className={styles.value}>
          <RadialChart value={profile.average_rating} max={5} size="70" />
        </span>
      </StatCard>
    </div>
  );
}

export default BarberDashboard;
