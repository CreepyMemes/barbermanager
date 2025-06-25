import { useState } from 'react';
import FormContext from '@contexts/FormContext';
import styles from './Form.module.scss';

export default function Form({ label, initialFields, onSubmit, children }) {
  const [fields, setFields] = useState(initialFields);
  const [error, setError] = useState('');

  /**
   * Handles changes in the input fields by updating local state.
   */
  const handleChange = (event) => {
    setFields((prev) => ({ ...prev, [event.target.name]: event.target.value }));
  };

  /**
   * Handles form submission for login, Determines whether the identifier is an email or username,
   * then attempts to log in with credentials. Displays error messages on failure.
   */
  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      await onSubmit(fields);
    } catch (error) {
      setError(error?.response?.data?.detail || error?.message || 'Login failed');
    }
  };

  return (
    <FormContext.Provider value={{ fields, handleChange, error, setError }}>
      <form className={styles.form} onSubmit={handleSubmit} autoComplete="on">
        <h2 className={styles.label}>{label}</h2>

        {children}
      </form>
    </FormContext.Provider>
  );
}
