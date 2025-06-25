import styles from './Button.module.scss';

function Button({ children, onClick, disabled, type = 'button', href }) {
  if (href) {
    return (
      <a
        className={styles.button}
        href={href}
        onClick={onClick}
        aria-disabled={disabled} // for accessibility
        tabIndex={disabled ? -1 : 0}
        style={disabled ? { pointerEvents: 'none', opacity: 0.6 } : {}}
      >
        {children}
      </a>
    );
  }

  return (
    <button className={styles.button} type={type} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}

export default Button;
