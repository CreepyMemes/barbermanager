import { useState, useEffect, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import styles from './ConfirmPasswordReset.module.scss';
import api from '@api';

import Spinner from '@components/common/Spinner/Spinner';
import Card from '@components/common/Card/Card';
import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Button from '@components/common/Button/Button';
import Error from '@components/common/Error/Error';
import Hero from '@components/common/Hero/Hero';
import SidePanel from '@components/common/SidePanel/SidePanel';
import Icon from '@components/common/Icon/Icon';

function ConfirmPasswordReset() {
  const { uidb64, token } = useParams();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState(null);
  const [status, setStatus] = useState('pending');
  const [message, setMessage] = useState('');

  const [loading, setLoading] = useState(false);

  /**
   * Calls backend API to get email with provided uidb64 and token.
   * Updates component status and message based on response.
   */
  const getEmail = useCallback(async () => {
    setStatus('pending');

    try {
      const resp = await api.auth.getEmailFromToken(uidb64, token);
      setStatus('success');
      setEmail(resp?.email);
    } catch (error) {
      setStatus('error');
      setMessage(error?.response?.data?.detail || 'The password reset link is invalid or expired.');
    }
  }, [uidb64, token]);

  /**
   * Handles fetching the email on mount or when params change, to check the uid64 and token validity
   */
  useEffect(() => {
    if (!uidb64 || !token) {
      setStatus('error');
      setMessage('No uidb46 or token were provided.');
      return;
    }

    getEmail();
  }, [uidb64, token, getEmail]);

  /**
   * Fields declaration for this form
   */
  const initialFields = {
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
  const handleConfirmPasswordReset = async ({ password }) => {
    setLoading(true);

    try {
      await api.auth.confirmPasswordReset(uidb64, token, password);
      navigate('/login?registered=3', { replace: true }); // todo change
    } finally {
      setLoading(false);
    }
  };

  return (
    <Hero>
      {status === 'success' && (
        <Hero.Right className={styles.page} background={'background'}>
          <Card className={styles.register}>
            <Form
              className={styles.registerForm}
              initialFields={initialFields}
              onSubmit={handleConfirmPasswordReset}
              validate={validate}
            >
              <h2 className={styles.label}>Choose a new password</h2>

              <Input label="Password" name="password" type="password" required size="md" />
              <Input label="Confirm password" name="passwordConfirm" type="password" required size="md" />

              <Button className={styles.registerBtn} type="submit" size="md" disabled={loading} wide color="primary">
                <span className={styles.line}>
                  {loading ? (
                    <>
                      <Spinner size={'sm'} /> Saving password...
                    </>
                  ) : (
                    'Save password'
                  )}
                </span>
              </Button>

              <Error />
            </Form>
          </Card>
        </Hero.Right>
      )}

      {status === 'pending' && (
        <Hero.Right className={styles.page} background={'background'}>
          <Card className={styles.error}>
            <div className={styles.center}>
              <Spinner size="lg" />
              <h2>Retreiving your email...</h2>
            </div>
          </Card>
        </Hero.Right>
      )}

      {status === 'error' && (
        <Hero.Right className={styles.page} background={'background'}>
          <Card className={styles.error}>
            <div className={styles.center}>
              <Icon name="cancelled" size="md" black />
              <h2>Invitation Error</h2>
              <div className={styles.message}>{message}</div>

              <Button href="/login" color="primary" size="md">
                Back to Login
              </Button>
            </div>
          </Card>
        </Hero.Right>
      )}
    </Hero>
  );
}

export default ConfirmPasswordReset;
