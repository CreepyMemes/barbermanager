import styles from './LoadingSpinner.module.scss';

export default function LoadingSpinner({ size = 48, label = 'Loading...' }) {
  return (
    <div className={styles.spinnerWrapper} role="status" aria-live="polite">
      <div className={styles.spinner} style={{ width: size, height: size }} aria-hidden="true" />
      <span className={styles.srOnly}>{label}</span>
    </div>
  );
}
