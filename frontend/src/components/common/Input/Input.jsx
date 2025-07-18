import styles from './Input.module.scss';
import { useForm } from '@hooks/useForm';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';
import { useState } from 'react';

function Input({
  label,
  type = 'text',
  min,
  step,
  name,
  required,
  autoComplete,
  disabled,
  size = 'md',
  placeholder,
  hide,
}) {
  const { fields, handleChange } = useForm();
  const [showPassword, setShowPassword] = useState(false);

  // Get all style classes into a string
  const className = [styles.input, styles[size]].join(' ');

  // Handler for the eye button
  function handleToggleShow() {
    setShowPassword((v) => !v);
  }

  const showEye = type === 'password' && !hide;
  const inputType = showEye && showPassword ? 'text' : type;

  return (
    <label className={styles.label}>
      {label}
      <span className={styles.inputWrapper}>
        <input
          className={className}
          name={name}
          type={inputType}
          min={min}
          step={step}
          value={fields[name]}
          onChange={handleChange}
          autoComplete={autoComplete}
          required={required}
          disabled={disabled}
          placeholder={placeholder}
        />

        {/* Only show eye button if password */}
        {showEye && (
          <Button
            className={styles.eyeBtn}
            type="button"
            onClick={handleToggleShow}
            tabIndex={-1}
            color="animated"
            size="sm"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
            disabled={disabled} // Optionally disabled if the field is disabled
          >
            <Icon name={showPassword ? 'eye_open' : 'eye_closed'} size="sm" black />
          </Button>
        )}
      </span>
    </label>
  );
}

export default Input;
