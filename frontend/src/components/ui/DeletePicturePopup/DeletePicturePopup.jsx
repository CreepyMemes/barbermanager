import { useState } from 'react';
import styles from './DeletePicturePopup.module.scss';

import Popup from '@components/common/Popup/Popup';
import Form from '@components/common/Form/Form';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';
import Spinner from '@components/common/Spinner/Spinner';
import Error from '@components/common/Error/Error';

function DeletePicturePopup({ open, onClose, onDelete }) {
  const [isDeleting, setIsDeleting] = useState(false); // Used to disable the delete picture button

  const handleDelete = async () => {
    setIsDeleting(true);

    try {
      await onDelete(); // Parent handles fetch and closing
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <Popup className={styles.deletePicturePopup} open={open} onClose={onClose}>
      <Form onSubmit={handleDelete}>
        <div className={styles.deletePicture}>
          <div className={styles.deletePictureHeader}>
            <Icon name="warning" size="lg" black />
            <span className={styles.deletePictureTitle}>Delete service</span>
          </div>
          <div className={styles.deletePictureContent}>
            <span className={styles.deletePictureText}>
              Are you sure you want to delete your profile picture? This action cannot be undone.
            </span>

            <div className={styles.deletePictureAction}>
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

export default DeletePicturePopup;
