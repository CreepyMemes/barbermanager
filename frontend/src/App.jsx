import { BrowserRouter } from 'react-router-dom';
import AuthProvider from '@providers/AuthProvider';
import AppRoutes from '@routes/AppRoutes';

import Header from '@components/layout/Header/Header';
import Footer from '@components/layout/Footer/Footer';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Header />
        <AppRoutes />
        <Footer />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
