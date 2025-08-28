// Input.jsx
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
  reloadKey,

  // For rating input
  maxStars = 5,
  allowClear = false,
}) {
  const { fields, handleChange } = useForm();

  // Get all style classes into a string
  const className = [styles.input, styles[size]].join(' ');

  // Dropdown & Checkbox options state
  const [selectOptions, setSelectOptions] = useState([]);
  const [selectLoading, setSelectLoading] = useState(false);
  const [selectError, setSelectError] = useState('');
  const [hasLoaded, setHasLoaded] = useState(false);

  // Rating Input state
  const [hoverValue, setHoverValue] = useState(0);

  // Rating Input functionality
  const numericValue = Number(fields[name]) || 0;
  const activeValue = hoverValue || numericValue;

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
      setHasLoaded(true);
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
   * Resets cache if the relevant dependencies change
   */
  useEffect(() => {
    setHasLoaded(false);
    setSelectOptions([]);
    setSelectError('');
  }, [reloadKey]);

  /**
   * Fetches the passed fetcher function on mount if on dropdown mode
   */
  useEffect(() => {
    if ((type === 'dropdown' || type === 'checkbox') && fetcher && !hasLoaded) {
      fetchOptions();
    }
  }, [type, fetcher, fetchOptions, hasLoaded]);

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

  const setRatingValue = (val) => {
    handleChange({ target: { name, value: val } });
  };

  const onClickStar = (val) => {
    if (disabled) return;
    if (allowClear && numericValue === val) {
      setRatingValue(0);
    } else {
      setRatingValue(val);
    }
  };

  // Roving tabindex: only one item is tabbable
  const getRatingTabIndex = (i) => {
    if (disabled) return -1;
    if (numericValue) return numericValue === i ? 0 : -1;
    return i === 1 ? 0 : -1;
  };

  const ratingOnKeyDown = (e, i) => {
    if (disabled) return;
    const key = e.key;
    if (key === 'ArrowRight' || key === 'ArrowUp') {
      e.preventDefault();
      const next = Math.min((numericValue || 0) + 1, maxStars);
      setRatingValue(next);
    } else if (key === 'ArrowLeft' || key === 'ArrowDown') {
      e.preventDefault();
      const prev = Math.max((numericValue || 0) - 1, 1);
      setRatingValue(prev);
    } else if (key === 'Home') {
      e.preventDefault();
      setRatingValue(1);
    } else if (key === 'End') {
      e.preventDefault();
      setRatingValue(maxStars);
    } else if ((key === 'Backspace' || key === 'Delete' || key === '0') && allowClear) {
      e.preventDefault();
      setRatingValue(0);
    } else if (key === ' ' || key === 'Enter') {
      e.preventDefault();
      onClickStar(i);
    }
  };

  // --- Rating Input ---
  if (type === 'rating') {
    return (
      <div className={styles.label}>
        {label}
        <div className={styles.ratingGroup} role="radiogroup" aria-label={label || name} aria-required={required || undefined}>
          {[...Array(maxStars)].map((_, idx) => {
            const i = idx + 1;
            const filled = i <= activeValue;

            return (
              <Button
                key={i}
                type="button"
                color="animated"
                className={`${styles.starBtn} ${filled ? styles.filled : ''} ${disabled ? styles.disabled : ''}`}
                tabIndex={getRatingTabIndex(i)}
                onMouseEnter={() => !disabled && setHoverValue(i)}
                onMouseLeave={() => !disabled && setHoverValue(0)}
                onFocus={() => !disabled && setHoverValue(0)}
                onClick={() => onClickStar(i)}
                onKeyDown={(e) => ratingOnKeyDown(e, i)}
                disabled={disabled}
              >
                <span className={styles.starIcon}>★</span>
              </Button>
            );
          })}
          {allowClear && (
            <Button
              type="button"
              color="animated"
              className={`${styles.clearBtn} ${disabled ? styles.disabled : ''}`}
              onClick={() => !disabled && setRatingValue(0)}
              disabled={disabled}
            >
              Clear
            </Button>
          )}
        </div>
      </div>
    );
  }

  // --- Checkbox Selection ---
  if (type === 'checkbox') {
    return (
      <fieldset className={styles.checkboxGroup} disabled={selectLoading || disabled}>
        <legend className={styles.label}>{label}</legend>
        <div className={styles.checkboxList}>
          {selectOptions.map((option) => (
            <label key={option.key} className={styles.checkboxLabel}>
              <input
                className={styles.checkboxInput}
                type="checkbox"
                value={option.key}
                checked={checkboxSelected.includes(option.key)}
                onChange={handleCheckbox}
                disabled={selectLoading || disabled}
              />
              <span className={styles.checkboxCustom} />
              <span className={`${styles.checkboxText} ${styles[size]}`}>{option.value}</span>
            </label>
          ))}
        </div>

        {!hasLoaded && selectLoading && <span className={styles.loading}>Loading...</span>}
        {selectOptions.length === 0 && !selectLoading && !selectError && <div className={styles.checkboxEmpty}>No options</div>}
        {selectError && <span className={styles.error}>{selectError}</span>}
      </fieldset>
    );
  }

  // --- Dropdown Selection ---
  if (type === 'dropdown') {
    return (
      <label className={styles.label}>
        {label}
        <span className={styles.inputWrapper}>
          <select
            className={`${styles.input} ${styles.select} ${styles[size]}`}
            name={name}
            value={fields[name] || ''}
            onChange={handleChange}
            disabled={selectLoading || disabled}
            required={required}
          >
            <option value="">{!hasLoaded && selectLoading ? 'Loading...' : placeholder || 'Select...'}</option>
            {selectOptions.map((option) => (
              <option key={option.key} value={option.key}>
                {option.value}
              </option>
            ))}
          </select>

          <Icon className={styles.selectArrow} name={'arrow_down'} size="ty" black />
        </span>

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
