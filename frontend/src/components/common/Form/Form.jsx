import { useContext } from 'react';
import styles from './Form.module.scss';
import FormContext from '@contexts/FormContext';

export default function Form({ label, children }) {
  const { handleSubmit } = useContext(FormContext);

  return (
    <form className={styles.form} onSubmit={handleSubmit} autoComplete="on">
      {label && <h2 className={styles.label}>{label}</h2>}
      {children}
    </form>
  );
}
