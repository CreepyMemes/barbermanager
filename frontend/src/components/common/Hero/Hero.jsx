import { Children } from 'react';
import styles from './Hero.module.scss';

function Hero({ children }) {
  const left = Children.toArray(children).find((child) => child.type.displayName === 'HeroLeft');
  const right = Children.toArray(children).find((child) => child.type.displayName === 'HeroRight');

  return (
    <div className={styles.hero}>
      <div className={`${styles.left} ${styles.centerVertical}`}>
        <div className={styles.centerHorizontal}>{left}</div>
      </div>

      <div className={`${styles.right} ${styles.centerVertical}`}>
        <div className={styles.centerHorizontal}>{right}</div>
      </div>
    </div>
  );
}

function Left({ children }) {
  return <>{children}</>;
}

function Right({ children }) {
  return <>{children}</>;
}

Left.displayName = 'HeroLeft';
Right.displayName = 'HeroRight';
Hero.Left = Left;
Hero.Right = Right;

export default Hero;
