import Button from '@components/common/Button/Button';
import styles from './HomePage.module.scss';

export default function HomePage() {
  return (
    <div className={styles.homeContainer}>
      <h1>Welcome to Barber Manager!</h1>
      <p>This page is styled using a SASS module 🎉</p>
      <Button href="/login/">Login</Button>
    </div>
  );
}
