import styles from './Logo.module.css';
import ManageBarberLogo from '/logo.png';

function Logo() {
  return (
    <div>
      <a href="#" target="_blank">
        <img src={ManageBarberLogo} className={styles.logo} alt="ManageBarber logo" />
      </a>
    </div>
  );
}

export default Logo;
