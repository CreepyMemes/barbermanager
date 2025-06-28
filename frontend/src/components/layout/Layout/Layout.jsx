import { useAuth } from '@hooks/useAuth';
import { Outlet } from 'react-router-dom';
import styles from './Layout.module.scss';

import Header from '@components/layout/Header/Header';
import Footer from '@components/layout/Footer/Footer';
import Sidebar from '@components/layout/Sidebar/Sidebar';

export default function Layout() {
  const { isAuthenticated } = useAuth();

  return (
    <div className={styles.appShell}>
      <div className={styles.headerArea}>
        <Header />
      </div>

      <div className={styles.shellMainArea}>
        {isAuthenticated && <Sidebar />}

        <div className={styles.contentArea}>
          <main className={styles.mainArea}>
            <Outlet />
          </main>

          <div className={styles.footerArea}>
            <Footer />
          </div>
        </div>
      </div>
    </div>
  );
}
