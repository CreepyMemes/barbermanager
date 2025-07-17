import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './AdminAppointments.module.scss';
import api from '@api';

import Pagination from '@components/common/Pagination/Pagination';
import Icon from '@components/common/Icon/Icon';
import Tag from '@components/common/Tag/Tag';
import Button from '@components/common/Button/Button';
import Spinner from '@components/common/Spinner/Spinner';

function AdminAppointments() {
  const { profile } = useAuth();
  const [appointments, setAppointments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

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
   * Only fetch if profile is loaded AND user is admin
   */
  useEffect(() => {
    if (profile?.role === 'ADMIN') {
      fetchAppointments();
    }
  }, [profile, fetchAppointments]);

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
                    <Icon name="refresh" size="ty" /> Refresh Appointments
                  </>
                )}
              </span>
            </Button>
          </div>
        </Pagination.Action>

        {/* Table headers */}
        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="id" size="ty" black />
            <span className={styles.tableTitleName}>ID</span>
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
            <Icon name="barber" size="ty" black />
            <span className={styles.tableTitleName}>Barber ID</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="user" size="ty" black />
            <span className={styles.tableTitleName}>Client ID</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="service" size="ty" black />
            <span className={styles.tableTitleName}>Service IDs</span>
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
              <span className={styles.id}>#{appointment.id}</span>
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
              <span className={styles.simpleId}>{appointment.barber_id}</span>
            </Pagination.Cell>

            <Pagination.Cell>
              <span className={styles.simpleId}>{appointment.client_id}</span>
            </Pagination.Cell>

            <Pagination.Cell>
              <span className={styles.services}>
                {appointment.service_ids.length > 0 ? (
                  appointment.service_ids.join(', ')
                ) : (
                  <span className={styles.noServices}>None</span>
                )}
              </span>
            </Pagination.Cell>

            <Pagination.Cell>
              <Tag className={styles.reminderTag} color={appointment.reminder_email_sent ? 'blue' : 'yellow'}>
                {appointment.reminder_email_sent ? 'Sent' : 'Not Sent'}
              </Tag>
            </Pagination.Cell>

            <Pagination.Cell>
              <Tag
                className={styles.tag}
                color={
                  appointment.status === 'COMPLETED' ? 'green' : appointment.status === 'ONGOING' ? 'yellow' : 'red'
                }
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
