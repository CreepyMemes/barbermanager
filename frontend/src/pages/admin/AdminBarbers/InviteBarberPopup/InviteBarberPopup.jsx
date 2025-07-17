import { useState } from 'react';
import styles from './InviteBarberPopup.module.scss';

import Popup from '@components/common/Popup/Popup';
import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';
import Spinner from '@components/common/Spinner/Spinner';
import Error from '@components/common/Error/Error';

function InviteBarberPopup({ open, onClose, onInvite }) {
  const [isInviting, setIsInviting] = useState(false); // Used to disable the invite barber button

  const handleSubmit = async ({ email }) => {
    setIsInviting(true);

    try {
      await onInvite(email); // Parent handles fetch and closing
    } finally {
      setIsInviting(false);
    }
  };

  return (
    <Popup className={styles.inviteBarberPopup} open={open} onClose={onClose}>
      <Form initialFields={{ email: '' }} onSubmit={handleSubmit}>
        <div className={styles.inviteBarber}>
          <div className={styles.inviteBarberHeader}>
            <Icon name="email_base" size="lg" black />
            <span className={styles.inviteBarberTitle}>Invite barber</span>
          </div>
          <div className={styles.inviteBarberContent}>
            <div className={styles.inviteBarberText}>
              Enter the barber&apos;s email address to send them an invitation to register.
            </div>
            <div className={styles.inviteBarberField}>
              <Input
                label="Barber email"
                type="email"
                name="email"
                required
                placeholder="barber@email.com"
                size="md"
                disabled={isInviting}
              />
            </div>
            <div className={styles.inviteBarberAction}>
              <Button
                type="button"
                color="translight"
                onClick={onClose}
                size="md"
                disabled={isInviting}
                wide //
              >
                Cancel
              </Button>
              <Button
                type="submit"
                color="primary"
                size="md"
                disabled={isInviting}
                wide //
              >
                <span className={styles.line}>
                  {isInviting ? (
                    <>
                      <Spinner size={'sm'} /> Sending...
                    </>
                  ) : (
                    'Send'
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

export default InviteBarberPopup;
