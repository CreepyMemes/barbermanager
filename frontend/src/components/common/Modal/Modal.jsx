import { useState, Children, useEffect, isValidElement, cloneElement } from 'react';
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
  onSubmit,
  onClose,
  children, // expects Modal.Title, Modal.Description, then form fields, then (optionally) custom extra actions
}) {
  const [isLoading, setIsLoading] = useState(false); // Used to disable the submit button while loading
  const [stepIndex, setStepIndex] = useState(0);

  // Extracts special children by type, passes the rest as the field inputs
  const all = Children.toArray(children);

  const steps = all.filter((child) => child?.type?.displayName === Step.displayName);
  const isMultiStep = steps.length > 0;

  const activeStep = isMultiStep ? steps[stepIndex] : { props: { children: all } };
  const { children: stepChildren, validate: stepValidate } = activeStep.props;

  const [title, description] = [Title.displayName, Description.displayName].map((name) =>
    Children.toArray(stepChildren).find((child) => child?.type?.displayName === name),
  );

  const fieldInputs = Children.toArray(stepChildren).filter(
    (child) => ![Title.displayName, Description.displayName].includes(child?.type?.displayName),
  );

  // Injects the isLoading prop to input fields
  const enhancedFields = fieldInputs.map((child) =>
    // Only clone Input components, pass through others unchanged
    isValidElement(child) && child.type === Input ? cloneElement(child, { disabled: isLoading }) : child,
  );

  useEffect(() => {
    if (open) setStepIndex(0);
  }, [open]);

  /**
   * Handles form submission running the submit function with passed data
   */
  const handleSubmit = async (data) => {
    // Step-level validation (Form will call this before continuing)
    if (isMultiStep && stepValidate) {
      const error = stepValidate(data);
      if (error) {
        throw new Error(error); // FormProvider will catch this and show <Error />
      }
    }

    // If not last step, just go forward
    if (isMultiStep && stepIndex < steps.length - 1) {
      setStepIndex((i) => i + 1);
      return;
    }

    // Final step: actually submit
    setIsLoading(true);

    try {
      await onSubmit(data); // Parent must handle fetching and closing popup
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    if (isMultiStep && stepIndex > 0) setStepIndex((i) => i - 1);
    else onClose();
  };

  return (
    <Popup
      className={styles.modalPopup}
      open={open}
      onClose={onClose} //
    >
      <Form
        initialFields={fields}
        validate={(vals) => stepValidate?.(vals)}
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
                onClick={handleBack}
                size="md"
                disabled={isLoading}
                wide //
              >
                {isMultiStep && stepIndex > 0 ? 'Back' : 'Cancel'}
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
                      <Spinner size="sm" /> {action.loading}
                    </>
                  ) : isMultiStep && stepIndex < steps.length - 1 ? (
                    'Next'
                  ) : (
                    action.submit
                  )}
                </span>
              </Button>
            </div>

            {isMultiStep && (
              <div className={styles.modalStepIndicator}>
                Step {stepIndex + 1} of {steps.length}
              </div>
            )}
          </div>

          <Error />
        </div>
      </Form>
    </Popup>
  );
}

// Subcomponents for clean declarative usage

const Step = ({ children }) => <>{children}</>; // Step container (may include `validate` prop)

const Title = ({ icon, children }) => (
  <div className={styles.modalHeader}>
    {icon && <Icon name={icon} size="lg" black />}
    <span className={styles.modalTitle}>{children}</span>
  </div>
);

const Description = ({ children }) => <div className={styles.modalDescription}>{children}</div>;

// Set display names for subcomponent identification
Step.displayName = 'ModalStep';
Title.displayName = 'ModalTitle';
Description.displayName = 'ModalDescription';

// Attach to main component for namespacing
Modal.Step = Step;
Modal.Title = Title;
Modal.Description = Description;

export default Modal;
