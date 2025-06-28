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
        {/* Render sidebar only if authenticated */}
        {isAuthenticated && (
          <aside className={styles.sidebarArea}>
            <Sidebar />
          </aside>
        )}

        <main className={styles.mainArea}>
          <Outlet /> {/* Renders the current route inside the layout */}
        </main>
      </div>

      <Footer />
    </div>
  );
}
