import styles from './StatCard.module.scss';

import Card from '@components/common/Card/Card';
import Icon from '@components/common/Icon/Icon';

function StatCard({ icon, label, value, children, className = '' }) {
  // Get all style classes into a string
  const computedClassName = [className, styles.card].join(' ');

  return (
    <Card className={computedClassName}>
      <div className={styles.icon}>
        <Icon name={icon} size="sm" black />
      </div>

      <div className={styles.content}>
        <div className={styles.label}>{label}</div>
        {children ? children : <div className={styles.value}>{value}</div>}
      </div>
    </Card>
  );
}

export default StatCard;
