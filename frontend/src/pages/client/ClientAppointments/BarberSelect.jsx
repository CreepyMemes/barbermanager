import { useEffect, useState, useCallback } from 'react';
import { useForm } from '@hooks/useForm';
import api from '@api';

/**
 * Dropdown selection list for barbers.
 * Selected id is stored in `fields.barber_id`
 */
function BarberSelect() {
  const { fields, handleChange } = useForm();

  const [barbers, setBarbers] = useState([]);
  const [loading, setLoading] = useState(true);

  /**
   * Fetches barbers from the API
   */
  const fetchBarbers = useCallback(async () => {
    setLoading(true);

    try {
      const result = await api.pub.getBarbersPublic();
      setBarbers(result.barbers || []);
    } catch {
      setBarbers([]);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * useEffect to fetch barbers on mount
   */
  useEffect(() => {
    fetchBarbers();
  }, [fetchBarbers]);

  /**
   *  Renders a select dropdown for barbers
   */
  return (
    <select
      name="barber_id"
      value={fields.barber_id || ''}
      onChange={handleChange}
      disabled={loading}
      required //
    >
      <option value="">Select barber...</option>

      {barbers.map(({ id, name, surname, username }) => (
        <option key={id} value={id}>
          ({username}) {name} {surname}
        </option>
      ))}
    </select>
  );
}

export default BarberSelect;
