import { useState } from 'react';
import styles from './DeleteBarberPopup.module.scss';

import Popup from '@components/common/Popup/Popup';
import Form from '@components/common/Form/Form';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';
import Spinner from '@components/common/Spinner/Spinner';
import Error from '@components/common/Error/Error';

function DeleteBarberPopup({ open, onClose, barber, onDelete }) {
  const [isDeleting, setIsDeletingId] = useState(false); // Used to disable the delete barber button

  const handleDelete = async () => {
    setIsDeletingId(true);

    try {
      await onDelete(barber.id); // Parent handles fetch and closing
    } finally {
      setIsDeletingId(false);
    }
  };

  return (
    <Popup className={styles.deleteBarberPopup} open={open} onClose={onClose}>
      <Form onSubmit={handleDelete}>
        <div className={styles.deleteBarber}>
          <div className={styles.deleteBarberHeader}>
            <Icon name="warning" size="lg" black />
            <span className={styles.deleteBarberTitle}>Delete barber</span>
          </div>
          <div className={styles.deleteBarberContent}>
            <span className={styles.deleteBarberText}>Are you sure you want to delete </span>
            <span className={styles.deleteBarberUsername}>{barber?.username || barber?.email}</span>
            <span className={styles.deleteBarberText}> ? This action cannot be undone. </span>

            <div className={styles.deleteBarberAction}>
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

export default DeleteBarberPopup;
