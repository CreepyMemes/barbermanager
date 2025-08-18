import { useEffect, useState, useCallback } from 'react';
import { useForm } from '@hooks/useForm';
import api from '@api';

/**
 * Checkbox multi-select for services.
 * Selected ids are stored in `fields.services` (array of string or number).
 */
function ServiceSelect() {
  const { fields, handleChange } = useForm();

  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(false);

  // Coerces to array, handles blank or undefined
  const selectedServices = Array.isArray(fields.services) ? fields.services : fields.services ? [fields.services] : [];

  /**
   * Fetches all offered services for the current barber from the API
   */
  const fetchServices = useCallback(async (barberId) => {
    setLoading(true);

    try {
      const { services } = await api.pub.getBarberServicesPublic(barberId);
      setServices(services);
    } catch {
      setServices([]);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * useEffect to fetch services on mount
   */
  useEffect(() => {
    if (!fields.barber_id) {
      setServices([]);
      return;
    }

    fetchServices(fields.barber_id);
  }, [fields.barber_id, fetchServices]);

  // If no barber is selected
  if (!fields.barber_id) return <div>Please select a barber first.</div>;

  /**
   * Custom handler for checkboxes to manage multiple selection
   */
  const handleCheckbox = (e) => {
    const id = e.target.value;
    let newSelected;

    if (e.target.checked) {
      newSelected = [...selectedServices, id]; // add id if not present
    } else {
      newSelected = selectedServices.filter((sid) => String(sid) !== String(id)); // remove id
    }

    // synthesizes an event matching the change handler's expectations
    handleChange({ target: { name: 'services', value: newSelected } });
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
            checked={selectedServices.includes(String(id))}
            onChange={handleCheckbox}
            disabled={loading}
          />{' '}
          {name} (${price})
        </label>
      ))}
      {services.length === 0 && !loading && <div>No services for this barber.</div>}
    </fieldset>
  );
}

export default ServiceSelect;
