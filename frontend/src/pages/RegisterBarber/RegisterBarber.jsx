import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import styles from './RegisterBarber.module.scss';
import api from '@api';

import { decodeUid64 } from '@utils/utils';
import Spinner from '@components/common/Spinner/Spinner';
import Card from '@components/common/Card/Card';
import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Button from '@components/common/Button/Button';
import Error from '@components/common/Error/Error';
import Hero from '@components/common/Hero/Hero';
import SidePanel from '@components/common/SidePanel/SidePanel';
import Icon from '@components/common/Icon/Icon';

function RegisterBarber() {
  const { uidb64, token } = useParams();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState(null);
  const [loading, setLoading] = useState(false);

  /**
   * On authentication state change, redirect authenticated users away from register.
   */
  useEffect(() => {
    if (isAuthenticated) navigate('/dashboard', { replace: true });
  }, [isAuthenticated, navigate]);

  /**
   * Fetch the email asynchronously, to check the uid64 and token validity
   */
  useEffect(() => {
    if (!uidb64 || !token) {
      setLoading(false);
      return;
    }

    setLoading(true);
    (async () => {
      try {
        const resp = await api.auth.getEmailFromToken(uidb64, token);
        setEmail(resp?.email);
      } catch {
        // Ignore
      } finally {
        setLoading(false);
      }
    })();
  }, [uidb64, token]);

  // Return spinner while loading the async getting email
  if (loading) return <Spinner />;

  /**
   *  Quick link guard, checks if there's uid and token in the url
   */
  if (!email) {
    return (
      <Hero>
        <Hero.Right className={styles.page} background={'background'}>
          <Card className={styles.error}>
            <div className={styles.center}>
              <Icon name="cancelled" size="md" black />
              <h2>Invalid invitation link.</h2>
              <div className={styles.message}>Please check your invitation email or contact your admin.</div>

              <Button href="/login" color="primary" size="md">
                Back to Login
              </Button>
            </div>
          </Card>
        </Hero.Right>
      </Hero>
    );
  }

  /**
   * Fields declaration for this form
   */
  const initialFields = {
    name: '',
    surname: '',
    username: '',
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
  const handleRegister = async ({ name, surname, username, password }) => {
    setLoading(true);

    try {
      await api.auth.registerBarber(uidb64, token, { name, surname, username, password });
      navigate('/login?registered=1', { replace: true });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Hero>
      <Hero.Left>
        <SidePanel heading="Barber Invitation" subheading="Complete your barber account setup">
          <SidePanel.Inner>
            <div className={styles.description}>
              <h2>Finish your registration as a barber</h2>
              <ul className={styles.features}>
                <li>
                  <Icon name="barber" size="sm" />
                  <p>Manage your profile, clients, and appointments.</p>
                </li>
                <li>
                  <Icon name="service" size="sm" />
                  <p>View your availability and set your offered services.</p>
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
            validate={validate}
          >
            <h2 className={styles.label}>Sign up</h2>

            <div className={styles.inputGroup}>
              <Input label="Name" name="name" type="text" required size="md" />
              <Input label="Surname" name="surname" type="text" required size="md" />
            </div>

            <div className={styles.inputGroup}>
              <Input label="Username" name="username" type="text" required size="md" />
              <Input label="Email" name="email" type="email" size="md" placeholder={email} disabled />
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

export default RegisterBarber;
