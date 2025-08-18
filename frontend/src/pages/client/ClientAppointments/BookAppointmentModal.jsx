import Modal from '@components/common/Modal/Modal';
import api from '@api';

import BarberSelect from './BarberSelect';
import ServiceSelect from './ServiceSelect';
import DateSlotSelect from './DateSlotSelect';
import ConfirmationStep from './ConfirmationStep';

function BookAppointmentModal({ open, onClose, onBooked }) {
  /**
   * Final submit handler (called from last step)
   */
  const handleSubmit = async (fields) => {
    await api.client.createClientAppointment(fields.barber_id, {
      services: fields.services,
      date: fields.date,
      slot: fields.slot,
    });
    onBooked?.(); // refresh parent
    onClose();
  };

  return (
    <Modal
      open={open}
      onClose={onClose}
      fields={{
        barber_id: '',
        services: [],
        date: '',
        slot: '',
      }}
      action={{ submit: 'Book', loading: 'Booking...' }}
      onSubmit={handleSubmit}
    >
      {/* STEP 1: Select Barber */}
      <Modal.Step validate={(fields) => (!fields.barber_id ? 'You must select a barber.' : undefined)}>
        <Modal.Title icon="barber">Choose Barber</Modal.Title>
        <Modal.Description>Please choose the barber you want to book.</Modal.Description>
        <BarberSelect />
      </Modal.Step>

      {/* STEP 2: Select Services */}
      <Modal.Step
        validate={(fields) =>
          !fields.services || fields.services.length === 0 ? 'You must select at least one service.' : undefined
        }
      >
        <Modal.Title icon="service">Choose Services</Modal.Title>
        <Modal.Description>Select one or more services offered by your selected barber.</Modal.Description>
        <ServiceSelect />
      </Modal.Step>

      {/* STEP 3: Select Date & Time slot */}
      <Modal.Step validate={(fields) => (!fields.date || !fields.slot ? 'Please select date and time slot.' : undefined)}>
        <Modal.Title icon="calendar">Choose Date & Time</Modal.Title>
        <Modal.Description>Select an available date and time slot. Only available slots are shown.</Modal.Description>
        <DateSlotSelect />
      </Modal.Step>

      {/* STEP 4: Confirmation */}
      <Modal.Step>
        <Modal.Title icon="check">Confirm</Modal.Title>
        <Modal.Description>
          <ConfirmationStep />
        </Modal.Description>
      </Modal.Step>
    </Modal>
  );
}

export default BookAppointmentModal;
