import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './BarberReviews.module.scss';
import api from '@api';

import Pagination from '@components/common/Pagination/Pagination';
import Icon from '@components/common/Icon/Icon';
import Rating from '@components/ui/Rating/Rating';
import Button from '@components/common/Button/Button';
import Spinner from '@components/common/Spinner/Spinner';
import Profile from '@components/ui/Profile/Profile';

function BarberReviews() {
  const { profile } = useAuth();
  const [reviews, setReviews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const [clients, setClients] = useState({}); // clientId -> profile

  /**
   * Defines fetching all reviews from api (single responsibility, outside effect)
   */
  const fetchReviews = useCallback(async () => {
    setIsLoading(true);

    try {
      const result = await api.barber.getBarberReviews();
      setReviews(result.reviews || []);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Defines fetching all client profiles needed (only unique client IDs)
   */
  const fetchClientProfiles = useCallback(async (reviews) => {
    // Gets all unique client IDs from reviews
    const clientIds = [...new Set(reviews.map((a) => a.client_id))];

    // fetches all client profiles in parallel
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
   * Only fetch if profile is loaded AND user is admin
   */
  useEffect(() => {
    if (profile?.role === 'BARBER') {
      fetchReviews();
    }
  }, [profile, fetchReviews]);

  /**
   * When reviews change, fetch needed barber profiles
   */
  useEffect(() => {
    if (reviews.length > 0) {
      fetchClientProfiles(reviews);
    }
  }, [reviews, fetchClientProfiles]);

  // Only render UI for admins; otherwise, render nothing
  if (!profile || profile.role !== 'BARBER') return null;

  return (
    <div className={styles.barberReviews}>
      <Pagination
        icon="review"
        label="Reviews"
        itemsPerPage={5}
        loading={isLoading}
        emptyMessage="No reviews yet." //
      >
        <Pagination.Action>
          <div className={styles.action}>
            <Button
              className={styles.refreshBtn}
              type="button"
              color="primary"
              size="md"
              onClick={fetchReviews}
              disabled={isLoading} //
            >
              <span className={styles.line}>
                {isLoading ? (
                  <>
                    <Spinner size="sm" /> Refreshing...
                  </>
                ) : (
                  <>
                    <Icon name="refresh" size="ty" /> Refresh reviews
                  </>
                )}
              </span>
            </Button>
          </div>
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
        {reviews.map((review) => (
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
    </div>
  );
}

export default BarberReviews;
