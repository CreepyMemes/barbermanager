import { useEffect, useState, useCallback } from 'react';
import { useForm } from '@hooks/useForm';
import api from '@api';

/**
 * Checkbox multi-select for services.
 * Selected ids are stored in `fields.services` (array of string or number).
 */
const ServiceSelect = () => {
  const { fields, handleChange } = useForm();
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(false);
  const barberId = fields.barber_id;

  // Helper: coerce to array (handle blank or undefined)
  const selected = Array.isArray(fields.services) ? fields.services : fields.services ? [fields.services] : [];

  // Fetch all offered services for the current barber
  const fetchServices = useCallback(async (barberId, signal) => {
    setLoading(true);
    try {
      const data = await api.pub.getBarberServicesPublic(barberId, { signal });
      setServices(data.services || []);
    } catch (error) {
      if (error.name !== 'AbortError') {
        setServices([]);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!barberId) {
      setServices([]);
      return;
    }
    const controller = new AbortController();
    fetchServices(barberId, controller.signal);
    return () => controller.abort();
  }, [barberId, fetchServices]);

  if (!barberId) return <div>Please select a barber first.</div>;

  // Custom handler for checkboxes to manage multiple selection
  const handleCheckbox = (e) => {
    const id = e.target.value;
    let newSelected;
    if (e.target.checked) {
      // add id if not present
      newSelected = [...selected, id];
    } else {
      // remove id
      newSelected = selected.filter((sid) => String(sid) !== String(id));
    }
    // synthesize an event matching the change handler's expectations
    handleChange({
      target: {
        name: 'services',
        value: newSelected,
      },
    });
  };

  /**
   *  Renders a multi selection checkbox for barber's offered services
   */
  return (
    <fieldset style={{ border: 0, padding: 0, margin: 0 }}>
      <legend>Select one or more services:</legend>
      {loading && <div>Loading services...</div>}
      {services.map(({ id, name, price }) => (
        <label key={id} style={{ display: 'block', marginBottom: 4 }}>
          <input
            type="checkbox"
            value={String(id)}
            checked={selected.includes(String(id))}
            onChange={handleCheckbox}
            disabled={loading}
          />{' '}
          {name} (${price})
        </label>
      ))}
      {services.length === 0 && !loading && <div>No services for this barber.</div>}
    </fieldset>
  );
};

export default ServiceSelect;
