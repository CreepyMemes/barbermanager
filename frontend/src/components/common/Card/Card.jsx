import styles from './Card.module.scss';

function Card({ className, children }) {
  // Get all style classes into a string
  const computedClassName = [className, styles.card].join(' ');

  return <div className={computedClassName}>{children}</div>;
}

export default Card;
