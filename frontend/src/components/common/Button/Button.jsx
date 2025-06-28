import { Link } from 'react-router-dom';
import { camelizeStyle } from '@utils/utils';
import styles from './Button.module.scss';

function Button({ children, onClick, disabled, type = 'button', href, size = 'md', color, width = 'full', className }) {
  // Get all style classes into a string
  const computedClassName =
    className || [styles.button, styles[size], styles[color], styles[camelizeStyle('width', width)]].join(' ');

  if (href) {
    // Use <Link> for internal links, <a> for external
    const isInternal = href.startsWith('/'); // crude check, improve as needed
    if (isInternal) {
      return (
        <Link
          className={computedClassName}
          to={href}
          // Extra props: aria-disabled etc. as needed
          tabIndex={disabled ? -1 : undefined}
          onClick={disabled ? (e) => e.preventDefault() : onClick}
        >
          {children}
        </Link>
      );
    }
    return (
      <a
        className={computedClassName}
        href={href}
        aria-disabled={disabled}
        tabIndex={disabled ? -1 : undefined}
        onClick={disabled ? (e) => e.preventDefault() : onClick}
        target="_blank" // maybe for external?
        rel="noopener noreferrer"
      >
        {children}
      </a>
    );
  }

  return (
    <button className={computedClassName} type={type} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}

export default Button;
