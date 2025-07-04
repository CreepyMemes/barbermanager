import { useState } from 'react';
import styles from './RequestPasswordReset.module.scss';

import api from '@api';
import Spinner from '@components/common/Spinner/Spinner';
import Card from '@components/common/Card/Card';
import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Icon from '@components/common/Icon/Icon';
import Button from '@components/common/Button/Button';
import Error from '@components/common/Error/Error';
import Hero from '@components/common/Hero/Hero';

function RequestPasswordReset() {
  const [status, setStatus] = useState(null);
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
    setStatus('pending');

    try {
      await api.auth.requestPasswordReset(email);
    } finally {
      setStatus('success');
    }
  };

  return (
    <Hero>
      <Hero.Right className={styles.page} background="background">
        {status !== 'success' && (
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
                disabled={status === 'pending'}
                size="md"
              />

              <Button
                className={styles.loginBtn}
                type="submit"
                size="md"
                disabled={status === 'pending'}
                wide
                color="primary"
              >
                <span className={styles.line}>
                  {status === 'pending' ? (
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

        {status === 'success' && (
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
