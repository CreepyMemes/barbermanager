import { useAuth } from '@hooks/useAuth';
import styles from './Layout.module.scss';

import Header from '@components/layout/Header/Header';
import Footer from '@components/layout/Footer/Footer';
import Sidebar from '@components/layout/Sidebar/Sidebar';
import Page from '@components/layout/Page/Page';

export default function Layout() {
  const { isAuthenticated } = useAuth();

  return (
    <div className={styles.app}>
      <Header />

      <div className={styles.content}>
        {isAuthenticated && <Sidebar />}

        <main className={styles.main}>
          <Page />
          <Footer />
        </main>
      </div>
    </div>
  );
}
