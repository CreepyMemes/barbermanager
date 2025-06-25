import { useEffect } from 'react';
import { useAuth } from '@hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import { isEmail } from '@utils/utils';
import styles from './LoginPage.module.scss';

import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Button from '@components/common/Button/Button';
import Error from '@components/common/Error/Error';

export default function LoginPage() {
  const { login, loading, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  /**
   * On authentication state change, redirect authenticated users away from login.
   */
  useEffect(() => {
    if (isAuthenticated) navigate('/dashboard', { replace: true });
  }, [isAuthenticated, navigate]);

  /**
   * Handles form submission for login, Determines whether the identifier is an email or username,
   * then attempts to log in with credentials. Displays error messages on failure.
   */
  const handleLoginSubmit = async ({ identifier, password }) => {
    const payload = isEmail(identifier) ? { email: identifier, password } : { username: identifier, password };
    await login(payload); // The AuthProvider will redirect due to isAuthenticated update.
  };

  return (
    <div className={styles.loginContainer}>
      <Form label="login" initialFields={{ identifier: '', password: '' }} onSubmit={handleLoginSubmit}>
        <Input
          label="Username or Email:"
          name="identifier"
          type="text"
          autoComplete="username"
          required
          disabled={loading}
        />

        <Input
          label="Password:"
          name="password"
          type="password"
          autoComplete="current-password"
          required
          disabled={loading}
        />

        <Button type="submit" size="lg" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </Button>

        <Error />
      </Form>
    </div>
  );
}
