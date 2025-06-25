import { useState, useEffect } from 'react';
import { useAuth } from '@hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import { isEmail } from '@utils/utils';
import styles from './LoginPage.module.scss';
import Button from '@components/common/Button/Button';

export default function LoginPage() {
  const { login, loading, isAuthenticated } = useAuth();
  const [fields, setFields] = useState({ identifier: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  /**
   * On authentication state change, redirect authenticated users away from login.
   */
  useEffect(() => {
    if (isAuthenticated) navigate('/dashboard', { replace: true });
  }, [isAuthenticated, navigate]);

  /**
   * Handles changes in the input fields by updating local state.
   */
  const handleChange = (e) => {
    setFields((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  /**
   * Handles form submission for login, Determines whether the identifier is an email or username,
   * then attempts to log in with credentials. Displays error messages on failure.
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const { identifier, password } = fields;
    const payload = isEmail(identifier) ? { email: identifier, password } : { username: identifier, password };

    try {
      await login(payload); // The AuthProvider will redirect due to isAuthenticated update.
    } catch (error) {
      setError(error?.response?.data?.detail || error?.message || 'Login failed'); // Extract and show backend error, or fallback to a sensible message
    }
  };

  return (
    <div className={styles.loginContainer}>
      <form className={styles.form} onSubmit={handleSubmit} autoComplete="on">
        <h2>Login</h2>

        <label>
          Username or Email:
          <input
            name="identifier"
            type="text"
            value={fields.identifier}
            onChange={handleChange}
            autoComplete="username"
            required
            disabled={loading}
          />
        </label>

        <label>
          Password:
          <input
            name="password"
            type="password"
            value={fields.password}
            onChange={handleChange}
            autoComplete="current-password"
            required
            disabled={loading}
          />
        </label>

        <Button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </Button>

        {error && <div className={styles.error}>{error}</div>}
      </form>
    </div>
  );
}
