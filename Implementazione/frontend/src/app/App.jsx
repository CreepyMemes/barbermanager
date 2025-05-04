import styles from './App.module.css';
import Logo from '@components/logo/Logo';
import Form from '@components/form/Form';
import Item from '@components/item/Item';
import { useEffect, useState } from 'react';

const apiUrl = 'http://127.0.0.1:8000/'; // Warning this only works on the host machine

function App() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/items/`);
      const data = await response.json();
      setItems(data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <Logo />
      <h1>BarberManager</h1>
      <Form />
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
