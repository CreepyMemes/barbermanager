import { Outlet } from 'react-router-dom';
import styles from './DashboardLayout.module.scss';

import Sidebar from '@components/layout/Sidebar/Sidebar';

// TODO: fix layout make header and sidebar outside, and the pages go inside
export default function DashboardLayout() {
  return (
    <div className={styles.layout}>
      <Sidebar />
      <main className={styles.mainContent}>
        <Outlet />
      </main>
    </div>
  );
}
