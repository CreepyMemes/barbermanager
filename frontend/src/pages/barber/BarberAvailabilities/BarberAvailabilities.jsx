import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './BarberAvailabilities.module.scss';
import api from '@api';

import Pagination from '@components/common/Pagination/Pagination';
import Icon from '@components/common/Icon/Icon';
import Button from '@components/common/Button/Button';
import Spinner from '@components/common/Spinner/Spinner';

function BarberAvailabilities() {
  const { profile } = useAuth();
  const [availabilities, setAvailabilities] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Defines fetching all availabilities from api (single responsibility, outside effect)
   */
  const fetchAvailabilities = useCallback(async () => {
    setIsLoading(true);

    try {
      const { availabilities } = await api.barber.getBarberAvailabilities();
      setAvailabilities(availabilities);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Only fetch if profile is loaded AND user is admin
   */
  useEffect(() => {
    if (profile?.role === 'BARBER') {
      fetchAvailabilities();
    }
  }, [profile, fetchAvailabilities]);

  // Only render UI for admins; otherwise, render nothing
  if (!profile || profile.role !== 'BARBER') return null;

  return (
    <Pagination
      className={styles.barberAvailabilities}
      icon="availability"
      label="Availabilities"
      itemsPerPage={5}
      loading={isLoading}
      emptyMessage="No availabilities found." //
    >
      <Pagination.Action>
        <div className={styles.action}>
          <Button
            className={styles.refreshBtn}
            type="button"
            color="primary"
            size="md"
            onClick={fetchAvailabilities}
            disabled={isLoading} //
          >
            <span className={styles.line}>
              {isLoading ? (
                <>
                  <Spinner size="sm" /> Refreshing...
                </>
              ) : (
                <>
                  <Icon name="refresh" size="ty" /> Refresh availabilities
                </>
              )}
            </span>
          </Button>
        </div>
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
      {availabilities.map((availability) => (
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
  );
}

export default BarberAvailabilities;
