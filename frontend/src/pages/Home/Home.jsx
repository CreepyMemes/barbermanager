import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import styles from './Home.module.scss';

import Spinner from '@components/common/Spinner/Spinner';
import Button from '@components/common/Button/Button';
import Hero from '@components/ui/Hero/Hero';
import SidePanel from '@components/ui/SidePanel/SidePanel';
import Icon from '@components/common/Icon/Icon';

function Home() {
  const { isAuthenticated, isLoggingOut } = useAuth();
  const navigate = useNavigate();

  /**
   * On authentication state change, redirect authenticated users away from home.
   */
  useEffect(() => {
    if (!isLoggingOut && isAuthenticated) navigate('/dashboard', { replace: true });
  }, [isAuthenticated, isLoggingOut, navigate]);

  // Don't show landing if redirecting
  if (isLoggingOut || isAuthenticated) return <Spinner />;

  return (
    <Hero>
      <Hero.Left>
        <SidePanel heading="Barbershop management platform">
          <SidePanel.Inner>
            <ul className={styles.features}>
              <li>
                <span className={styles.featureTitle}>
                  <Icon name="appointment" size="sm" />
                  <p>Effortless Appointments</p>
                </span>
                <span>Let customers book themselves. Manage your schedule with ease.</span>
              </li>

              <li>
                <span className={styles.featureTitle}>
                  <Icon name="client" size="sm" />
                  <p>Customer Relationship</p>
                </span>
                <span>Track client history, notes, and preferences for unbeatable service.</span>
              </li>

              <li>
                <span className={styles.featureTitle}>
                  <Icon name="review" size="sm" /> <p>Reviews & Growth</p>
                </span>
                <span>Collect feedback, drive loyalty and get insights to grow your business.</span>
              </li>
            </ul>
          </SidePanel.Inner>

          <SidePanel.Actions>
            <Button href="/register" size="lg" color="secondary">
              Get started
            </Button>

            <p className={styles.note}>No credit card required. Cancel anytime.</p>
          </SidePanel.Actions>
        </SidePanel>
      </Hero.Left>

      <Hero.Right background={'splash'}></Hero.Right>
    </Hero>
  );
}

export default Home;
