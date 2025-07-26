import { useEffect, useState, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import styles from './AdminAvailabilities.module.scss';
import api from '@api';

import Icon from '@components/common/Icon/Icon';
import Pagination from '@components/common/Pagination/Pagination';
import Hero from '@components/ui/Hero/Hero';
import Card from '@components/common/Card/Card';
import Button from '@components/common/Button/Button';
import StatCard from '@components/ui/StatCard/StatCard';
import Profile from '@components/ui/Profile/Profile';
// import Modal from '@components/common/Modal/Modal';
// import Input from '@components/common/Input/Input';
import Spinner from '@components/common/Spinner/Spinner';

function AdminAvailabilities() {
  const { profile } = useAuth();
  const { barberId } = useParams();

  const [barberProfile, setBarberProfile] = useState(null);
  const [availabilities, setAvailabilities] = useState([]);

  const [status, setStatus] = useState('pending');
  const [message, setMessage] = useState('');

  const [isLoadingBarberProfile, setIsLoadingBarberProfile] = useState(true);
  const [isLoadingAvailabilities, setIsLoadingAvailabilities] = useState(true);

  /**
   * Defines fetching barbers from api (single responsibility, outside effect)
   */
  const fetchBarberProfile = useCallback(async () => {
    setIsLoadingBarberProfile(true);

    try {
      const { profile } = await api.pub.getBarberProfilePublic(barberId);
      setBarberProfile(profile);
    } finally {
      setIsLoadingBarberProfile(false);
    }
  }, [barberId]);

  /**
   * Defines fetching all availabilities from api (single responsibility, outside effect)
   */
  const fetchAvailabilities = useCallback(async () => {
    setIsLoadingAvailabilities(true);

    try {
      const { availabilities } = await api.pub.getBarberAvailabilitiesPublic(barberId);
      setAvailabilities(availabilities);
    } finally {
      setIsLoadingAvailabilities(false);
    }
  }, [barberId]);

  /**
   * Calls backend API to get the barber profile and availabilities with the provided barber ID
   * Updates component status and message based on response.
   */
  const hydrateBarberData = useCallback(async () => {
    setStatus('pending');

    try {
      await fetchBarberProfile();
      await fetchAvailabilities();
      setStatus('success');
    } catch (error) {
      setMessage(error?.response?.data?.detail || 'The provided Barber ID parameter is invalid.');
      setStatus('error');
    }
  }, [fetchBarberProfile, fetchAvailabilities]);

  /**
   * Only fetch if profile is loaded AND user is admin,
   * then handles fetching the barber profile and availabilities from passed barber ID on mount or when params change.
   */
  useEffect(() => {
    if (profile?.role === 'ADMIN') {
      if (!barberId) {
        setStatus('error');
        setMessage('No barber ID was provided.');
        return;
      }

      hydrateBarberData();
    }
  }, [profile, barberId, hydrateBarberData]);

  // Only render UI for admins; otherwise, render nothing
  if (!profile || profile.role !== 'ADMIN') return null;

  return (
    <div className={styles.adminAvailabilities}>
      {status === 'success' && (
        <>
          <StatCard icon="barber" label="Barber">
            <Profile
              className={styles.profileSection}
              profile={barberProfile}
              imageSize="10rem"
              fontSize="2rem"
              loading={isLoadingBarberProfile} //
            />
          </StatCard>

          {/* Barber Availabilities Pagination */}
          <Pagination
            icon="availability"
            label="Availabilities"
            itemsPerPage={5}
            loading={isLoadingAvailabilities}
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
                  disabled={isLoadingAvailabilities} //
                >
                  <span className={styles.line}>
                    {isLoadingAvailabilities ? (
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
        </>
      )}

      {status === 'pending' && (
        <Card className={styles.error}>
          <Spinner size="lg" />
          <span className={styles.title}>Retreiving the selected barber&apos;s availabilities...</span>
        </Card>
      )}

      {status === 'error' && (
        <Card className={styles.error}>
          <Icon name="cancelled" size="md" black />
          <span className={styles.title}>Barber Error</span>
          <div className={styles.message}>{message}</div>

          <Button href="/admin/barbers" color="primary" size="md">
            Back to Barbers
          </Button>
        </Card>
      )}
    </div>
  );
}

export default AdminAvailabilities;
