import styles from './Spinner.module.scss';

export default function Spinner({ size = 'lg' }) {
  // Get all style classes into a string
  const className = [styles.spinner, styles[size]].join(' ');

  return (
    <div className={styles.spinnerWrapper}>
      <div className={className} />
    </div>
  );
}
