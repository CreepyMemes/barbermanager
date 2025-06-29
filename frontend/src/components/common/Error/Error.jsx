import styles from './Error.module.scss';
import { useForm } from '@hooks/useForm';

function Error({ size = 'md' }) {
  const { error } = useForm();
  if (!error) return null;

  // Get all style classes into a string
  const className = [styles.error, styles[size]].join(' ');

  return <div className={className}>{error}</div>;
}

export default Error;
