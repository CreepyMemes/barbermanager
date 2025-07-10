import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './AdminBarbers.module.scss';

import api from '@api';
import Pagination from '@components/common/Pagination/Pagination';
import Spinner from '@components/common/Spinner/Spinner';

function AdminBarbers() {
  const { profile } = useAuth();
  const [barbers, setBarbers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Define fetchBarbers (single responsibility, outside effect)
   */
  const fetchBarbers = useCallback(async () => {
    setIsLoading(true);
    try {
      const result = await api.admin.getAllBarbers();
      setBarbers(result.barbers || []);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Only fetch if profile is loaded AND user is admin
   */
  useEffect(() => {
    if (profile && profile.role === 'ADMIN') {
      fetchBarbers();
    }
  }, [profile, fetchBarbers]);

  // Only render UI for admins; otherwise, render nothing
  if (!profile || profile?.role !== 'ADMIN') return null;

  return (
    <div className={styles.adminBarbers}>
      <Pagination icon="barber" label="Registered Barbers" emptyMessage="No barbers found.">
        {isLoading ? (
          <Spinner />
        ) : (
          barbers.map((barber) => (
            <div key={barber.id} className={styles.barberRow}>
              <div className={styles.header}>
                <span className={styles.barberName}>
                  {barber.name || barber.username || barber.email}
                  {!barber.is_active && (
                    <span className={styles.inactive} title="Inactive">
                      (inactive)
                    </span>
                  )}
                </span>
                <span className={styles.barberRating}>
                  {'★'.repeat(barber.average_rating)}
                  {'☆'.repeat(5 - barber.average_rating)}
                  {barber.average_rating > 0 && <span className={styles.ratingValue}> {barber.average_rating}/5</span>}
                </span>
              </div>
              <div className={styles.details}>
                <span className={styles.email}>{barber.email}</span>
                <span className={styles.revenue}>
                  Revenue: <span className={styles.revenueValue}>€{barber.total_revenue.toFixed(2)}</span>
                </span>
                <span className={styles.completed}>Completed: {barber.completed_appointments}</span>
              </div>
              <div className={styles.services}>
                <span className={styles.servicesLabel}>Services:</span>
                {barber.services.length ? (
                  <span className={styles.servicesList}>{barber.services.map((srv) => srv.name).join(', ')}</span>
                ) : (
                  <span className={styles.servicesNone}>None</span>
                )}
              </div>
            </div>
          ))
        )}
      </Pagination>
    </div>
  );
}

export default AdminBarbers;
