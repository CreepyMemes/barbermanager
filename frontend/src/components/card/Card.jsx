import { useState } from 'react';
import styles from './Card.module.css';

function Card() {
  const [count, setCount] = useState(0);

  return (
    <div className={styles.card}>
      <button onClick={() => setCount((count) => count + 1)}>count is {count}</button>
      <p>
        Edit <code>src/app/App.jsx</code> and save to test HMR
      </p>
    </div>
  );
}

export default Card;
