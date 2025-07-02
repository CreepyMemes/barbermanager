import { Children } from 'react';
import styles from './Hero.module.scss';

function Hero({ children }) {
  // Extracts first HeroLeft and HeroRight children by displayName
  const [left, right] = ['HeroLeft', 'HeroRight'].map((name) =>
    Children.toArray(children).find((child) => child.type.displayName === name),
  );

  return (
    <div className={styles.hero}>
      {left}
      {right}
    </div>
  );
}

// Simple Left and Right subcomponents
const Left = ({ children, className }) => {
  const computedClassName = [styles.left, className].join(' ');
  return <aside className={computedClassName}>{children}</aside>;
};

const Right = ({ children, className }) => {
  const computedClassName = [styles.right, className].join(' ');
  return <main className={computedClassName}>{children}</main>;
};

// Set display names for subcomponent identification
Left.displayName = 'HeroLeft';
Right.displayName = 'HeroRight';

// Attach to main component for namespacing (Hero.Left, Hero.Right)
Hero.Left = Left;
Hero.Right = Right;

export default Hero;
