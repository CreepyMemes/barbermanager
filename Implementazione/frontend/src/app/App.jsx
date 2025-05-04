import styles from './App.module.css';
import Logo from '@components/logo/Logo';
import Form from '@components/form/Form';
import Item from '@components/item/Item';
import { useEffect, useState } from 'react';

const apiUrl = 'http://127.0.0.1:8000/'; // Warning this only works on the host machine

function App() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState('');
  const [quantity, setQuantity] = useState(0);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/items/`);
      const items = await response.json();
      setItems(items);
    } catch (error) {
      console.log(error);
    }
  };

  const addItem = async () => {
    const itemData = {
      name,
      quantity,
    };

    try {
      const response = await fetch(`${apiUrl}/api/items/create/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(itemData),
      });

      const newItem = await response.json();
      setItems((prevItems) => [...prevItems, newItem]);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <Logo />
      <h1>BarberManager</h1>
      <Form
        name={name}
        quantity={quantity}
        setName={setName}
        setQuantity={setQuantity}
        onSubmit={addItem}
      />
      <p className={styles.text}> Testing API CRUD operations</p>

      <h2>Items: </h2>
      <div className={styles.itemList}>
        {items.map((item) => (
          <Item key={item.id} item={item}></Item>
        ))}
      </div>
    </>
  );
}

export default App;
