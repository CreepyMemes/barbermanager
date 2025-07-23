import { useState } from 'react';
import styles from './UpdateServicePopup.module.scss';

import Popup from '@components/common/Popup/Popup';
import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';
import Spinner from '@components/common/Spinner/Spinner';
import Error from '@components/common/Error/Error';

function UpdateServicePopup({ open, onClose, onUpdate, service }) {
  const [isUpdating, setIsUpdating] = useState(false); // Used to disable the update service button

  /**
   * Validate at least one provided, matching your backend logic
   */
  const validate = ({ name, price }) => {
    const nameValue = name && name.trim();
    const priceValue = price !== '' && price !== undefined;

    if (!nameValue && !priceValue) {
      return 'Provide a new name, a new price, or both to update the service.';
    }
    return undefined;
  };

  /**
   * Handles form submission for updating the selected service
   * Send only the filled fields to the API
   */
  const handleUpdate = async ({ name, price }) => {
    setIsUpdating(true);

    const payload = {};
    if (name && name.trim() !== '') payload.name = name.trim();
    if (price !== '' && price !== undefined) payload.price = price;

    try {
      await onUpdate(service.id, payload);
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <Popup className={styles.updateServicePopup} open={open} onClose={onClose}>
      <Form
        initialFields={{ name: '', price: '' }}
        onSubmit={handleUpdate}
        validate={validate} //
      >
        <div className={styles.updateService}>
          <div className={styles.updateServiceHeader}>
            <Icon name="pen" size="lg" black />
            <span className={styles.updateServiceTitle}>Update service</span>
          </div>
          <div className={styles.updateServiceContent}>
            <span className={styles.updateServiceText}>Enter new values to update the service: </span>
            <span className={styles.updateServiceName}>{service?.name}</span>
            <span className={styles.updateServiceText}> This action cannot be undone. </span>

            <div className={styles.updateServiceField}>
              <Input
                label="Service name"
                type="text"
                name="name"
                placeholder={service?.name}
                size="md"
                disabled={isUpdating}
              />
              <Input
                label="Service Price"
                type="number"
                min="1"
                step="any"
                name="price"
                placeholder={service?.price}
                size="md"
                disabled={isUpdating}
              />
            </div>

            <div className={styles.updateServiceAction}>
              <Button
                type="button"
                color="translight"
                onClick={onClose}
                size="md"
                disabled={isUpdating}
                wide //
              >
                Cancel
              </Button>

              <Button
                type="submit"
                color="primary"
                size="md"
                disabled={isUpdating}
                wide //
              >
                <span className={styles.line}>
                  {isUpdating ? (
                    <>
                      <Spinner size={'sm'} /> Updating...
                    </>
                  ) : (
                    'Update'
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

export default UpdateServicePopup;
