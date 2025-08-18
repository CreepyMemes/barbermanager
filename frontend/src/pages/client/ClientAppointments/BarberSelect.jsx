import { useEffect, useState, useCallback } from 'react';
import { useForm } from '@hooks/useForm';
import api from '@api';

const BarberSelect = () => {
  const { fields, handleChange } = useForm();

  const [barbers, setBarbers] = useState([]);
  const [loading, setLoading] = useState(true);

  /**
   * Asynchronously fetchess barbers from the API, wrapped in useCallback for memoization
   */
  const fetchBarbers = useCallback(async (signal) => {
    setLoading(true);

    try {
      const data = await api.pub.getBarbersPublic({ signal });
      setBarbers(data.barbers || []);
    } catch (error) {
      if (error.name !== 'AbortError') {
        setBarbers([]);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * useEffect to fetch barbers on mount
   */
  useEffect(() => {
    const controller = new AbortController();
    fetchBarbers(controller.signal);
    return () => controller.abort();
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
};

export default BarberSelect;
