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
      <Header />
      <div className={styles.shellMainArea}>
        {isAuthenticated && (
          <aside className={styles.sidebarArea}>
            <Sidebar />
          </aside>
        )}
        <main className={styles.mainArea}>
          <Outlet /> {/* <-- This renders the current route/page inside the layout */}
        </main>
      </div>
      <Footer />
    </div>
  );
}
