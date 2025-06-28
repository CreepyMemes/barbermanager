import { Link } from 'react-router-dom';
import styles from './Footer.module.scss';

import BarberManagerLogo from '@components/common/BarberManagerLogo/BarberManagerLogo';

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <BarberManagerLogo size="sm" />

      <ul className={styles.links}>
        <li>
          <Link to="/">Home</Link>
        </li>

        <li>
          <Link to="/dashboard">Dashboard</Link>
        </li>

        <li>
          <a href="https://github.com/CreepyMemes/barbermanager" target="_blank" rel="noopener noreferrer">
            Github
          </a>
        </li>
      </ul>

      <div className={styles.copyright}>&copy; {new Date().getFullYear()} CreepyMemes. All rights reserved.</div>
    </footer>
  );
}
