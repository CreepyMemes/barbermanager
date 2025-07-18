import { useState } from 'react';
import styles from './DeleteServicePopup.module.scss';

import Popup from '@components/common/Popup/Popup';
import Form from '@components/common/Form/Form';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';
import Spinner from '@components/common/Spinner/Spinner';
import Error from '@components/common/Error/Error';

function DeleteServicePopup({ open, onClose, service, onDelete }) {
  const [isDeleting, setIsDeletingId] = useState(false); // Used to disable the delete service button

  const handleDelete = async () => {
    setIsDeletingId(true);

    try {
      await onDelete(service.id); // Parent handles fetch and closing
    } finally {
      setIsDeletingId(false);
    }
  };

  return (
    <Popup className={styles.deleteServicePopup} open={open} onClose={onClose}>
      <Form onSubmit={handleDelete}>
        <div className={styles.deleteService}>
          <div className={styles.deleteServiceHeader}>
            <Icon name="warning" size="lg" black />
            <span className={styles.deleteServiceTitle}>Delete service</span>
          </div>
          <div className={styles.deleteServiceContent}>
            <span className={styles.deleteServiceText}>Are you sure you want to delete </span>
            <span className={styles.deleteServiceUsername}>{service?.name}</span>
            <span className={styles.deleteServiceText}> ? This action cannot be undone. </span>

            <div className={styles.deleteServiceAction}>
              <Button
                type="button"
                color="translight"
                onClick={onClose}
                size="md"
                disabled={isDeleting}
                wide //
              >
                Cancel
              </Button>

              <Button
                type="submit"
                color="primary"
                size="md"
                disabled={isDeleting}
                wide //
              >
                <span className={styles.line}>
                  {isDeleting ? (
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
  );
}

export default DeleteServicePopup;
