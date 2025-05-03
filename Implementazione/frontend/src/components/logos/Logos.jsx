import styles from './Logos.module.css';
import reactLogo from '@assets/react.svg';
import BarberManagerLogo from '/logo.png';
function Logos() {
  return (
    <div>
      <a href="" target="_blank">
        <img src={BarberManagerLogo} className={styles.logo} alt="BarberManager logo" />
      </a>
      <a href="https://react.dev" target="_blank">
        <img src={reactLogo} className={`${styles.logo} ${styles.react}`} alt="React logo" />
      </a>
    </div>
  );
}

export default Logos;
