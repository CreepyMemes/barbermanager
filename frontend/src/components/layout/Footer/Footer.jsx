import { Link } from 'react-router-dom';
import styles from './Footer.module.scss';

import ManageBarberLogo from '@components/common/ManageBarberLogo/ManageBarberLogo';

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <ManageBarberLogo size="sm" />

      <ul className={styles.links}>
        <li>
          <Link to="/">Home</Link>
        </li>

        <li>
          <Link to="/dashboard">Dashboard</Link>
        </li>

        <li>
          <a href="https://github.com/s1lentCommit/manageBarber" target="_blank" rel="noopener noreferrer">
            Github
          </a>
        </li>
      </ul>

      <div className={styles.copyright}>&copy; {new Date().getFullYear()} s1lentCommit. All rights reserved.</div>
    </footer>
  );
}
