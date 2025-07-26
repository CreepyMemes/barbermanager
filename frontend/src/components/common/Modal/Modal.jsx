import { useState, Children, isValidElement, cloneElement } from 'react';
import styles from './Modal.module.scss';

import Popup from '@components/common/Popup/Popup';
import Icon from '@components/common/Icon/Icon';
import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Error from '@components/common/Error/Error';
import Button from '@components/common/Button/Button';
import Spinner from '@components/common/Spinner/Spinner';

function Modal({
  open,
  fields,
  action,
  onValidate,
  onSubmit,
  onClose,
  children, // expects Modal.Title, Modal.Description, then form fields, then (optionally) custom extra actions
}) {
  const [isLoading, setIsLoading] = useState(false); // Used to disable the submit button while loading

  /**
   * Handles form submission running the submit function with passed data
   */
  const handleSubmit = async (data) => {
    setIsLoading(true);

    try {
      await onSubmit(data); // Parent must handle fetching and closing popup
    } finally {
      setIsLoading(false);
    }
  };

  // Extracts special children by type, passes the rest as the field inputs
  const all = Children.toArray(children);

  const [title, description] = [Title.displayName, Description.displayName].map((name) =>
    all.find((child) => child.type.displayName === name),
  );

  const fieldInputs = all.filter(
    (child) => child?.type?.displayName !== Title.displayName && child?.type?.displayName !== Description.displayName,
  );

  // Injects the isLoading prop to input fields
  const enhancedFields = fieldInputs.map((child) =>
    // Only clone Input components, pass through others unchanged
    isValidElement(child) && child.type === Input ? cloneElement(child, { disabled: isLoading }) : child,
  );

  return (
    <Popup
      className={styles.modalPopup}
      open={open}
      onClose={onClose} //
    >
      <Form
        initialFields={fields}
        validate={onValidate}
        onSubmit={handleSubmit} //
      >
        <div className={styles.modal}>
          {title}
          <div className={styles.modalContent}>
            {description}
            <div className={styles.modalField}>{enhancedFields}</div>
            <div className={styles.modalAction}>
              <Button
                type="button"
                color="translight"
                onClick={onClose}
                size="md"
                disabled={isLoading}
                wide //
              >
                Cancel
              </Button>

              <Button
                type="submit"
                color="primary"
                size="md"
                disabled={isLoading}
                wide //
              >
                <span className={styles.line}>
                  {isLoading ? (
                    <>
                      <Spinner size={'sm'} /> {action.loading}
                    </>
                  ) : (
                    action.submit
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

// Subcomponents for clean declarative usage
const Title = ({ icon, children }) => {
  <div className={styles.modalHeader}>
    {<Icon name={icon} size="lg" black />}
    <span className={styles.modalTitle}>{children}</span>
  </div>;
};

const Description = ({ children }) => {
  <div className={styles.modalDescription}>{children}</div>;
};

// Set display names for subcomponent identification
Title.displayName = 'ModalTitle';
Description.displayName = 'ModalDescription';

// Attach to main component for namespacing
Modal.Title = Title;
Modal.Description = Description;

export default Modal;
