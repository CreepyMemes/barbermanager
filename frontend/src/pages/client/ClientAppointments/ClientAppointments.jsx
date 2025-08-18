import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './ClientAppointments.module.scss';
import api from '@api';

import BookAppointmentModal from './BookAppointmentModal';

import Pagination from '@components/common/Pagination/Pagination';
import Modal from '@components/common/Modal/Modal';
import Icon from '@components/common/Icon/Icon';
import Tag from '@components/common/Tag/Tag';
import Button from '@components/common/Button/Button';
import Spinner from '@components/common/Spinner/Spinner';
import Profile from '@components/ui/Profile/Profile';

function ClientAppointments() {
  const { profile } = useAuth();
  const [appointments, setAppointments] = useState([]);

  const [isLoadingAppointments, setIsLoadingAppointments] = useState(true);
  const [isLoadingBarberProfiles, setIsLoadingBarberProfiles] = useState(true);

  const [barbers, setBarbers] = useState({}); // barberId -> profile

  // Popup states
  const [bookPopup, setBookPopup] = useState(false);
  const [cancelPopup, setCancelPopup] = useState({ open: false, appointment: null });

  /**
   * Defines fetching all appointmentts from api (single responsibility, outside effect)
   */
  const fetchAppointments = useCallback(async () => {
    setIsLoadingAppointments(true);

    try {
      const result = await api.client.getClientAppointments();
      setAppointments(result.appointments || []);
    } finally {
      setIsLoadingAppointments(false);
    }
  }, []);

  /**
   * Defines fetching all barber profiles needed (only unique barber IDs)
   */
  const fetchClientProfiles = useCallback(async (appointments) => {
    setIsLoadingBarberProfiles(true);
    try {
      // Gets all unique barber IDs from appointments
      const barberIds = [...new Set(appointments.map((a) => a.barber_id))];

      // fetches all barber profiles in parallel
      const entries = await Promise.all(
        barberIds.map(async (id) => {
          try {
            const { profile } = await api.pub.getBarberProfilePublic(id);
            return [id, profile];
          } catch {
            return [id, null];
          }
        }),
      );

      setBarbers(Object.fromEntries(entries)); // assembles into { [id]: profile }
    } finally {
      setIsLoadingBarberProfiles(false);
    }
  }, []);

  /**
   * Only fetch if profile is loaded AND user is admin
   */
  useEffect(() => {
    if (profile?.role === 'CLIENT') {
      fetchAppointments();
    }
  }, [profile, fetchAppointments]);

  /**
   * When appointments change, fetch needed barber profiles
   */
  useEffect(() => {
    if (appointments.length > 0) {
      fetchClientProfiles(appointments);
    }
  }, [appointments, fetchClientProfiles]);

  // Book appointment popup state handlers
  const openCreatePopup = () => setBookPopup(true);
  const closeCreatePopup = () => setBookPopup(false);

  // Cancel apointment popup state handlers
  const openCancelPopup = (appointment) => setCancelPopup({ open: true, appointment });
  const closeCancelPopup = () => setCancelPopup({ open: false, appointment: null });

  /**
   * Handles booking appointmentss
   */
  const handleBookAppointment = async () => {
    await fetchAppointments();
  };

  /**
   * Handles canceling the selected appointment
   */
  const handleCancelAppointment = async (appointmentId) => {
    await api.client.cancelClientAppointment(appointmentId);
    closeCancelPopup();
    await fetchAppointments();
  };

  // Only render UI for admins; otherwise, render nothing
  if (!profile || profile.role !== 'CLIENT') return null;

  return (
    <>
      <Pagination
        className={styles.clientAppointments}
        icon="appointment"
        label="Appointments"
        itemsPerPage={7}
        loading={isLoadingAppointments}
        emptyMessage="No appointments found." //
      >
        <Pagination.Action>
          <div className={styles.action}>
            <Button
              className={styles.refreshBtn}
              type="button"
              color="primary"
              size="md"
              onClick={fetchAppointments}
              disabled={isLoadingAppointments} //
            >
              <span className={styles.line}>
                {isLoadingAppointments ? (
                  <>
                    <Spinner size="sm" /> Refreshing...
                  </>
                ) : (
                  <>
                    <Icon name="refresh" size="ty" /> Refresh appointments
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
              <span>Book appointment</span>
            </Button>
          </div>
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

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="email_base" size="ty" black />
            <span className={styles.tableTitleName}>Reminder</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="spinner" size="ty" black />
            <span className={styles.tableTitleName}>Status</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="dial" size="ty" black />
            <span className={styles.tableTitleName}>Actions</span>
          </div>
        </Pagination.Column>

        {/* Table rows */}
        {appointments.map((appointment) => (
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

            <Pagination.Cell>
              <Tag className={styles.reminderTag} color={appointment.reminder_email_sent ? 'blue' : 'yellow'}>
                {appointment.reminder_email_sent ? 'Sent' : 'Not Sent'}
              </Tag>
            </Pagination.Cell>

            <Pagination.Cell>
              <Tag
                className={styles.statusTag}
                color={appointment.status === 'COMPLETED' ? 'green' : appointment.status === 'ONGOING' ? 'yellow' : 'red'}
              >
                {appointment.status.charAt(0) + appointment.status.slice(1).toLowerCase()}
              </Tag>
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.actions}>
                <Button
                  type="button"
                  size="sm"
                  color="animated"
                  disabled={appointment.status !== 'ONGOING'}
                  onClick={() => openCancelPopup(appointment)} //
                >
                  <Icon name="trash" size="ty" black />
                </Button>
              </div>
            </Pagination.Cell>
          </Pagination.Row>
        ))}
      </Pagination>

      {/* Book Appointment Modal */}
      <BookAppointmentModal
        open={bookPopup}
        onClose={closeCreatePopup}
        onBooked={handleBookAppointment} //
      />

      {/* Cancel Appointment Modal */}
      <Modal
        open={cancelPopup.open}
        action={{ submit: 'Cancel', loading: 'Canceling...' }}
        onSubmit={() => handleCancelAppointment(cancelPopup.appointment?.id)}
        onClose={closeCancelPopup}
      >
        <Modal.Title icon="warning">Cancel Appointment</Modal.Title>
        <Modal.Description>
          Are you sure you want to cancel your appointment at <strong>{cancelPopup.appointment?.date}</strong>? This action cannot
          be undone.
        </Modal.Description>
      </Modal>
    </>
  );
}

export default ClientAppointments;
