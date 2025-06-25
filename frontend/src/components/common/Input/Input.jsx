import styles from './Input.module.scss';
import { useForm } from '@hooks/useForm';

export default function Input({ label, type, name, required, autoComplete, loading }) {
  const { fields, handleChange } = useForm();

  return (
    <label className={styles.label}>
      {label}
      <input
        className={styles.input}
        name={name}
        type={type}
        value={fields[name]}
        onChange={handleChange}
        autoComplete={autoComplete}
        required={required}
        disabled={loading}
      />
    </label>
  );
}
