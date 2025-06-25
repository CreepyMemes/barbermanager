import { useAuth } from '@hooks/useAuth';

// TODO: This is just a proof of concept that authenticated data is retreived
export default function DashboardPage() {
  const { user, profile } = useAuth();
  return (
    <div style={{ padding: 32 }}>
      <h1>Dashboard</h1>
      {user && (
        <div>
          <p>
            Welcome, <strong>{user?.username || user?.email}</strong>!
          </p>
          <p>
            Role: <strong>{user.role}</strong>
          </p>
        </div>
      )}
      {profile && (
        <div style={{ marginTop: 24 }}>
          <h2>Your Profile</h2>
          <pre>{JSON.stringify(profile, null, 2)}</pre>
        </div>
      )}
      {!profile && (
        <div style={{ marginTop: 24 }}>
          <em>Profile loading or unavailable.</em>
        </div>
      )}
      {/* Add dashboard widgets or quick links here */}
    </div>
  );
}
