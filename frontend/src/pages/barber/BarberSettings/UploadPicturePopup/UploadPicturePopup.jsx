import { useState } from 'react';
import styles from './UploadPicturePopup.module.scss';

import Popup from '@components/common/Popup/Popup';
import Form from '@components/common/Form/Form';
import FileInput from '@components/common/FileInput/FileInput';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';
import Spinner from '@components/common/Spinner/Spinner';
import Error from '@components/common/Error/Error';

function UploadPicturePopup({ open, onClose, onUpload }) {
  const [isUploading, setIsUploading] = useState(false); // Used to disable the upload button

  /**
   * Validates if a file was selected
   */
  const validate = ({ profile_image }) => {
    if (!profile_image) {
      return 'Please select an image to upload.';
    }

    // TODO: Add additional file type/size validations here.
    return undefined;
  };

  /**
   * Handles form submission for uploading the picture.
   */
  const handleUpload = async ({ profile_image }) => {
    setIsUploading(true);

    try {
      await onUpload(profile_image);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Popup className={styles.uploadPicturePopup} open={open} onClose={onClose}>
      <Form
        initialFields={{ profile_image: null }} // Custom file field handling because Input isn't set up for files
        onSubmit={handleUpload}
        validate={validate} //
      >
        <div className={styles.uploadPicture}>
          <div className={styles.uploadPictureHeader}>
            <Icon name="image" size="lg" black />
            <span className={styles.uploadPictureTitle}>Upload profile picture</span>
          </div>
          <div className={styles.uploadPictureContent}>
            <span className={styles.uploadPictureText}>Select a profile image to upload.</span>

            <FileInput
              name="profile_image"
              disabled={isUploading}
              accept="image/*" //
            />

            <div className={styles.uploadPictureAction}>
              <Button
                type="button"
                color="translight"
                onClick={onClose}
                size="md"
                disabled={isUploading}
                wide //
              >
                Cancel
              </Button>

              <Button
                type="submit"
                color="primary"
                size="md"
                disabled={isUploading}
                wide //
              >
                <span className={styles.line}>
                  {isUploading ? (
                    <>
                      <Spinner size={'sm'} /> Uploading...
                    </>
                  ) : (
                    'Upload'
                  )}
                </span>
              </Button>
            </div>
          </div>
          <Error />
        </div>
      </Form>
    </Popup>
  );
}

export default UploadPicturePopup;
