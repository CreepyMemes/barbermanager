import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import { isEmail } from '@utils/utils';
import styles from './Login.module.scss';

import Card from '@components/common/Card/Card';
import Logo from '@components/common/Logo/Logo';

import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Button from '@components/common/Button/Button';
import Error from '@components/common/Error/Error';
import Spinner from '@components/common/Spinner/Spinner';
import Hero from '@components/common/Hero/Hero';
import Icon from '@components/common/Icon/Icon';

function Login() {
  const { login, loading, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  /**
   * On authentication state change, redirect authenticated users away from login.
   */
  useEffect(() => {
    if (!loading && isAuthenticated) navigate('/dashboard', { replace: true });
  }, [isAuthenticated, loading, navigate]);

  // Don't show login if redirecting
  if (isAuthenticated && loading) return <Spinner />;

  /**
   * Handles form submission for login, Determines whether the identifier is an email or username,
   * then attempts to log in with credentials. Displays error messages on failure.
   */
  const handleLogin = async ({ identifier, password }) => {
    const payload = isEmail(identifier) ? { email: identifier, password } : { username: identifier, password };
    await login(payload); // The AuthProvider will redirect due to isAuthenticated update.
  };

  return (
    <Hero>
      <Hero.Left>
        <section className={styles.left}>
          <h1 className={styles.heading}>Welcome back</h1>

          <div className={styles.container}>
            <Logo size="hg" split />

            <div className={styles.description}>
              <h2>Manage your barbershop with ease</h2>

              <ul className={styles.features}>
                <li>
                  <Icon name="barber" size="sm" />
                  <p>Run your barbershop smoothly.</p>
                </li>
                <li>
                  <Icon name="appointment" size="sm" />
                  <p>Book. Manage. Grow.</p>
                </li>
                <li>
                  <Icon name="client" size="sm" />
                  <p>Appointments, clients, reviews. All in one place.</p>
                </li>
              </ul>
            </div>
          </div>

          <div className={styles.actions}>
            <p className={styles.note}>Don&apos;t already have an account?</p>
            <Button href="/register" color="secondary" size="md" width="content">
              Sign up!
            </Button>
          </div>
        </section>
      </Hero.Left>

      <Hero.Right>
        <Card className={styles.login}>
          <Form className={styles.loginForm} initialFields={{ identifier: '', password: '' }} onSubmit={handleLogin}>
            <h2 className={styles.label}>Login</h2>

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

            <Button className={styles.forgotBtn} href="/reset-password" size="sm" color="link">
              Forgot password?
            </Button>

            <Error />
          </Form>
        </Card>
      </Hero.Right>
    </Hero>
  );
}

export default Login;
