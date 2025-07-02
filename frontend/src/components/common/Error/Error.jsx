import styles from './Error.module.scss';
import { useForm } from '@hooks/useForm';

function Error() {
  const { error } = useForm();
  if (!error) return null;

  return <div className={styles.error}>{error}</div>;
}

export default Error;
