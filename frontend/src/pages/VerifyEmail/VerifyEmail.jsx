import { useEffect, useState, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import styles from './VerifyEmail.module.scss';

import api from '@api';
import Spinner from '@components/common/Spinner/Spinner';
import Card from '@components/common/Card/Card';
import Icon from '@components/common/Icon/Icon';
import Button from '@components/common/Button/Button';
import Hero from '@components/common/Hero/Hero';

function VerifyEmail() {
  const { uidb64, token } = useParams();
  const [status, setStatus] = useState('pending');
  const [message, setMessage] = useState('');

  /**
   * Calls backend API to verify email with provided uidb64 and token.
   * Updates component status and message based on response.
   */
  const verify = useCallback(async () => {
    setStatus('pending');

    try {
      await api.auth.verifyEmail(uidb64, token);
      setStatus('success');
      setMessage('Email verified successfully! You can now log in.');
    } catch (error) {
      setStatus('error');
      setMessage(error?.response?.data?.detail || 'The verification link is invalid or expired.');
    }
  }, [uidb64, token]);

  /**
   * Handles verification on mount or when params change.
   */
  useEffect(() => {
    if (!uidb64 || !token) {
      setStatus('error');
      setMessage('Invalid verification link.');
      return;
    }

    verify();
  }, [uidb64, token, verify]);

  return (
    <Hero>
      <Hero.Right className={styles.page} background="background">
        <Card className={styles.verify}>
          {/* If email confirmation is still pending*/}
          {status === 'pending' && (
            <div className={styles.center}>
              <Spinner size="lg" />
              <h2>Verifying your email...</h2>
            </div>
          )}

          {/* If email confirmation is successfull */}
          {status === 'success' && (
            <div className={styles.center}>
              <Icon name="completed" size="md" black />
              <h2>Email Verified!</h2>
              <div className={styles.message}>{message}</div>

              <Button href="/login" color="primary" size="md">
                Back to Login
              </Button>
            </div>
          )}

          {/* If email confirmation failed */}
          {status === 'error' && (
            <div className={styles.center}>
              <Icon name="cancelled" size="md" black />
              <h2>Verification Failed</h2>
              <div className={styles.message}>{message}</div>

              <Button href="/login" color="primary" size="md">
                Back to Login
              </Button>
            </div>
          )}
        </Card>
      </Hero.Right>
    </Hero>
  );
}

export default VerifyEmail;
