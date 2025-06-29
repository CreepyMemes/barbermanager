import styles from './Logo.module.scss';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';

function Logo({ className, size = 'md', split, button }) {
  // Classes for the span inside the Button
  const computedClassName = [className, styles.logo, styles[size], split ? styles.split : ''].join(' ');

  const content = (
    <>
      <Icon name="barbermanager" size={size} />
      <span className={styles.text}>
        <span className={styles.light}>Barber</span>
        <span className={styles.dark}>Manager</span>
      </span>
    </>
  );

  if (button) {
    return (
      <Button href="/" size={size} width="content" color="animated">
        <span className={computedClassName}>{content}</span>
      </Button>
    );
  }

  // Otherwise return just the span (with no Button wrapper)
  return <span className={computedClassName}>{content}</span>;
}

export default Logo;
