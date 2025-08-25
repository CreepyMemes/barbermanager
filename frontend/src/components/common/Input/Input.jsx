import { useState, useRef, useCallback, useEffect } from 'react';
import { useForm } from '@hooks/useForm';
import styles from './Input.module.scss';

import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';

function Input({
  // General use
  type = 'text',
  size = 'md',
  name,
  label,
  placeholder,
  disabled,
  required,

  // For Standard input
  autoComplete,
  hide,
  step,
  min,

  // For file input
  accept,

  // For dropdown and checkbox selections
  fetcher,
  mapOption,
}) {
  const { fields, handleChange } = useForm();

  // Get all style classes into a string
  const className = [styles.input, styles[size]].join(' ');

  // Dropdown & Checkbox options state
  const [selectOptions, setSelectOptions] = useState([]);
  const [selectLoading, setSelectLoading] = useState(false);
  const [selectError, setSelectError] = useState('');

  // Password Input state
  const [showPassword, setShowPassword] = useState(false);

  // File input functionality
  const fileInputRef = useRef(null);
  const fileInputId = `input-${name}`;

  // Password eye toggle functionality
  const showEye = type === 'password' && !hide;
  const inputType = showEye && showPassword ? 'text' : type;

  // The selected item from tthet checkbox input
  const checkboxSelected = Array.isArray(fields[name]) ? fields[name].map(String) : fields[name] ? [String(fields[name])] : [];

  /**
   * Runs the passed fetcher function to get all options for dropdown or checkbox
   */
  const fetchOptions = useCallback(async () => {
    if (!fetcher) return;

    setSelectLoading(true);
    setSelectError('');

    try {
      const options = await fetcher();
      setSelectOptions(mapOption ? options.map(mapOption) : options);
    } catch {
      setSelectOptions([]);
      setSelectError('Failed to load options');
    } finally {
      setSelectLoading(false);
    }
  }, [fetcher, mapOption]);

  /**
   * Handles changing values based on selected checkboxes
   */
  const handleCheckbox = (e) => {
    const id = e.target.value;
    let newSelected;

    if (e.target.checked) {
      newSelected = [...checkboxSelected, id];
    } else {
      newSelected = checkboxSelected.filter((sid) => sid !== id);
    }

    // Synthesize event for useForm's handleChange
    handleChange({ target: { name, value: newSelected } });
  };

  /**
   * Fetches the passed fetcher function on mount if on dropdown mode
   */
  useEffect(() => {
    if ((type === 'dropdown' || type === 'checkbox') && fetcher) {
      fetchOptions();
    }
  }, [type, fetchOptions, fetcher]);

  /**
   * Handler for opening the window to upload a file when upload button is clicked
   */
  const handleUploadButton = () => {
    if (!disabled && fileInputRef.current) {
      fileInputRef.current.click();
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

  // --- Checkbox Selection ---
  if (type === 'checkbox') {
    return (
      <fieldset>
        <legend>{label}</legend>

        {selectOptions.map((option) => (
          <label key={option.key} style={{ display: 'block' }}>
            <input
              type="checkbox"
              value={option.key}
              checked={checkboxSelected.includes(option.key)}
              onChange={handleCheckbox}
              disabled={selectLoading || disabled} //
            />
            {option.value}
          </label>
        ))}
        {selectOptions.length === 0 && !selectLoading && !selectError && <div>No options</div>}

        {selectLoading && <span>Loading…</span>}
        {selectError && <span>{selectError}</span>}
      </fieldset>
    );
  }

  // --- Dropdown Selection ---
  if (type === 'dropdown') {
    return (
      <label>
        {label}
        <select
          className={className}
          name={name}
          value={fields[name] || ''}
          onChange={handleChange}
          disabled={selectLoading || disabled}
          required={required} //
        >
          <option value="">{placeholder || 'Select...'}</option>

          {selectOptions.map((option) => (
            <option key={option.key} value={option.key}>
              {option.value}
            </option>
          ))}
        </select>

        {selectLoading && <span className={styles.loading}>Loading...</span>}
        {selectError && <span className={styles.error}>{selectError}</span>}
      </label>
    );
  }

  // --- File Input ---
  if (type === 'file') {
    return (
      <div className={styles.fileInput}>
        <input
          className={styles.fileInputField}
          ref={fileInputRef}
          id={fileInputId}
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
          aria-controls={fileInputId}
        >
          <Icon name="plus" size="ty" />
          <span>{fields[name]?.name || placeholder || 'Choose a file'}</span>
        </Button>
      </div>
    );
  }

  // --- Standard Input (text, number, password, etc.) ---
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
            onClick={() => setShowPassword((v) => !v)}
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
