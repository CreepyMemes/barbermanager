import styles from './Item.module.css'; // Import the CSS module

function Item({ item }) {
  return (
    <div className={styles.item}>
      <p>Name: {item.name}</p>
      <p>Quantity: {item.quantity}</p>
    </div>
  );
}

export default Item;
