import styles from './Tag.module.scss';

const COLOR_MAP = {
  green: styles.green,
  yellow: styles.yellow,
  red: styles.red,
  blue: styles.blue,
};

function Tag({ className, color, children }) {
  // Get all style classes into a string
  const computedClassName = [className, styles.tag, COLOR_MAP[color]].join(' ');

  return <span className={computedClassName}>{children}</span>;
}

export default Tag;
