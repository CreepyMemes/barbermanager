import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import { isEmail } from '@utils/utils';
import styles from './Login.module.scss';

import FormProvider from '@providers/FormProvider';
import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Button from '@components/common/Button/Button';
import Error from '@components/common/Error/Error';
import Spinner from '@components/common/Spinner/Spinner';

function Login() {
  const { login, loading, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  /**
   * On authentication state change, redirect authenticated users away from login.
   */
  useEffect(() => {
    if (!loading && isAuthenticated) navigate('/dashboard', { replace: true });
  }, [isAuthenticated, loading, navigate]);

  // Don't show login if athenticated
  if (isAuthenticated) return null;

  /**
   * Handles form submission for login, Determines whether the identifier is an email or username,
   * then attempts to log in with credentials. Displays error messages on failure.
   */
  const handleLoginSubmit = async ({ identifier, password }) => {
    const payload = isEmail(identifier) ? { email: identifier, password } : { username: identifier, password };
    await login(payload); // The AuthProvider will redirect due to isAuthenticated update.
  };

  return (
    <div className={styles.login}>
      <FormProvider initialFields={{ identifier: '', password: '' }} onSubmit={handleLoginSubmit}>
        <Form label="Login">
          <Input
            label="Email or username"
            name="identifier"
            type="text"
            autoComplete="username"
            required
            disabled={loading}
            size="md"
          />

          <Input
            label="Password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            disabled={loading}
            size="md"
          />

          <Button className={styles.loginBtn} type="submit" size="md" disabled={loading} wide color="primary">
            <span className={styles.line}>
              {loading ? (
                <>
                  <Spinner size={'sm'} /> Logging in...
                </>
              ) : (
                'Login'
              )}
            </span>
          </Button>
          <Error />
        </Form>
      </FormProvider>
    </div>
  );
}

export default Login;
