import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './AdminDashboard.module.scss';
import api from '@api';

import Spinner from '@components/common/Spinner/Spinner';
import StatCard from '@components/ui/StatCard/StatCard';
import RadialChart from '@components/ui/RadialChart/RadialChart';

function AdminDashboard() {
  const { profile, setProfile } = useAuth();
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Defines fetching latest profile data
   */
  const fetchProfile = useCallback(async () => {
    setIsLoading(true);

    try {
      const { profile } = await api.admin.getAdminProfile();
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

  // While fetching latest profile data show loading spinner
  if (isLoading) return <Spinner />;

  return (
    <div className={styles.adminDashboard}>
      {/* Revenue */}
      <StatCard icon="revenue" label="Total Revenue">
        <span className={styles.value}>{`$${profile.total_revenue}`}</span>
      </StatCard>

      {/* Total Barbers */}
      <StatCard icon="barber" label="Total Barbers">
        <span className={styles.value}>{profile.total_barbers} </span>
      </StatCard>

      {/* Total Appointments */}
      <StatCard icon="appointment" label="Total Appointments">
        <span className={styles.value}>{profile.total_appointments} </span>
      </StatCard>

      {/* Completed Appointments */}
      <StatCard icon="completed" label="Completed Appointments">
        <span className={styles.value}>{profile.completed_appointments} </span>
      </StatCard>

      {/* Ongoing Appointments */}
      <StatCard icon="calendar" label="Ongoing Appointments">
        <span className={styles.value}> {profile.ongoing_appointments} </span>
      </StatCard>

      {/* Cancelled Appointments */}
      <StatCard icon="cancelled" label="Cancelled Appointments">
        <span className={styles.value}> {profile.cancelled_appointments} </span>
      </StatCard>

      {/* Total Clients */}
      <StatCard icon="client" label="Total Clients">
        <span className={styles.value}> {profile.total_clients} </span>
      </StatCard>

      {/* Total Reviews */}
      <StatCard icon="review" label="Total Reviews">
        <span className={styles.value}> {profile.total_reviews} </span>
      </StatCard>

      {/* Average Rating */}
      <StatCard icon="rating" label="Average Rating">
        <span className={styles.value}>
          <RadialChart value={profile.average_rating} max={5} size="70" />
        </span>
      </StatCard>
    </div>
  );
}

export default AdminDashboard;
