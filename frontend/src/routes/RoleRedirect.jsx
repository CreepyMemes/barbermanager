import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';

function RoleRedirect() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (loading || !user) return;

    // Remove leading "/" if present
    const path = location.pathname.replace(/^\//, '');

    // Redirects `/<page>` to `/<role>/<page>`
    if (user.role && path) {
      navigate(`/${user.role.toLowerCase()}/${path}`, { replace: true });
    } else {
      navigate('/', { replace: true });
    }
  }, [user, loading, navigate, location]);

  return null;
}

export default RoleRedirect;
