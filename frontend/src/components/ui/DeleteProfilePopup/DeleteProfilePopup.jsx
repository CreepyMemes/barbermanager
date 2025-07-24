import { useState } from 'react';
import styles from './DeleteProfilePopup.module.scss';

import Popup from '@components/common/Popup/Popup';
import Form from '@components/common/Form/Form';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';
import Spinner from '@components/common/Spinner/Spinner';
import Error from '@components/common/Error/Error';

function DeleteProfilePopup({ open, onClose, onDelete }) {
  const [isDeleting, setIsDeleting] = useState(false); // Used to disable the delete profile button

  const handleDelete = async () => {
    setIsDeleting(true);

    try {
      await onDelete(); // Parent handles fetch and closing
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <Popup className={styles.deleteProfilePopup} open={open} onClose={onClose}>
      <Form onSubmit={handleDelete}>
        <div className={styles.deleteProfile}>
          <div className={styles.deleteProfileHeader}>
            <Icon name="warning" size="lg" black />
            <span className={styles.deleteProfileTitle}>Delete service</span>
          </div>
          <div className={styles.deleteProfileContent}>
            <span className={styles.deleteProfileText}>
              Are you sure you want to delete your profile? This action cannot be undone.
            </span>

            <div className={styles.deleteProfileAction}>
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

export default DeleteProfilePopup;
