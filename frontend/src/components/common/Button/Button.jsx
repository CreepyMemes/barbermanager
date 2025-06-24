import styles from './Button.module.scss';

function Button({ children, onClick, disabled, type = 'button' }) {
  return (
    <button className={styles.button} type={type} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}

export default Button;
