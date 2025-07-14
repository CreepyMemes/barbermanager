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
import Error from '@components/common/Error/Error';
import Spinner from '@components/common/Spinner/Spinner';

function AdminBarbers() {
  const { profile } = useAuth();
  const [barbers, setBarbers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [deletingId, setDeletingId] = useState(null); // Used to disable buttton associated to the deleted barber while loading

  const [popup, setPopup] = useState({ open: false, barber: null });

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

  /**
   * Handles setting the delete barber popup to be opened, and sets the selected barber
   */
  function openDeletePopup(barber) {
    setPopup({ open: true, barber });
  }

  /**
   * Handles settitng the delete barber popup to be closed
   */
  function closeDeletePopup() {
    setPopup({ open: false, barber: null });
  }

  /**
   * Delete barber handler with confirmation
   */
  const handleDeleteBarber = async () => {
    setDeletingId(popup.barber.id);

    try {
      await api.admin.deleteBarber(popup.barber.id); // throws on error, caught by FormProvider
      closeDeletePopup();

      await fetchBarbers(); // refresh list after deletion
    } finally {
      setDeletingId(null);
    }
  };

  // Only render UI for admins; otherwise, render nothing
  if (!profile || profile?.role !== 'ADMIN') return null;

  return (
    <>
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
                  onClick={() => openDeletePopup(barber)}
                  disabled={deletingId === barber.id}
                >
                  <Icon name="trash" size="sm" black />
                </Button>
              </Pagination.Cell>
            </Pagination.Row>
          ))}
        </Pagination>
      </div>

      <Popup className={styles.deleteBarberPopup} open={popup.open} onClose={closeDeletePopup}>
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
              <span className={styles.deleteBarberEmail}>{popup.barber?.username}</span>
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
                  disabled={deletingId === popup.barber?.id}
                  wide //
                >
                  <span className={styles.line}>
                    {deletingId ? (
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
