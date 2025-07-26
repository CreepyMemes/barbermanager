import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import { isEmail } from '@utils/utils';
import styles from './Login.module.scss';

import Spinner from '@components/common/Spinner/Spinner';
import Card from '@components/common/Card/Card';
import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Button from '@components/common/Button/Button';
import Error from '@components/common/Error/Error';
import Hero from '@components/ui/Hero/Hero';
import SidePanel from '@components/ui/SidePanel/SidePanel';
import Icon from '@components/common/Icon/Icon';

function Login() {
  const { login, isAuthenticated, isLoggingIn } = useAuth();
  const navigate = useNavigate();

  const [searchParams] = useSearchParams();
  const registered = searchParams.get('registered');

  /**
   * On authentication state change, redirect authenticated users away from login.
   */
  useEffect(() => {
    if (!isLoggingIn && isAuthenticated) navigate('/dashboard', { replace: true });
  }, [isLoggingIn, isAuthenticated, navigate]);

  // Don't show login if redirecting
  if (isAuthenticated) return null;

  /**
   * Fields declaration for this form
   */
  const initialFields = {
    identifier: '',
    password: '',
  };

  /**
   * Handles form submission for login, Determines whether the identifier is an email or username,
   * then attempts to log in with credentials. Displays error messages on failure.
   */
  const handleLogin = async ({ identifier, password }) => {
    const payload = isEmail(identifier) ? { email: identifier, password } : { username: identifier, password };
    await login(payload); // The AuthProvider will redirect due to isAuthenticated update.
  };

  return (
    <>
      {registered && (
        <Card className={styles.registered}>
          <Icon name="email" size="md" black />
          <div>
            <strong>Account created!</strong>
            {registered === '1' && <div>Please check your email to verify your account before logging in.</div>}
            {registered === '2' && <div>You can now log in to your account.</div>}
          </div>
        </Card>
      )}

      <Hero>
        <Hero.Left>
          <SidePanel heading="Welcome back" subheading="Manage your barbershop with ease">
            <SidePanel.Inner>
              <div className={styles.description}>
                <h2>All your barbershop needs in one place</h2>
                <ul className={styles.features}>
                  <li>
                    <Icon name="appointment" size="sm" />
                    <p>Book and manage appointments easily.</p>
                  </li>
                  <li>
                    <Icon name="service" size="sm" />
                    <p>Personalized experience for barbers and clients.</p>
                  </li>
                  <li>
                    <Icon name="review" size="sm" />
                    <p>View and share reviews.</p>
                  </li>
                </ul>
              </div>
            </SidePanel.Inner>

            <SidePanel.Actions>
              <p className={styles.note}>Don&apos;t have an account?</p>

              <Button href="/register" color="secondary" size="md" width="content">
                Sign up!
              </Button>
            </SidePanel.Actions>
          </SidePanel>
        </Hero.Left>

        <Hero.Right background={'background'}>
          <Card className={styles.login}>
            <Form className={styles.loginForm} initialFields={initialFields} onSubmit={handleLogin}>
              <h2 className={styles.label}>Login</h2>

              <Input
                label="Email or username"
                name="identifier"
                type="text"
                autoComplete="username"
                required
                disabled={isLoggingIn}
                size="md"
              />

              <Input
                label="Password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                disabled={isLoggingIn}
                size="md"
              />

              <Button
                className={styles.loginBtn}
                type="submit"
                color="primary"
                size="md"
                disabled={isLoggingIn}
                wide //
              >
                <span className={styles.line}>
                  {isLoggingIn ? (
                    <>
                      <Spinner size={'sm'} /> Logging in...
                    </>
                  ) : (
                    'Login'
                  )}
                </span>
              </Button>

              <Button className={styles.forgotBtn} href="/reset-password" size="sm" color="link">
                Forgot password?
              </Button>

              <Error />
            </Form>
          </Card>
        </Hero.Right>
      </Hero>
    </>
  );
}

export default Login;
