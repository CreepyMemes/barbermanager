import styles from './Logo.module.scss';
import Button from '@components/common/Button/Button';

import Icon from '@components/common/Icon/Icon';

export default function Logo({ size = 'md' }) {
  return (
    <Button href="/" size={size} width="content" color="animated">
      <span className={`${styles.logo} ${styles[size] || ''}`}>
        <Icon name="barbermanager" size={size} />

        <span className={styles.text}>
          Barber<span>Manager</span>
        </span>
      </span>
    </Button>
  );
}
