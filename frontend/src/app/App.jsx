import styles from './App.module.css';
import Logo from '@components/logo/Logo';
import Form from '@components/form/Form';
import { useEffect, useState } from 'react';

function App() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/items/');
      const data = await response.json();
      console.log(data);
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
    </>
  );
}

export default App;
