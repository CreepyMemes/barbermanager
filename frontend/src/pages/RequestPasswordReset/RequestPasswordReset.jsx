import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import styles from './RequestPasswordReset.module.scss';

import api from '@api';
import Spinner from '@components/common/Spinner/Spinner';
import Card from '@components/common/Card/Card';
import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Icon from '@components/common/Icon/Icon';
import Button from '@components/common/Button/Button';
import Error from '@components/common/Error/Error';
import Hero from '@components/ui/Hero/Hero';

function RequestPasswordReset() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [status, setStatus] = useState('waiting');
  const [loading, setLoading] = useState(false);

  /**
   * On authentication state change, redirect authenticated users to their settings.
   */
  useEffect(() => {
    if (isAuthenticated) navigate('/settings', { replace: true });
  }, [isAuthenticated, navigate]);

  /**
   * Fields declaration for this form
   */
  const initialFields = {
    email: '',
  };

  /**
   * Handles form submission for login, Determines whether the identifier is an email or username,
   * then attempts to log in with credentials. Displays error messages on failure.
   */
  const handleRequestPasswordReset = async ({ email }) => {
    setLoading(true);

    try {
      await api.auth.requestPasswordReset(email);
    } finally {
      setLoading(false);
      setStatus('sent');
    }
  };

  return (
    <Hero>
      <Hero.Right className={styles.page} background="background">
        {status === 'waiting' && (
          <Card className={styles.login}>
            <Form className={styles.loginForm} initialFields={initialFields} onSubmit={handleRequestPasswordReset}>
              <h2 className={styles.label}>Reset your password</h2>

              <Input
                label="Email"
                name="email"
                type="email"
                autoComplete="email"
                placeholder="your@email.com"
                required
                disabled={loading}
                size="md"
              />

              <Button className={styles.loginBtn} type="submit" size="md" disabled={loading} wide color="primary">
                <span className={styles.line}>
                  {loading ? (
                    <>
                      <Spinner size={'sm'} /> Sending email...
                    </>
                  ) : (
                    'Send password reset email'
                  )}
                </span>
              </Button>

              <Error />
            </Form>
          </Card>
        )}

        {status === 'sent' && (
          <Card className={styles.success}>
            <div className={styles.center}>
              <Icon name="completed" size="md" black />
              <h2>Email sent!</h2>
              <div className={styles.message}>Check your email to reset your password</div>

              <Button href="/login" color="primary" size="md">
                Back to Login
              </Button>
            </div>
          </Card>
        )}
      </Hero.Right>
    </Hero>
  );
}

export default RequestPasswordReset;
