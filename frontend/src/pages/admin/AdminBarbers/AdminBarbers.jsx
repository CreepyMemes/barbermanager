import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './AdminBarbers.module.scss';
import api from '@api';

import Icon from '@components/common/Icon/Icon';
import Pagination from '@components/common/Pagination/Pagination';
import Profile from '@components/ui/Profile/Profile';
import Rating from '@components/ui/Rating/Rating';
import Tag from '@components/common/Tag/Tag';
import Button from '@components/common/Button/Button';
import Modal from '@components/common/Modal/Modal';
import Input from '@components/common/Input/Input';
import Spinner from '@components/common/Spinner/Spinner';

function AdminBarbers() {
  const { profile } = useAuth();
  const [barbers, setBarbers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Popup states
  const [deletePopup, setDeletePopup] = useState({ open: false, barber: null });
  const [invitePopup, setInvitePopup] = useState(false);

  /**
   * Defines fetching barbers from api (single responsibility, outside effect)
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
    if (profile?.role === 'ADMIN') {
      fetchBarbers();
    }
  }, [profile, fetchBarbers]);

  // Invite popup state handlers
  const openInvitePopup = () => setInvitePopup(true);
  const closeInvitePopup = () => setInvitePopup(false);

  // Delete popup state handlers
  const openDeletePopup = (barber) => setDeletePopup({ open: true, barber });
  const closeDeletePopup = () => setDeletePopup({ open: false, barber: null });

  /**
   * Handles inviting a new barber
   */
  const handleInviteBarber = async ({ email }) => {
    await api.admin.inviteBarber({ email });
    closeInvitePopup();
    await fetchBarbers();
  };

  /**
   * Handles deleting the selected barber
   */
  const handleDeleteBarber = async (barberId) => {
    await api.admin.deleteBarber(barberId);
    closeDeletePopup();
    await fetchBarbers();
  };

  // Only render UI for admins; otherwise, render nothing
  if (!profile || profile.role !== 'ADMIN') return null;

  return (
    <>
      {/* Registered Barbers Pagination */}
      <Pagination
        className={styles.adminBarbers}
        icon="barber"
        label="Barbers"
        itemsPerPage={5}
        loading={isLoading}
        emptyMessage="No barbers found." //
      >
        <Pagination.Action>
          <div className={styles.action}>
            <Button
              className={styles.refreshBtn}
              type="button"
              color="primary"
              size="md"
              onClick={fetchBarbers}
              disabled={isLoading}
            >
              <span className={styles.line}>
                {isLoading ? (
                  <>
                    <Spinner size={'sm'} /> Refreshing...
                  </>
                ) : (
                  <>
                    <Icon name="refresh" size="ty" /> Refresh barbers
                  </>
                )}
              </span>
            </Button>

            <Button
              className={styles.actionBtn}
              type="button"
              color="primary"
              size="md"
              onClick={openInvitePopup} //
            >
              <Icon name="plus" size="ty" />
              <span>Invite barber</span>
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
              <div className={styles.emailContainer}>
                <span className={styles.email}>{barber.email}</span>
              </div>
            </Pagination.Cell>

            <Pagination.Cell>
              <Rating rating={barber.average_rating} />
            </Pagination.Cell>

            <Pagination.Cell>
              <span className={styles.revenue}>${barber.total_revenue}</span>
            </Pagination.Cell>

            <Pagination.Cell>
              <Tag className={styles.tag} color={barber.is_active ? 'green' : 'yellow'}>
                {barber.is_active ? 'Active' : 'Invited'}
              </Tag>
            </Pagination.Cell>

            <Pagination.Cell>
              <Button
                type="button"
                size="sm"
                color="animated"
                onClick={() => openDeletePopup(barber)} //
              >
                <Icon name="trash" size="sm" black />
              </Button>
            </Pagination.Cell>
          </Pagination.Row>
        ))}
      </Pagination>

      {/* Invite Barber Modal */}
      <Modal
        open={invitePopup}
        fields={{ email: '' }}
        action={{ submit: 'Send', loading: 'Sending...' }}
        onSubmit={handleInviteBarber}
        onClose={closeInvitePopup}
      >
        <Modal.Title icon="email_base">Invite Barber</Modal.Title>
        <Modal.Description>Enter the barber&apos;s email address to send them an invitation to register.</Modal.Description>

        <Input
          label="Barber email"
          type="email"
          name="email"
          required
          placeholder="barber@email.com"
          size="md" //
        />
      </Modal>

      {/* Delete Barber Modal */}
      <Modal
        open={deletePopup.open}
        action={{ submit: 'Delete', loading: 'Deleting...' }}
        onSubmit={() => handleDeleteBarber(deletePopup.barber?.id)}
        onClose={closeDeletePopup}
      >
        <Modal.Title icon="warning">Delete Barber</Modal.Title>
        <Modal.Description>
          Are you sure you want to delete <strong>{deletePopup.barber?.username || deletePopup.barber?.email}</strong> ? This
          action cannot be undone.
        </Modal.Description>
      </Modal>
    </>
  );
}

export default AdminBarbers;
