import styles from './Spinner.module.scss';

export default function Spinner({ size = 48, label = 'Loading...' }) {
  return (
    <div className={styles.spinnerWrapper} role="status">
      <div className={styles.spinner} style={{ width: size, height: size }} />
      <span className={styles.srOnly}>{label}</span>
    </div>
  );
}
