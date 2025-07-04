import styles from './Spinner.module.scss';

function Spinner({ size = 'lg' }) {
  // Get all style classes into a string
  const className = [styles.spinner, styles[size]].join(' ');

  return (
    <div className={styles.spinnerWrapper}>
      <div className={className} />
    </div>
  );
}

export default Spinner;
