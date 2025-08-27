import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './AdminClients.module.scss';
import api from '@api';

import Pagination from '@components/common/Pagination/Pagination';
import Icon from '@components/common/Icon/Icon';
import Profile from '@components/ui/Profile/Profile';
import Tag from '@components/common/Tag/Tag';
import Button from '@components/common/Button/Button';
import Spinner from '@components/common/Spinner/Spinner';

function AdminClients() {
  const { profile } = useAuth();
  const [clients, setClients] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Defines fetching clients from api (single responsibility, outside effect)
   */
  const fetchClients = useCallback(async () => {
    setIsLoading(true);

    try {
      const result = await api.admin.getAllClients();
      setClients(result.clients || []);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Only fetch if profile is loaded AND user is admin
   */
  useEffect(() => {
    if (profile?.role === 'ADMIN') {
      fetchClients();
    }
  }, [profile, fetchClients]);

  // Only render UI for admins; otherwise, render nothing// Only render UI for admins; otherwise, render nothing
  if (!profile || profile.role !== 'ADMIN') return null;

  return (
    <div className={styles.adminClients}>
      <Pagination
        icon="client"
        label="Clients"
        itemsPerPage={5}
        loading={isLoading}
        emptyMessage="No clients found." //
      >
        <Pagination.Action>
          <div className={styles.action}>
            <Button
              className={styles.refreshBtn}
              type="button"
              color="primary"
              size="md"
              onClick={fetchClients}
              disabled={isLoading} //
            >
              <span className={styles.line}>
                {isLoading ? (
                  <>
                    <Spinner size="sm" /> Refreshing...
                  </>
                ) : (
                  <>
                    <Icon name="refresh" size="ty" /> Refresh Clients
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
            <Icon name="email_base" size="ty" black />
            <span className={styles.tableTitleName}>Email</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="appointment" size="ty" black />
            <span className={styles.tableTitleName}>Appointment</span>
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
            <Icon name="completed" size="ty" black />
            <span className={styles.tableTitleName}>Completed</span>
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
            <Icon name="spinner" size="ty" black />
            <span className={styles.tableTitleName}>Status</span>
          </div>
        </Pagination.Column>

        {/* Table Rows */}
        {clients.map((client) => (
          <Pagination.Row key={client.id}>
            <Pagination.Cell>
              <Profile profile={client} />
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.emailContainer}>
                <span className={styles.email}>{client.email}</span>
              </div>
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.upcomingAppointmentContainer}>
                <div className={styles.upcomingAppointment}>
                  {client.upcoming_appointment ? (
                    <>
                      <span className={styles.appointmentDate}>{client.upcoming_appointment.date.replaceAll('-', ' / ')}</span>
                      <span className={styles.appointmentSlot}>( {client.upcoming_appointment.slot} )</span>
                    </>
                  ) : (
                    <span className={styles.noAppointment}>—</span>
                  )}
                </div>
              </div>
            </Pagination.Cell>

            <Pagination.Cell>
              <span className={styles.spent}>${client.total_spent}</span>
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.completed}>
                <span className={styles.count}>{client.completed_appointments}</span>
                <span className={styles.text}>appointments</span>
              </div>
            </Pagination.Cell>

            <Pagination.Cell>
              <span className={styles.date}>{client.date_joined.replaceAll('-', ' / ')}</span>
            </Pagination.Cell>

            <Pagination.Cell>
              <Tag className={styles.tag} color={client.is_active ? 'green' : 'yellow'}>
                {client.is_active ? 'Active' : 'Inactive'}
              </Tag>
            </Pagination.Cell>
          </Pagination.Row>
        ))}
      </Pagination>
    </div>
  );
}

export default AdminClients;
