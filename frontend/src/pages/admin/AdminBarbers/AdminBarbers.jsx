import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './AdminBarbers.module.scss';

import api from '@api';
import Pagination from '@components/common/Pagination/Pagination';
import Icon from '@components/common/Icon/Icon';
import Profile from '@components/common/Profile/Profile';
import Rating from '@components/common/Rating/Rating';
import Tag from '@components/common/Tag/Tag';
import Button from '@components/common/Button/Button';

function AdminBarbers() {
  const { profile } = useAuth();
  const [barbers, setBarbers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [deletingId, setDeletingId] = useState(null); // optionally indicate deleting

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

  // Delete barber handler with confirmation
  const handleDeleteBarber = useCallback(
    async (barberId, barberEmail) => {
      const confirmed = window.confirm(
        `Are you sure you want to delete barber "${barberEmail}"?\nThis action cannot be undone.`,
      );
      if (!confirmed) return;

      try {
        setDeletingId(barberId);
        await api.admin.deleteBarber(barberId);
        await fetchBarbers(); // refresh list after deletion
      } catch (err) {
        window.alert('Failed to delete barber. Please try again.');
      } finally {
        setDeletingId(null);
      }
    },
    [fetchBarbers],
  );

  // Only render UI for admins; otherwise, render nothing
  if (!profile || profile?.role !== 'ADMIN') return null;

  return (
    <div className={styles.adminBarbers}>
      <Pagination icon="barber" label="Barbers" itemsPerPage="5" loading={isLoading} emptyMessage="No barbers found.">
        <Pagination.Action>
          <div className={styles.action}>put invite new barber here</div>
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
            <Icon name="review" size="ty" black />
            <span className={styles.tableTitleName}>Rating</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="revenue" size="ty" black />
            <span className={styles.tableTitleName}>Revenue</span>
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

        {/* Table Rows */}
        {barbers.map((barber) => (
          <Pagination.Row key={barber.id}>
            <Pagination.Cell>
              <Profile profile={barber} />
            </Pagination.Cell>

            <Pagination.Cell>
              <span className={styles.email}>{barber.email}</span>
            </Pagination.Cell>

            <Pagination.Cell>
              <Rating rating={barber.average_rating} />
            </Pagination.Cell>

            <Pagination.Cell>
              <span className={styles.revenue}>${barber.total_revenue}</span>
            </Pagination.Cell>

            <Pagination.Cell>
              <Tag className={styles.tag} color={barber.is_active ? 'green' : 'yellow'}>
                {barber.is_active ? 'Active' : 'Inactive'}
              </Tag>
            </Pagination.Cell>

            <Pagination.Cell>
              <Button
                type="button"
                size="sm"
                color="animated"
                onClick={() => handleDeleteBarber(barber.id, barber.email)}
                disabled={deletingId === barber.id}
                aria-label={`Delete barber ${barber.full_name || barber.email}`}
              >
                <Icon name="trash" size="sm" black />
              </Button>
            </Pagination.Cell>
          </Pagination.Row>
        ))}
      </Pagination>
    </div>
  );
}

export default AdminBarbers;
