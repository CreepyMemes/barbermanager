import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './ClientBarbers.module.scss';
import api from '@api';

import Icon from '@components/common/Icon/Icon';
import Pagination from '@components/common/Pagination/Pagination';
import Profile from '@components/ui/Profile/Profile';
import Rating from '@components/ui/Rating/Rating';
import Button from '@components/common/Button/Button';
import Spinner from '@components/common/Spinner/Spinner';

function AdminBarbers() {
  const { profile } = useAuth();
  const [barbers, setBarbers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Defines fetching barbers from api (single responsibility, outside effect)
   */
  const fetchBarbers = useCallback(async () => {
    setIsLoading(true);

    try {
      const { barbers } = await api.pub.getBarbersPublic();
      setBarbers(barbers);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Only fetch if profile is loaded AND user is client
   */
  useEffect(() => {
    if (profile?.role === 'CLIENT') {
      fetchBarbers();
    }
  }, [profile, fetchBarbers]);

  // Only render UI for clients otherwise render nothing
  if (!profile || profile.role !== 'CLIENT') return null;

  return (
    <>
      {/* Registered Barbers Pagination */}
      <Pagination
        className={styles.clientBarbers}
        icon="barber"
        label="Barbers"
        itemsPerPage={5}
        loading={isLoading}
        emptyMessage="No barbers found." //
      >
        <Pagination.Action>
          <div className={styles.action}>
            <Button
              className={styles.refreshBtn}
              type="button"
              color="primary"
              size="md"
              onClick={fetchBarbers}
              disabled={isLoading}
            >
              <span className={styles.line}>
                {isLoading ? (
                  <>
                    <Spinner size={'sm'} /> Refreshing...
                  </>
                ) : (
                  <>
                    <Icon name="refresh" size="ty" /> Refresh barbers
                  </>
                )}
              </span>
            </Button>
          </div>
        </Pagination.Action>

        {/* Table Headers */}
        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="user" size="ty" black />
            <span className={styles.tableTitleName}>User</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="comment" size="ty" black />
            <span className={styles.tableTitleName}>Description</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="review" size="ty" black />
            <span className={styles.tableTitleName}>Rating</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="check" size="ty" black />
            <span className={styles.tableTitleName}>Joined</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="dial" size="ty" black />
            <span className={styles.tableTitleName}>Actions</span>
          </div>
        </Pagination.Column>

        {/* Table Rows */}
        {barbers.map((barber) => (
          <Pagination.Row key={barber.id}>
            <Pagination.Cell>
              <Profile profile={barber} />
            </Pagination.Cell>

            <Pagination.Cell>
              <span className={barber.description ? styles.description : `${styles.description} ${styles.noDescription}`}>
                {barber.description || 'No description'}
              </span>
            </Pagination.Cell>

            <Pagination.Cell>
              <Rating rating={barber.average_rating} />
            </Pagination.Cell>

            <Pagination.Cell>
              <span className={styles.date}>{barber.date_joined.replaceAll('-', ' / ')}</span>
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.actions}>
                <Button
                  type="button"
                  size="sm"
                  color="animated"
                  href={`/client/appointments?bookBarber=${barber.id}`} //
                >
                  <Icon name="calendar" size="sm" black />
                </Button>

                <Button
                  type="button"
                  size="sm"
                  color="animated"
                  href={`/client/reviews?reviewBarber=${barber.id}`} //
                >
                  <Icon name="rating" size="sm" black />
                </Button>
              </div>
            </Pagination.Cell>
          </Pagination.Row>
        ))}
      </Pagination>
    </>
  );
}

export default AdminBarbers;
