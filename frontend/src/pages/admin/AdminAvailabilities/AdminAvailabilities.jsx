import { useEffect, useState, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import { cleanPayload, isAnyFieldSet } from '@utils/utils';
import styles from './AdminAvailabilities.module.scss';
import api from '@api';

import Icon from '@components/common/Icon/Icon';
import Pagination from '@components/common/Pagination/Pagination';
import Card from '@components/common/Card/Card';
import Button from '@components/common/Button/Button';
import StatCard from '@components/ui/StatCard/StatCard';
import Profile from '@components/ui/Profile/Profile';
import Modal from '@components/common/Modal/Modal';
import Input from '@components/common/Input/Input';
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

  // Popup states
  const [createPopup, setCreatePopup] = useState(false);
  const [deletePopup, setDeletePopup] = useState({ open: false, availability: null });
  const [updatePopup, setUpdatePopup] = useState({ open: false, availability: null });

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

  // Create popup state handlers
  const openCreatePopup = () => setCreatePopup(true);
  const closeCreatePopup = () => setCreatePopup(false);

  // Delete popup state handlers
  const openDeletePopup = (availability) => setDeletePopup({ open: true, availability });
  const closeDeletePopup = () => setDeletePopup({ open: false, availability: null });

  // Update popup state handlers
  const openUpdatePopup = (availability) => setUpdatePopup({ open: true, availability });
  const closeUpdatePopup = () => setUpdatePopup({ open: false, availability: null });

  /**
   * Handles cr a new availability
   */
  const handleCreateAvailability = async (
    barberId,
    { start_date, end_date, start_time, end_time, slot_interval, days_of_week },
  ) => {
    await api.admin.createBarberAvailability(barberId, {
      start_date,
      end_date,
      start_time,
      end_time,
      slot_interval,
      days_of_week,
    });
    closeCreatePopup();
    await fetchAvailabilities();
  };

  /**
   * Handles deleting the selected availability
   */
  const handleDeleteAvailability = async (barberId, availabilityId) => {
    await api.admin.deleteBarberAvailability(barberId, availabilityId);
    closeDeletePopup();
    await fetchAvailabilities();
  };

  /**
   * Handles updating the selected availability
   */
  const handleUpdateAvailability = async (barberId, availabilityId, { start_time, end_time, slot_interval }) => {
    await api.admin.updateBarberAvailability(barberId, availabilityId, { start_time, end_time, slot_interval });
    closeUpdatePopup();
    await fetchAvailabilities();
  };

  // Only render UI for admins; otherwise, render nothing
  if (!profile || profile.role !== 'ADMIN') return null;

  return (
    <>
      <div className={styles.adminAvailabilities}>
        {status === 'success' && (
          <>
            {/* Barber Profile Section */}
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

                  <Button
                    className={styles.actionBtn}
                    type="button"
                    color="primary"
                    size="md"
                    onClick={openCreatePopup} //
                  >
                    <Icon name="plus" size="ty" />
                    <span>Create availability</span>
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

              <Pagination.Column>
                <div className={styles.tableTitle}>
                  <Icon name="dial" size="ty" black />
                  <span className={styles.tableTitleName}>Actions</span>
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

                  <Pagination.Cell>
                    <div className={styles.actions}>
                      <Button
                        type="button"
                        size="sm"
                        color="animated"
                        onClick={() => openUpdatePopup(availability)} //
                      >
                        <Icon name="pen" size="ty" black />
                      </Button>

                      <Button
                        type="button"
                        size="sm"
                        color="animated"
                        onClick={() => openDeletePopup(availability)} //
                      >
                        <Icon name="trash" size="ty" black />
                      </Button>
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

      {/* Create Availability Modal */}
      <Modal
        open={createPopup}
        fields={{
          start_date: '',
          end_date: '',
          start_time: '',
          end_time: '',
          slot_interval: '',
          days_of_week: '',
        }}
        action={{ submit: 'Create', loading: 'Creating...' }}
        onValidate={(payload) => isAnyFieldSet(payload, 'Fill at least start date, start-end time to create a new availability.')}
        onSubmit={(payload) => handleCreateAvailability(barberId, cleanPayload(payload))}
        onClose={closeCreatePopup}
      >
        <Modal.Title icon="calendar">Create Availability</Modal.Title>
        <Modal.Description>
          Specify the dates and time range when the barber is available. For a single day, end date is not required. 30min
          interval is default.
        </Modal.Description>

        <Input
          label="Start Date"
          type="date"
          name="start_date"
          required
          size="md" //
        />

        <Input
          label="End Date"
          type="date"
          name="end_date"
          size="md"
          helperText="Optional. Leave blank for a single day." //
        />

        <Input
          label="Start Time"
          type="time"
          name="start_time"
          required
          size="md" //
        />

        <Input
          label="End Time"
          type="time"
          name="end_time"
          required
          size="md" //
        />

        <Input
          label="Slot Interval (minutes)"
          type="number"
          name="slot_interval"
          min="1"
          placeholder="30"
          size="md"
          helperText="Optional. Defaults to 30." //
        />

        <Input
          label="Days of Week (comma-separated, 0=Mon...6=Sun)"
          type="text"
          name="days_of_week"
          placeholder="0,2,4"
          size="md"
          helperText="Optional. Only applies for multiple days." //
        />
      </Modal>

      {/* Delete Availability Modal */}
      <Modal
        open={deletePopup.open}
        action={{ submit: 'Delete', loading: 'Deleting...' }}
        onSubmit={() => handleDeleteAvailability(barberId, deletePopup.availability?.id)}
        onClose={closeDeletePopup} //
      >
        <Modal.Title icon="warning">Delete Availability</Modal.Title>
        <Modal.Description>
          Are you sure you want to delete <strong>{deletePopup.availability?.date}</strong>? This action cannot be undone.
        </Modal.Description>
      </Modal>

      {/* Update Availability Modal */}
      <Modal
        open={updatePopup.open}
        fields={{
          start_time: '',
          end_time: '',
          slot_interval: '',
        }}
        action={{ submit: 'Update', loading: 'Updating...' }}
        onValidate={(payload) => isAnyFieldSet(payload, 'Fill at least start-end time to update the availability.')}
        onSubmit={(payload) => handleUpdateAvailability(barberId, updatePopup.availability?.id, cleanPayload(payload))}
        onClose={closeCreatePopup}
      >
        <Modal.Title icon="calendar">Create Availability</Modal.Title>
        <Modal.Description>
          Specify the time range when the barber is available on the day: <strong>{updatePopup.availability?.date}</strong>. 30min
          interval is default.
        </Modal.Description>

        <Input
          label="Start Time"
          type="time"
          name="start_time"
          required
          size="md" //
        />

        <Input
          label="End Time"
          type="time"
          name="end_time"
          required
          size="md" //
        />

        <Input
          label="Slot Interval (minutes)"
          type="number"
          name="slot_interval"
          min="1"
          placeholder="30"
          size="md"
          helperText="Optional. Defaults to 30." //
        />
      </Modal>
    </>
  );
}

export default AdminAvailabilities;
