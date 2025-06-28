import { Outlet } from 'react-router-dom';
import styles from './Page.module.scss';

export default function Page() {
  return (
    <div className={styles.page}>
      <Outlet />
    </div>
  );
}
