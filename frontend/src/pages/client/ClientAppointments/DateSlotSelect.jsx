import { useEffect, useState, useCallback } from 'react';
import { useForm } from '@hooks/useForm';
import api from '@api';

const DateSlotSelect = () => {
  const { fields, handleChange } = useForm();
  const [loading, setLoading] = useState(false);
  const [availabilities, setAvailabilities] = useState([]);

  /**
   * Fetches the barber's availabilities from the API
   */
  const fetchAvailabilities = useCallback(async (barberId) => {
    setLoading(true);

    try {
      const data = await api.pub.getBarberAvailabilitiesPublic(barberId);
      setAvailabilities(data.availabilities || []);
    } catch {
      setAvailabilities([]);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * useEffect to fetch availabilities on mount
   */
  useEffect(() => {
    if (!fields.barber_id) {
      setAvailabilities([]);
      return;
    }

    fetchAvailabilities(fields.barber_id);
  }, [fields.barber_id, fetchAvailabilities]);

  // If no barber is selected
  if (!fields.barber_id) return <div>Please select a barber first.</div>;

  // Find selected availability
  const selectedAvailability = availabilities.find((a) => a.date === fields.date);

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
        {selectedAvailability?.slots?.map((slot) => (
          <option key={slot} value={slot}>
            {slot}
          </option>
        ))}
      </select>
    </>
  );
};

export default DateSlotSelect;
