import styles from './Form.module.css';
import Button from '@components/button/Button';

function Form() {
  return (
    <div className={styles.form}>
      <input type="text" placeholder="Item Name..." />
      <input type="number" placeholder="Item Quantity..." />
      <Button> Add Item </Button>
    </div>
  );
}

export default Form;
