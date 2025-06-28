import icons from '@assets/icons';
import styles from './Icon.module.scss';

export default function Icon({ name, size = 'md' }) {
  const icon = icons[name];
  if (!icon) return null;

  return <img className={`${styles.icon} ${styles[size] || ''} `} src={icon} alt={`${name} logo`} />;
}
