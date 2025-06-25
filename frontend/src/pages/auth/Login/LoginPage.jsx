import { useState } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './LoginPage.module.scss';

// TODO: redo all of this, this is just AI slop for testing
export default function LoginPage() {
  const { login, loading } = useAuth();
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await login(form);
      // If login succeeds, auth context will update.
      // Optionally redirect (use `useNavigate` if you want).
    } catch (_) {
      // You may want better error handling depending on login() implementation.
      setError('Login failed. Please check your credentials.');
    }
  };

  return (
    <div className={styles.loginContainer}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <h2>Login</h2>
        <label>
          Username:
          <input
            name="username"
            value={form.username}
            onChange={handleChange}
            required
            autoComplete="username"
            disabled={loading}
          />
        </label>
        <label>
          Password:
          <input
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            required
            autoComplete="current-password"
            disabled={loading}
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
