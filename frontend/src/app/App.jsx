import { useState } from 'react';
// import styles from './App.module.scss';
import Login from '../pages/Login';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <div>
      {loggedIn ? (
        <Login onLogin={() => setLoggedIn(true)}></Login>
      ) : (
        <Login onLogin={() => setLoggedIn(false)}></Login>
      )}
    </div>
  );
}

export default App;
