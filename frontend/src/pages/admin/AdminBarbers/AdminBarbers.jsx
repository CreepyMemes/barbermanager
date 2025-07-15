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
import Popup from '@components/common/Popup/Popup';
import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Error from '@components/common/Error/Error';
import Spinner from '@components/common/Spinner/Spinner';

function AdminBarbers() {
  const { profile } = useAuth();
  const [barbers, setBarbers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const [isDeletingId, setIsDeletingId] = useState(null); // Used to disable button associated to the deleted barber while loading
  const [isInviting, setIsInviting] = useState(false); // Used to disable the invite barber button

  // Popup states
  const [deletePopup, setDeletePopup] = useState({ open: false, barber: null });
  const [invitePopup, setInvitePopup] = useState(false);

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

  // Invite popup open
  const openInvitePopup = () => {
    setInvitePopup(true);
  };

  // Invite popup close
  const closeInvitePopup = () => {
    setInvitePopup(false);
  };

  // Handles setting the delete barber popup to be opened, and sets the selected barber
  const openDeletePopup = (barber) => {
    setDeletePopup({ open: true, barber });
  };

  // Handles settitng the delete barber popup to be closed
  const closeDeletePopup = () => {
    setDeletePopup({ open: false, barber: null });
  };

  /**
   * Handles inviting a new barber
   */
  const handleInviteBarber = async ({ email }) => {
    setIsInviting(true);

    try {
      await api.admin.inviteBarber(email); // throws on error (handled by Form)
      closeInvitePopup();
      await fetchBarbers(); // refresh list after invitation
    } finally {
      setIsInviting(false);
    }
  };

  /**
   * Delete barber handler with confirmation
   */
  const handleDeleteBarber = async () => {
    setIsDeletingId(deletePopup.barber.id);

    try {
      await api.admin.deleteBarber(deletePopup.barber.id); // throws on error (handled by Form)
      closeDeletePopup();
      await fetchBarbers(); // refresh list after deletion
    } finally {
      setIsDeletingId(null);
    }
  };

  // Only render UI for admins; otherwise, render nothing
  if (!profile || profile?.role !== 'ADMIN') return null;

  return (
    <>
      <div className={styles.adminBarbers}>
        <Pagination icon="barber" label="Barbers" itemsPerPage="5" loading={isLoading} emptyMessage="No barbers found.">
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
                      <Icon name="refresh" size="ty" /> Refresh Barbers
                    </>
                  )}
                </span>
              </Button>

              <Button
                className={styles.actionBtn}
                type="button"
                color="primary"
                size="md"
                onClick={openInvitePopup}
                disabled={isInviting} //
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
                  onClick={() => openDeletePopup(barber)}
                  disabled={isDeletingId === barber.id}
                >
                  <Icon name="trash" size="sm" black />
                </Button>
              </Pagination.Cell>
            </Pagination.Row>
          ))}
        </Pagination>
      </div>

      {/* Invite barber popup */}
      <Popup className={styles.inviteBarberPopup} open={invitePopup} onClose={closeInvitePopup}>
        <Form initialFields={{ email: '' }} onSubmit={handleInviteBarber}>
          <div className={styles.inviteBarber}>
            <div className={styles.inviteBarberHeader}>
              <Icon name="email_base" size="lg" black />
              <span className={styles.inviteBarberTitle}>Invite barber</span>
            </div>
            <div className={styles.inviteBarberContent}>
              <div className={styles.inviteBarberText}>
                Enter the barber&apos;s email address to send them an invitation to register.
              </div>
              <div className={styles.inviteBarberField}>
                <Input
                  label="Barber email"
                  type="email"
                  name="email"
                  required
                  placeholder="barber@email.com"
                  size="md"
                  disabled={isInviting}
                />
              </div>
              <div className={styles.inviteBarberAction}>
                <Button
                  type="button"
                  color="translight"
                  onClick={closeInvitePopup}
                  size="md"
                  wide //
                >
                  Cancel
                </Button>

                <Button
                  type="submit"
                  color="primary"
                  size="md"
                  disabled={isInviting}
                  wide //
                >
                  <span className={styles.line}>
                    {isInviting ? (
                      <>
                        <Spinner size={'sm'} /> Sending...
                      </>
                    ) : (
                      'Send'
                    )}
                  </span>
                </Button>
              </div>
            </div>
            <Error />
          </div>
        </Form>
      </Popup>

      {/* Delete barber popup */}
      <Popup className={styles.deleteBarberPopup} open={deletePopup.open} onClose={closeDeletePopup}>
        <Form
          initialFields={{}} // no fields required
          onSubmit={handleDeleteBarber}
        >
          <div className={styles.deleteBarber}>
            <div className={styles.deleteBarberHeader}>
              <Icon name="warning" size="lg" black />
              <span className={styles.deleteBarberTitle}>Delete barber</span>
            </div>

            <div className={styles.deleteBarberContent}>
              <span className={styles.deleteBarberText}>Are you sure you want to delete </span>
              <span className={styles.deleteBarberUsername}>
                {deletePopup.barber?.username || deletePopup.barber?.email}
              </span>
              <span className={styles.deleteBarberText}> ? This action cannot be undone. </span>

              <div className={styles.deleteBarberAction}>
                <Button
                  type="button"
                  color="translight"
                  onClick={closeDeletePopup}
                  size="md"
                  wide //
                >
                  Cancel
                </Button>

                <Button
                  type="submit"
                  color="primary"
                  size="md"
                  disabled={isDeletingId === deletePopup.barber?.id}
                  wide //
                >
                  <span className={styles.line}>
                    {isDeletingId ? (
                      <>
                        <Spinner size={'sm'} /> Deleting...
                      </>
                    ) : (
                      'Delete'
                    )}
                  </span>
                </Button>
              </div>
            </div>
          </div>

          <Error />
        </Form>
      </Popup>
    </>
  );
}

export default AdminBarbers;
