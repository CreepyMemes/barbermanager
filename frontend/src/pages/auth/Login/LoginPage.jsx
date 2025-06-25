import { useState, useEffect } from 'react';
import { useAuth } from '@hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import styles from './LoginPage.module.scss';

function isEmail(value) {
  // Simple email heuristic
  return /\S+@\S+\.\S+/.test(value);
}

export default function LoginPage() {
  const { login, loading, isAuthenticated } = useAuth();
  const [fields, setFields] = useState({ identifier: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // If already logged in, redirect to dashboard
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleChange = (e) => {
    setFields((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

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
            placeholder="Enter your username or email"
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
            placeholder="Enter your password"
          />
        </label>

        <button className={styles.button} type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>

        {error && <div className={styles.error}>{error}</div>}
      </form>
    </div>
  );
}
