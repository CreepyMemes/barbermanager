import { useForm } from '@hooks/useForm';
import { useEffect, useCallback, useState } from 'react';
import api from '@api';

function ConfirmationStep() {
  const { fields } = useForm();

  const [barbers, setBarbers] = useState([]);
  const [services, setServices] = useState([]);

  /**
   * Function that fetches all barbers from API
   */
  const fetchBarbers = useCallback(async () => {
    try {
      const result = await api.pub.getBarbersPublic();
      setBarbers(result.barbers || []);
    } catch {
      setBarbers([]);
    }
  }, []);

  /**
   * Fetches all barbers on mount
   */
  useEffect(() => {
    fetchBarbers();
  }, [fetchBarbers]);

  /**
   * Function that fetches all services for the selected barber from API
   */
  const fetchBarberServices = useCallback(async () => {
    if (fields.barber_id) {
      try {
        const result = await api.pub.getBarberServicesPublic(fields.barber_id);
        setServices(result.services || []);
      } catch {
        setServices([]);
      }
    } else {
      setServices([]);
    }
  }, [fields.barber_id]);

  /**
   * Fetches all selected barber's offered services on mount
   */
  useEffect(() => {
    fetchBarberServices();
  }, [fetchBarberServices]);

  // Find selected barber and service
  const barber = barbers.find((b) => String(b.id) === String(fields.barber_id));
  const selectedServices = services.filter((srv) => fields.services?.includes(String(srv.id)));

  return (
    <div>
      <div>
        <b>Barber:</b> {barber ? `${barber.name} ${barber.surname}` : fields.barber_id}
      </div>
      <div>
        <b>Services:</b> {selectedServices.length ? selectedServices.map((s) => s.name).join(', ') : fields.services?.join(', ')}
      </div>
      <div>
        <b>Date:</b> {fields.date}
      </div>
      <div>
        <b>Time Slot:</b> {fields.slot}
      </div>
    </div>
  );
}

export default ConfirmationStep;
