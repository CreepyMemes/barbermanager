import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import styles from './RegisterClient.module.scss';
import api from '@api';

import Spinner from '@components/common/Spinner/Spinner';
import Card from '@components/common/Card/Card';
import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Button from '@components/common/Button/Button';
import Error from '@components/common/Error/Error';
import Hero from '@components/ui/Hero/Hero';
import SidePanel from '@components/ui/SidePanel/SidePanel';
import Icon from '@components/common/Icon/Icon';

function RegisterClient() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  /**
   * On authentication state change, redirect authenticated users away from register.
   */
  useEffect(() => {
    if (isAuthenticated) navigate('/dashboard', { replace: true });
  }, [isAuthenticated, navigate]);

  /**
   * Fields declaration for this form
   */
  const initialFields = {
    name: '',
    surname: '',
    username: '',
    email: '',
    password: '',
    passwordConfirm: '',
  };

  /**
   * Custom Form field validation
   */
  const validate = ({ password, passwordConfirm }) => {
    if (!password || password.length < 8) return 'Password is too short';
    if (password !== passwordConfirm) return 'Passwords do not match';
    return undefined;
  };

  /**
   * Handles form submission for registering a new account to the api
   * If successfull redirect to login page, otherwise displays error messages on failure.
   */
  const handleRegister = async ({ name, surname, username, email, password }) => {
    setLoading(true);

    try {
      await api.auth.registerClient({ name, surname, username, email, password });
      navigate('/login?registered=1', { replace: true });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Hero>
      <Hero.Left>
        <SidePanel heading="Welcome to BarberManager" subheading="Manage your barbershop with ease">
          <SidePanel.Inner>
            <div className={styles.description}>
              <h2>Book your next haircut effortlessly</h2>
              <ul className={styles.features}>
                <li>
                  <Icon name="appointment" size="sm" />
                  <p>Book appointments online in seconds.</p>
                </li>
                <li>
                  <Icon name="availability" size="sm" />
                  <p>Keep and update your personal profile.</p>
                </li>
                <li>
                  <Icon name="calendar" size="sm" />
                  <p>Track your appointment history easily.</p>
                </li>
              </ul>
            </div>
          </SidePanel.Inner>

          <SidePanel.Actions>
            <p className={styles.note}>Already have an account?</p>

            <Button href="/login" color="secondary" size="md" width="content">
              Login!
            </Button>
          </SidePanel.Actions>
        </SidePanel>
      </Hero.Left>

      <Hero.Right background={'background'}>
        <Card className={styles.register}>
          <Form
            className={styles.registerForm}
            initialFields={initialFields}
            onSubmit={handleRegister}
            validate={validate} //
          >
            <h2 className={styles.label}>Sign up</h2>

            <div className={styles.inputGroup}>
              <Input label="Name" name="name" type="text" required size="md" />
              <Input label="Surname" name="surname" type="text" required size="md" />
            </div>

            <div className={styles.inputGroup}>
              <Input label="Username" name="username" type="text" required size="md" />
              <Input label="Email" name="email" type="email" required size="md" />
            </div>

            <div className={styles.inputGroup}>
              <Input label="Password" name="password" type="password" required size="md" />
              <Input label="Confirm password" name="passwordConfirm" type="password" required size="md" />
            </div>

            <Button className={styles.registerBtn} type="submit" size="md" disabled={loading} wide color="primary">
              <span className={styles.line}>
                {loading ? (
                  <>
                    <Spinner size={'sm'} /> Signing up...
                  </>
                ) : (
                  'Create Account'
                )}
              </span>
            </Button>

            <Error />
          </Form>
        </Card>
      </Hero.Right>
    </Hero>
  );
}

export default RegisterClient;
