import { Children } from 'react';
import styles from './Hero.module.scss';

import Image from '@components/common/Image/Image';

function Hero({ children, className }) {
  // Extracts first HeroLeft and HeroRight children by displayName
  const [left, right] = [Left.displayName, Right.displayName].map((name) =>
    Children.toArray(children).find((child) => child.type.displayName === name),
  );

  // Get all classes
  const computedClassName = [styles.hero, className].join(' ');

  return (
    <div className={computedClassName}>
      {left}
      {right}
    </div>
  );
}

// Simple Left and Right subcomponents
const Left = ({ children, className }) => {
  const computedClassName = [styles.left, className].join(' ');
  return <div className={computedClassName}>{children}</div>;
};

/**
 * Accepts background prop for right side. If set, renders it as absolutely positioned background.
 */
const Right = ({ children, className, background }) => {
  const computedClassName = [styles.right, className].join(' ');

  return (
    <div className={computedClassName}>
      {background && <Image className={styles.background} name={background} />}
      {children}
    </div>
  );
};

// Set display names for subcomponent identification
Left.displayName = 'HeroLeft';
Right.displayName = 'HeroRight';

// Attach to main component for namespacing
Hero.Left = Left;
Hero.Right = Right;

export default Hero;
