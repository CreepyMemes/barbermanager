import App from '@app/App';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.scss';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
