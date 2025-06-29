import icons from '@assets/icons';
import styles from './Icon.module.scss';

function Icon({ name, size = 'md' }) {
  const SvgIcon = icons[name];
  if (!SvgIcon) return null;

  // Get all style classes into a string
  const computedClassName = [styles.wrapper, styles[size], styles[size]].join(' ');

  return (
    <span className={computedClassName}>
      <SvgIcon width="100%" height="100%" className={styles.icon} />
    </span>
  );
}

export default Icon;
