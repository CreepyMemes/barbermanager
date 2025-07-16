import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './AdminBarbers.module.scss';
import api from '@api';

import InviteBarberPopup from './InviteBarberPopup/InviteBarberPopup';
import DeleteBarberPopup from './DeleteBarberPopup/DeleteBarberPopup';

import Pagination from '@components/common/Pagination/Pagination';
import Icon from '@components/common/Icon/Icon';
import Profile from '@components/common/Profile/Profile';
import Rating from '@components/common/Rating/Rating';
import Tag from '@components/common/Tag/Tag';
import Button from '@components/common/Button/Button';
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
  const handleInviteBarber = async (email) => {
    await api.admin.inviteBarber(email);
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
      <div className={styles.adminBarbers}>
        <Pagination
          icon="barber"
          label="Barbers"
          itemsPerPage="5"
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
      </div>

      <InviteBarberPopup
        open={invitePopup}
        onClose={closeInvitePopup}
        onInvite={handleInviteBarber} //
      />

      <DeleteBarberPopup
        open={deletePopup.open}
        onClose={closeDeletePopup}
        onDelete={handleDeleteBarber}
        barber={deletePopup.barber} //
      />
    </>
  );
}

export default AdminBarbers;
