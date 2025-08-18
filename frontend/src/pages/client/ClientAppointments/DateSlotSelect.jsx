import { useEffect, useState, useCallback } from 'react';
import { useForm } from '@hooks/useForm';
import api from '@api';

const DateSlotSelect = () => {
  const { fields, handleChange } = useForm();
  const [loading, setLoading] = useState(false);
  const [availabilities, setAvailabilities] = useState([]);

  const barberId = fields.barber_id;

  /**
   * Asynchronously fetches the barber's availabilities from the API, wrapped in useCallback for memoization
   */
  const fetchAvailabilities = useCallback(async (barberId, signal) => {
    setLoading(true);

    try {
      const data = await api.pub.getBarberAvailabilitiesPublic(barberId, { signal });
      setAvailabilities(data.availabilities || []);
    } catch (error) {
      if (error.name !== 'AbortError') {
        setAvailabilities([]);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * useEffect to fetch availabilities on mount
   */
  useEffect(() => {
    if (!barberId) {
      setAvailabilities([]);
      return;
    }
    const controller = new AbortController();
    fetchAvailabilities(barberId, controller.signal);
    return () => controller.abort();
  }, [barberId, fetchAvailabilities]);

  // If no barber is selected
  if (!barberId) return <div>Please select a barber first.</div>;

  const currentAvailability = availabilities.find((a) => a.date === fields.date);

  /**
   *  Renders a select dropdown for barbers's availability slot
   */
  return (
    <>
      <label>Date</label>
      <select
        name="date"
        value={fields.date || ''}
        onChange={handleChange}
        disabled={loading}
        required //
      >
        <option value="">Select date...</option>
        {availabilities.map(({ date }) => (
          <option key={date} value={date}>
            {date}
          </option>
        ))}
      </select>

      <label>Slot</label>
      <select
        name="slot"
        value={fields.slot || ''}
        onChange={handleChange}
        disabled={loading || !fields.date}
        required //
      >
        <option value="">Select timeslot...</option>
        {currentAvailability?.slots?.map((slot) => (
          <option key={slot} value={slot}>
            {slot}
          </option>
        ))}
      </select>
    </>
  );
};

export default DateSlotSelect;
