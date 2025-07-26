import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './AdminAppointments.module.scss';
import api from '@api';

import Pagination from '@components/common/Pagination/Pagination';
import Icon from '@components/common/Icon/Icon';
import Tag from '@components/common/Tag/Tag';
import Button from '@components/common/Button/Button';
import Spinner from '@components/common/Spinner/Spinner';
import Profile from '@components/ui/Profile/Profile';

function AdminAppointments() {
  const { profile } = useAuth();
  const [appointments, setAppointments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const [barbers, setBarbers] = useState({}); // barberId -> profile
  const [clients, setClients] = useState({}); // clientId -> profile

  /**
   * Defines fetching all appointmentts from api (single responsibility, outside effect)
   */
  const fetchAppointments = useCallback(async () => {
    setIsLoading(true);

    try {
      const result = await api.admin.getAllAppointments();
      setAppointments(result.appointments || []);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Defines fetching all barber profiles needed (only unique barber IDs)
   */
  const fetchBarberProfiles = useCallback(async (appointments) => {
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
  }, []);

  /**
   * Defines fetching all client profiles needed (only unique client IDs)
   */
  const fetchClientProfiles = useCallback(async (appointments) => {
    // Gets all unique client IDs from appointments
    const clientIds = [...new Set(appointments.map((a) => a.client_id))];

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
    setClients(Object.fromEntries(entries));
  }, []);

  /**
   * Only fetch if profile is loaded AND user is admin
   */
  useEffect(() => {
    if (profile?.role === 'ADMIN') {
      fetchAppointments();
    }
  }, [profile, fetchAppointments]);

  /**
   * When appointments change, fetch needed barber profiles
   */
  useEffect(() => {
    if (appointments.length > 0) {
      fetchBarberProfiles(appointments);
      fetchClientProfiles(appointments);
    }
  }, [appointments, fetchBarberProfiles, fetchClientProfiles]);

  // Only render UI for admins; otherwise, render nothing
  if (!profile || profile.role !== 'ADMIN') return null;

  return (
    <div className={styles.adminAppointments}>
      <Pagination
        icon="appointment"
        label="Appointments"
        itemsPerPage={7}
        loading={isLoading}
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
              disabled={isLoading} //
            >
              <span className={styles.line}>
                {isLoading ? (
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
            <Icon name="client" size="ty" black />
            <span className={styles.tableTitleName}>Client</span>
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
            <Icon name="revenue" size="ty" black />
            <span className={styles.tableTitleName}>Spent</span>
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

        {/* Table rows */}
        {appointments.map((appointment) => (
          <Pagination.Row key={appointment.id}>
            <Pagination.Cell>
              {barbers[appointment.barber_id] ? <Profile profile={barbers[appointment.barber_id]} /> : <Spinner size="sm" />}
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
              {clients[appointment.client_id] ? <Profile profile={clients[appointment.client_id]} /> : <Spinner size="sm" />}
            </Pagination.Cell>

            <Pagination.Cell>
              <span className={styles.services}>{appointment.services.map((service) => service.name).join(', ')}</span>
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.amountSpent}>
                <span className={styles.amount}>${appointment.amount_spent}</span>
              </div>
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
          </Pagination.Row>
        ))}
      </Pagination>
    </div>
  );
}

export default AdminAppointments;
