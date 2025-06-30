import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';

function RoleRedirect() {
  const { isAuthenticated, isFetchingProfile, user } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    // Don't do anything if user is not authenticattd or still fetching user data
    if (!isAuthenticated || isFetchingProfile || !user) return;

    // Remove leading "/" if present
    const path = location.pathname.replace(/^\//, '');

    // Redirects `/<page>` to `/<role>/<page>`
    if (user.role && path) {
      navigate(`/${user.role.toLowerCase()}/${path}`, { replace: true });
    } else {
      navigate('/', { replace: true });
    }
  }, [isAuthenticated, isFetchingProfile, user, location, navigate]);

  return null;
}

export default RoleRedirect;
