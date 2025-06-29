import { Outlet } from 'react-router-dom';
import styles from './Page.module.scss';

function Page() {
  return (
    <div className={styles.page}>
      <Outlet />
    </div>
  );
}

export default Page;
