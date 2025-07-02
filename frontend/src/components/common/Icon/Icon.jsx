import icons from '@assets/icons';
import styles from './Icon.module.scss';

function Icon({ name, size = 'md', black = false }) {
  const SvgIcon = icons[name];
  if (!SvgIcon) return null;

  // Get all style classes into a string
  const computedClassName = [styles.wrapper, styles[size]].join(' ');

  return (
    <span className={computedClassName}>
      <SvgIcon width="100%" height="100%" className={styles.icon} style={black ? { filter: 'invert(1)' } : undefined} />
    </span>
  );
}

export default Icon;
