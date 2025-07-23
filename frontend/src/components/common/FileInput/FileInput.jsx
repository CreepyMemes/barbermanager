import { useRef } from 'react';
import { useForm } from '@hooks/useForm';
import styles from './FileInput.module.scss';

import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';

function FileInput({ name, disabled, accept }) {
  const { fields, handleChange } = useForm();
  const inputRef = useRef();
  const inputId = `file-input-${name}`;

  /**
   * Handles opening the window to upload a file after clicking the button
   */
  const onButtonClick = () => {
    if (!disabled && inputRef.current) {
      inputRef.current.click();
    }
  };

  /**
   * Handles file change and update form context
   * The File object is "e.target.files[0]"
   */
  const onFileChange = (e) => {
    handleChange({
      target: {
        name,
        value: e.target.files[0] || null,
      },
    });
  };

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
        onChange={onFileChange}
        tabIndex={-1}
        aria-hidden="true"
      />

      <Button
        className={styles.uploadButton}
        type="button"
        color="primary"
        size="md"
        disabled={disabled}
        tabIndex={0}
        onClick={onButtonClick}
        aria-controls={inputId}
      >
        <Icon name="plus" size="ty" />
        <span>{fields[name]?.name || 'Choose an image'}</span>
      </Button>
    </div>
  );
}

export default FileInput;
