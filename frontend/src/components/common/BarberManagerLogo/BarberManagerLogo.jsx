import styles from './BarberManagerLogo.module.scss';
import Button from '@components/common/Button/Button';

import Logo from '@components/common/Logo/Logo';

export default function BarberManagerLogo({ size = 'md' }) {
  return (
    <Button href="/" size={size} width="content">
      <span className={`${styles.logo} ${styles[size] || ''}`}>
        <Logo name="barbermanager" size={size} />

        <span className={styles.text}>
          Barber<span>Manager</span>
        </span>
      </span>
    </Button>
  );
}
