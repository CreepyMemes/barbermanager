import styles from './Logos.module.css';
import reactLogo from '@assets/react.svg';
import ManageBarberLogo from '/logo.png';
function Logos() {
  return (
    <div>
      <a href="" target="_blank">
        <img src={ManageBarberLogo} className={styles.logo} alt="ManageBarber logo" />
      </a>
      <a href="https://react.dev" target="_blank">
        <img src={reactLogo} className={`${styles.logo} ${styles.react}`} alt="React logo" />
      </a>
    </div>
  );
}

export default Logos;
