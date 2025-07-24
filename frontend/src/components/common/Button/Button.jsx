import { useState, cloneElement, isValidElement, Children } from 'react';
import { Link, NavLink } from 'react-router-dom';
import styles from './Button.module.scss';

function Button({
  children,
  onClick,
  disabled,
  type = 'button',
  href,
  nav = false,
  activeClassName,
  size,
  wide,
  color,
  className,
  autoIconInvert = false, // <-- new prop, default false
}) {
  const [hovered, setHovered] = useState(false);

  const isIconElement = (child) => {
    const type = child.type;
    return type && ((type.displayName && type.displayName === 'Icon') || (type.name && type.name === 'Icon'));
  };

  /**
   * Enhances currently present black prop on Icon children, if autoIconInvert is true
   */
  const composedChildren = autoIconInvert
    ? Children.map(children, (child) => {
        if (isValidElement(child) && isIconElement(child) && typeof child.props.black !== 'undefined') {
          return cloneElement(child, { black: !hovered });
        }
        return child;
      })
    : children;

  /**
   * These props let all variants get hover
   */
  const hoverProps = autoIconInvert
    ? {
        onMouseEnter: () => setHovered(true),
        onMouseLeave: () => setHovered(false),
      }
    : {};

  // Get all style classes into a string
  const computedClassName = [className, styles.button, styles[size], styles[color], wide ? styles.wide : ''].join(' ');

  if (href) {
    // Check if link is internal with a crude check (works for now)
    if (href.startsWith('/')) {
      // If 'nav' prop is true, render NavLink for active awareness
      if (nav) {
        return (
          <NavLink
            to={href}
            className={({ isActive }) => [computedClassName, isActive ? activeClassName : ''].filter(Boolean).join(' ')}
            tabIndex={disabled ? -1 : undefined}
            aria-disabled={disabled}
            onClick={disabled ? (e) => e.preventDefault() : onClick}
            {...hoverProps}
          >
            {composedChildren}
          </NavLink>
        );
      }

      // Otherwise render Link component
      return (
        <Link
          className={computedClassName}
          to={href}
          tabIndex={disabled ? -1 : undefined}
          aria-disabled={disabled}
          onClick={disabled ? (e) => e.preventDefault() : onClick}
          {...hoverProps}
        >
          {composedChildren}
        </Link>
      );
    }

    // If it's an external link, renders default anchor
    return (
      <a
        className={computedClassName}
        href={href}
        aria-disabled={disabled}
        tabIndex={disabled ? -1 : undefined}
        onClick={disabled ? (e) => e.preventDefault() : onClick}
        target="_blank" // maybe for external?
        rel="noopener noreferrer"
        {...hoverProps}
      >
        {composedChildren}
      </a>
    );
  }

  return (
    <button
      className={computedClassName}
      type={type}
      onClick={onClick}
      disabled={disabled}
      {...hoverProps} ///
    >
      {composedChildren}
    </button>
  );
}

export default Button;
