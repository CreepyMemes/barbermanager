import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './BarberServices.module.scss';
import api from '@api';

import CreateServicePopup from './CreateServicePopup/CreateServicePopup';
import DeleteServicePopup from './DeleteServicePopup/DeleteServicePopup';
import UpdateServicePopup from './UpdateServicePopup/UpdateServicePopup';

import Icon from '@components/common/Icon/Icon';
import Pagination from '@components/common/Pagination/Pagination';
import Button from '@components/common/Button/Button';
import Spinner from '@components/common/Spinner/Spinner';

function BarberServices() {
  const { profile } = useAuth();
  const [services, setServices] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Popup states
  const [createPopup, setCreatePopup] = useState(false);
  const [deletePopup, setDeletePopup] = useState({ open: false, service: null });
  const [updatePopup, setUpdatePopup] = useState({ open: false, service: null });

  /**
   * Defines fetching services from api (single responsibility, outside effect)
   */
  const fetchServices = useCallback(async () => {
    setIsLoading(true);

    try {
      const result = await api.barber.getBarberServices();
      setServices(result.services || []);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Only fetch if profile is loaded AND user is barber
   */
  useEffect(() => {
    if (profile?.role === 'BARBER') {
      fetchServices();
    }
  }, [profile, fetchServices]);

  // Invite popup state handlers
  const openCreatePopup = () => setCreatePopup(true);
  const closeCreatePopup = () => setCreatePopup(false);

  // Delete popup state handlers
  const openDeletePopup = (service) => setDeletePopup({ open: true, service });
  const closeDeletePopup = () => setDeletePopup({ open: false, service: null });

  // Update popup state handlers
  const openUpdatePopup = (service) => setUpdatePopup({ open: true, service });
  const closeUpdatePopup = () => setUpdatePopup({ open: false, service: null });

  /**
   * Handles inviting a new barber
   */
  const handleCreateService = async ({ name, price }) => {
    await api.barber.createBarberService({ name, price });
    closeCreatePopup();
    await fetchServices();
  };

  /**
   * Handles deleting the selected service
   */
  const handleDeleteService = async (serviceId) => {
    await api.barber.deleteBarberService(serviceId);
    closeDeletePopup();
    await fetchServices();
  };

  /**
   * Handles updating the selected service
   */
  const handleUpdateService = async ({ name, price }) => {
    await api.barber.updateBarberService(updatePopup.service.id, { name, price });
    closeUpdatePopup();
    await fetchServices();
  };

  // Only render UI for admins; otherwise, render nothing
  if (!profile || profile.role !== 'BARBER') return null;

  return (
    <>
      <div className={styles.barberServices}>
        <Pagination
          icon="service"
          label="Services"
          itemsPerPage={5}
          loading={isLoading}
          emptyMessage="No services offered." //
        >
          <Pagination.Action>
            <div className={styles.action}>
              <Button
                className={styles.refreshBtn}
                type="button"
                color="primary"
                size="md"
                onClick={fetchServices}
                disabled={isLoading}
              >
                <span className={styles.line}>
                  {isLoading ? (
                    <>
                      <Spinner size={'sm'} /> Refreshing...
                    </>
                  ) : (
                    <>
                      <Icon name="refresh" size="ty" /> Refresh services
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
                <span>Create service</span>
              </Button>
            </div>
          </Pagination.Action>

          {/* Table headers */}

          <Pagination.Column>
            <div className={styles.tableTitle}>
              <Icon name="scissors" size="ty" black />
              <span className={styles.tableTitleName}>Name</span>
            </div>
          </Pagination.Column>

          <Pagination.Column>
            <div className={styles.tableTitle}>
              <Icon name="revenue" size="ty" black />
              <span className={styles.tableTitleName}>Price</span>
            </div>
          </Pagination.Column>

          <Pagination.Column>
            <div className={styles.tableTitle}>
              <Icon name="id" size="ty" black />
              <span className={styles.tableTitleName}>Service ID</span>
            </div>
          </Pagination.Column>

          <Pagination.Column>
            <div className={styles.tableTitle}>
              <Icon name="dial" size="ty" black />
              <span className={styles.tableTitleName}>Actions</span>
            </div>
          </Pagination.Column>

          {/* Table rows */}
          {services.map((service) => (
            <Pagination.Row key={service.id}>
              <Pagination.Cell>
                <span className={styles.serviceName}>{service.name}</span>
              </Pagination.Cell>

              <Pagination.Cell>
                <span className={styles.servicePrice}>${service.price}</span>
              </Pagination.Cell>

              <Pagination.Cell>
                <div className={styles.serviceId}>
                  <span className={styles.hash}># </span>
                  <span className={styles.id}>{service.id} </span>
                </div>
              </Pagination.Cell>

              <Pagination.Cell>
                <div className={styles.actions}>
                  <Button
                    type="button"
                    size="sm"
                    color="animated"
                    onClick={() => openUpdatePopup(service)} //
                  >
                    <Icon name="pen" size="ty" black />
                  </Button>

                  <Button
                    type="button"
                    size="sm"
                    color="animated"
                    onClick={() => openDeletePopup(service)} //
                  >
                    <Icon name="trash" size="ty" black />
                  </Button>
                </div>
              </Pagination.Cell>
            </Pagination.Row>
          ))}
        </Pagination>
      </div>

      <CreateServicePopup
        open={createPopup}
        onClose={closeCreatePopup}
        onCreate={handleCreateService} //
      />

      <DeleteServicePopup
        open={deletePopup.open}
        onClose={closeDeletePopup}
        onDelete={handleDeleteService}
        service={deletePopup.service} //
      />

      <UpdateServicePopup
        open={updatePopup.open}
        onClose={closeUpdatePopup}
        onUpdate={handleUpdateService}
        service={updatePopup.service} //
      />
    </>
  );
}

export default BarberServices;
