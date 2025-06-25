import styles from './Error.module.scss';
import { useForm } from '@hooks/useForm';

export default function Error() {
  const { error } = useForm();
  if (!error) return null;

  return <div className={styles.error}>{error}</div>;
}
