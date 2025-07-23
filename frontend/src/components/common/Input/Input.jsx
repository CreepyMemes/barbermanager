import { useState, useRef } from 'react';
import { useForm } from '@hooks/useForm';
import styles from './Input.module.scss';

import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';

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
  accept, // for file inputs
}) {
  const { fields, handleChange } = useForm();
  const [showPassword, setShowPassword] = useState(false);
  const inputRef = useRef(null);

  // Get all style classes into a string
  const className = [styles.input, styles[size]].join(' ');

  // File upload functionality
  const inputId = `input-${name}`;

  // Password eye toggle functionality
  const showEye = type === 'password' && !hide;
  const inputType = showEye && showPassword ? 'text' : type;

  /**
   * Handler for opening the window to upload a file when upload button is clicked
   */
  const handleUploadButton = () => {
    if (!disabled && inputRef.current) {
      inputRef.current.click();
    }
  };

  /**
   * Handler for file change and update to form context
   */
  const handleFileChange = (e) => {
    handleChange({
      target: {
        name,
        value: e.target.files[0] || null, // File object is "e.target.files[0]"
      },
    });
  };

  // Handler for toggling the password hiding
  const handleToggleShow = () => {
    setShowPassword((v) => !v);
  };

  // If input type is a file
  if (type === 'file') {
    return (
      <div className={styles.fileInput}>
        <input
          className={styles.fileInputField}
          ref={inputRef}
          id={inputId}
          type="file"
          name={name}
          accept={accept}
          disabled={disabled}
          onChange={handleFileChange}
          tabIndex={-1}
          aria-hidden="true"
        />

        <Button
          className={styles.uploadButton}
          type="button"
          color="primary"
          size="md"
          disabled={disabled}
          onClick={handleUploadButton}
          tabIndex={0}
          aria-controls={inputId}
        >
          <Icon name="plus" size="ty" />
          <span>{fields[name]?.name || placeholder || 'Choose a file'}</span>
        </Button>
      </div>
    );
  }

  // Normal input (text, number, password, etc.)
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
            disabled={disabled}
          >
            <Icon name={showPassword ? 'eye_open' : 'eye_closed'} size="sm" black />
          </Button>
        )}
      </span>
    </label>
  );
}

export default Input;
