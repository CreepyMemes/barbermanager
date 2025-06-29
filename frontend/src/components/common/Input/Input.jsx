import styles from './Input.module.scss';
import { useForm } from '@hooks/useForm';

export default function Input({ label, type, name, required, autoComplete, disabled, size }) {
  const { fields, handleChange } = useForm();

  // Get all style classes into a string
  const className = [styles.input, styles[size]].join(' ');

  return (
    <label className={styles.label}>
      {label}
      <input
        className={className}
        name={name}
        type={type}
        value={fields[name]}
        onChange={handleChange}
        autoComplete={autoComplete}
        required={required}
        disabled={disabled}
      />
    </label>
  );
}
