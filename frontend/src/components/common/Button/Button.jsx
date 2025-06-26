import styles from './Button.module.scss';

import { camelizeStyle } from '@utils/utils';

function Button({
  children,
  onClick,
  disabled,
  type = 'button',
  href,
  size = 'md',
  color = 'primary',
  width = 'full',
}) {
  // Get all style classes into a string
  const className = [styles.button, styles[size], styles[color], styles[camelizeStyle('width', width)]].join(' ');

  // If button is a link
  if (href) {
    return (
      <a
        className={className}
        href={href}
        onClick={disabled ? (e) => e.preventDefault() : onClick}
        aria-disabled={disabled}
        tabIndex={disabled ? -1 : undefined}
      >
        {children}
      </a>
    );
  }

  return (
    <button className={className} type={type} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}

export default Button;
