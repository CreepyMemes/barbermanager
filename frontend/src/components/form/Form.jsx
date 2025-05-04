import styles from './Form.module.css';
import Button from '@components/button/Button';

function Form({ name, quantity, setName, setQuantity, onSubmit }) {
  return (
    <div className={styles.form}>
      <input
        type="text"
        placeholder="Item Name..."
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="number"
        placeholder="Item Quantity..."
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
      />
      <Button onClick={onSubmit}> Add Item </Button>
    </div>
  );
}

export default Form;
