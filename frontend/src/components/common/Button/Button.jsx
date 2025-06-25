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
  const className = [styles.button, styles[size], styles[color], styles[camelizeStyle('width', width)]].join(' ');

  if (href) {
    return (
      <a
        className={className}
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
    <button className={className} type={type} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}

export default Button;
