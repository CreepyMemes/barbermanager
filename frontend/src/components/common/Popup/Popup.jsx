import styles from './Popup.module.scss';
import Card from '@components/common/Card/Card';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';
import { useEffect, useRef } from 'react';

function Popup({ open, onClose, children, className }) {
  const backdropRef = useRef();

  /**
   *  Close when pressing ESC
   */
  useEffect(() => {
    if (!open) return;
    function handleKeyDown(e) {
      if (e.key === 'Escape') onClose?.();
    }
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [open, onClose]);

  /**
   * Click outside to close
   */
  function handleBackdropClick(e) {
    if (e.target === backdropRef.current) onClose?.();
  }

  // Do nothing if popup isn't open
  if (!open) return null;

  return (
    <div
      className={styles.backdrop}
      ref={backdropRef}
      onMouseDown={handleBackdropClick}
      tabIndex={-1} //
    >
      <Card className={styles.popup}>
        <Button
          className={styles.closeBtn}
          type="button"
          onClick={onClose}
          color="animated"
          size="sm"
          aria-label="Close"
        >
          <Icon name="close" size="ty" black />
        </Button>

        {children}
      </Card>
    </div>
  );
}

export default Popup;
