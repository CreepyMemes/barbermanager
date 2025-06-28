import icons from '@assets/icons';
import styles from './Logo.module.scss';

export default function Logo({ name, size = 'md' }) {
  const icon = icons[name];
  if (!icon) return null;

  return <img className={`${styles.icon} ${styles[size] || ''} `} src={icon} alt={`${name} logo`} />;
}
