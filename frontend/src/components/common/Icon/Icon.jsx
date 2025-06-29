import icons from '@assets/icons';
import styles from './Icon.module.scss';

function Icon({ name, size = 'md', color }) {
  const SvgIcon = icons[name];
  if (!SvgIcon) return null;

  // Pass `size` as modifier class to wrapper
  return (
    <span className={`${styles.wrapper} ${styles[size]}`}>
      <SvgIcon width="100%" height="100%" className={styles.icon} style={color ? { color } : undefined} />
    </span>
  );
}

export default Icon;
