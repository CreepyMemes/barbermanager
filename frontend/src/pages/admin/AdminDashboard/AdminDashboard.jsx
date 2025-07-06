import { useAuth } from '@hooks/useAuth';
// import styles from './AdminDashboard.module.scss';

import StatCard from '@components/common/StatCard/StatCard';
import RadialChart from '@components/common/RadialChart/RadialChart';

function AdminDashboard() {
  const { profile } = useAuth();

  return (
    <>
      {/* Revenue */}
      <StatCard icon="revenue" label="Total Revenue" value={`$${profile.total_revenue}`} />

      {/* Total Barbers */}
      <StatCard icon="barber" label="Total Barbers" value={profile.total_barbers} />

      {/* Total Appointments */}
      <StatCard icon="appointment" label="Total Appointments" value={profile.total_appointments} />

      {/* Completed Appointments */}
      <StatCard icon="completed" label="Completed Appointments" value={profile.completed_appointments} />

      {/* Ongoing Appointments */}
      <StatCard icon="calendar" label="Ongoing Appointments" value={profile.ongoing_appointments} />

      {/* Cancelled Appointments */}
      <StatCard icon="cancelled" label="Cancelled Appointments" value={profile.cancelled_appointments} />

      {/* Total Clients */}
      <StatCard icon="client" label="Total Clients" value={profile.total_clients} />

      {/* Total Reviews */}
      <StatCard icon="review" label="Total Reviews" value={profile.total_reviews} />

      {/* Average Rating */}
      <StatCard icon="rating" label="Average Rating">
        <RadialChart value={profile.average_rating} max={5} size="70" />
      </StatCard>
    </>
  );
}

export default AdminDashboard;
