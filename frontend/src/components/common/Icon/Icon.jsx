import icons from '@assets/icons';
import styles from './Icon.module.scss';

const SIZES = {
  sm: 20,
  md: 28,
  lg: 33,
};

export default function Icon({ name, size = 'md', color }) {
  const SvgIcon = icons[name];

  if (!SvgIcon) return null;

  const pixelSize = SIZES[size] || SIZES.md;

  return <SvgIcon width={pixelSize} height={pixelSize} className={styles.icon} style={color ? { color } : undefined} />;
}
