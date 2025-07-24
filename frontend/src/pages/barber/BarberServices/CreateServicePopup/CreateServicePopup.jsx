import { useState } from 'react';
import styles from './CreateServicePopup.module.scss';

import Popup from '@components/common/Popup/Popup';
import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';
import Spinner from '@components/common/Spinner/Spinner';
import Error from '@components/common/Error/Error';

function CreateServicePopup({ open, onClose, onCreate }) {
  const [isCreating, setIsCreating] = useState(false); // Used to disable the create service button

  const handleSubmit = async ({ name, price }) => {
    setIsCreating(true);

    try {
      await onCreate({ name, price }); // Parent handles fetch and closing
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <Popup className={styles.createServicePopup} open={open} onClose={onClose}>
      <Form initialFields={{ name: '', price: '' }} onSubmit={handleSubmit}>
        <div className={styles.createService}>
          <div className={styles.createServiceHeader}>
            <Icon name="id" size="lg" black />
            <span className={styles.createServiceTitle}>Create service</span>
          </div>
          <div className={styles.createServiceContent}>
            <div className={styles.createServiceText}>
              Enter the service&apos;s name and price for you newly offered service.
            </div>

            <div className={styles.createServiceField}>
              <Input
                label="Service name"
                type="text"
                name="name"
                required
                placeholder="Haircut"
                size="md"
                disabled={isCreating}
              />

              <Input
                label="Service Price"
                type="number"
                min="1"
                step="any"
                name="price"
                required
                placeholder="25.99"
                size="md"
                disabled={isCreating}
              />
            </div>

            <div className={styles.createServiceAction}>
              <Button
                type="button"
                color="translight"
                onClick={onClose}
                size="md"
                disabled={isCreating}
                wide //
              >
                Cancel
              </Button>
              <Button
                type="submit"
                color="primary"
                size="md"
                disabled={isCreating}
                wide //
              >
                <span className={styles.line}>
                  {isCreating ? (
                    <>
                      <Spinner size={'sm'} /> Creating...
                    </>
                  ) : (
                    'Create'
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

export default CreateServicePopup;
