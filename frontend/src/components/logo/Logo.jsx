import styles from './Logo.module.css';
import BarberManagerLogo from '/logo.png';

function Logo() {
  return (
    <div>
      <a href="#" target="_blank">
        <img src={BarberManagerLogo} className={styles.logo} alt="BarberManager logo" />
      </a>
    </div>
  );
}

export default Logo;
