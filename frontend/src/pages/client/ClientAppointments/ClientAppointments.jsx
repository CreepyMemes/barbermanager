import { useEffect, useState, useCallback } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import { useForm } from '@hooks/useForm';
import styles from './ClientAppointments.module.scss';
import api from '@api';

import Pagination from '@components/common/Pagination/Pagination';
import Input from '@components/common/Input/Input';
import Modal from '@components/common/Modal/Modal';
import Icon from '@components/common/Icon/Icon';
import Tag from '@components/common/Tag/Tag';
import Button from '@components/common/Button/Button';
import Spinner from '@components/common/Spinner/Spinner';
import Profile from '@components/ui/Profile/Profile';

function ClientAppointments() {
  const { profile } = useAuth();

  const location = useLocation();
  const navigate = useNavigate();

  // Parse barber id from query:
  const queryParams = new URLSearchParams(location.search);
  const preselectBarberId = queryParams.get('bookBarber');

  const [appointments, setAppointments] = useState([]);

  const [isLoadingAppointments, setIsLoadingAppointments] = useState(true);
  const [isLoadingBarberProfiles, setIsLoadingBarberProfiles] = useState(true);

  const [barbers, setBarbers] = useState({}); // barberId -> profile

  // Popup states
  const [bookPopup, setBookPopup] = useState(Boolean(preselectBarberId)); // Local state for controlling the modal and preselection
  const [cancelPopup, setCancelPopup] = useState({ open: false, appointment: null });

  // Preselected barber initial fields state from parameters
  const [bookFields, setBookFields] = useState({ barber_id: preselectBarberId || '', services: [], date: '', slot: '' });

  /**
   * Defines fetching all appointmentts from api (single responsibility, outside effect)
   */
  const fetchAppointments = useCallback(async () => {
    setIsLoadingAppointments(true);

    try {
      const result = await api.client.getClientAppointments();
      setAppointments(result.appointments || []);
    } finally {
      setIsLoadingAppointments(false);
    }
  }, []);

  /**
   * Defines fetching all barber profiles needed (only unique barber IDs)
   */
  const fetchBarberProfiles = useCallback(async (appointments) => {
    setIsLoadingBarberProfiles(true);

    try {
      // Gets all unique barber IDs from appointments
      const barberIds = [...new Set(appointments.map((a) => a.barber_id))];

      // fetches all barber profiles in parallel
      const entries = await Promise.all(
        barberIds.map(async (id) => {
          try {
            const { profile } = await api.pub.getBarberProfilePublic(id);
            return [id, profile];
          } catch {
            return [id, null];
          }
        }),
      );

      setBarbers((prev) => ({ ...prev, ...Object.fromEntries(entries) })); // assembles into { [id]: profile }
    } finally {
      setIsLoadingBarberProfiles(false);
    }
  }, []);

  /**
   * Only fetch if profile is loaded AND user is client
   */
  useEffect(() => {
    if (profile?.role === 'CLIENT') {
      fetchAppointments();
    }
  }, [profile, fetchAppointments]);

  /**
   * When appointments change, fetch needed barber profiles
   */
  useEffect(() => {
    if (appointments.length > 0) {
      fetchBarberProfiles(appointments);
    }
  }, [appointments, fetchBarberProfiles]);

  /**
   *  If query param is present and modal isn't open, open it and preselect barber
   */
  useEffect(() => {
    if (!preselectBarberId) return;

    // Open and preselect the barber (ok even if already open)
    openBookPopup();
    setBookFields((fields) => ({ ...fields, barber_id: preselectBarberId }));

    // Remove the param immediately so closing won't reopen the modal
    const params = new URLSearchParams(location.search);
    params.delete('bookBarber');
    navigate({ search: params.toString() }, { replace: true });
  }, [preselectBarberId, location.search, navigate]);

  // Book appointment popup state handlers
  const openBookPopup = () => setBookPopup(true);
  const closeBookPopup = () => {
    setBookPopup(false);
    setBookFields({ barber_id: '', services: [], date: '', slot: '' });
  };

  // Cancel apointment popup state handlers
  const openCancelPopup = (appointment) => setCancelPopup({ open: true, appointment });
  const closeCancelPopup = () => setCancelPopup({ open: false, appointment: null });

  /**
   * Handles booking appointmentss
   */
  const handleBookAppointment = async ({ barber_id, services, date, slot }) => {
    await api.client.createClientAppointment(barber_id, { services, date, slot });
    closeBookPopup();
    await fetchAppointments();
  };

  /**
   * Handles canceling the selected appointment
   */
  const handleCancelAppointment = async (appointmentId) => {
    await api.client.cancelClientAppointment(appointmentId);
    closeCancelPopup();
    await fetchAppointments();
  };

  /**
   * Function that fetches and returns all barbers from the API (useCallback to fix endless loop)
   */
  const fetchBarbers = useCallback(async () => {
    const { barbers } = await api.pub.getBarbersPublic();
    return barbers;
  }, []);

  /**
   * Function that fetches and returns all services of the selected barber from the API (useCallback to fix endless loop)
   */
  const fetchServices = useCallback(async (barberId) => {
    if (!barberId) return [];

    const { services } = await api.pub.getBarberServicesPublic(barberId);
    return services;
  }, []);

  /**
   * Services selection component to render the checkbox input of services to be selected
   */
  const ServiceSelect = () => {
    const { fields } = useForm();

    // If no barber is selected render error
    if (!fields.barber_id) return <div>Please select a barber first.</div>;

    return (
      <Input
        type="checkbox"
        name="services"
        label="Select one or more services"
        fetcher={() => fetchServices(fields.barber_id)}
        mapOption={(service) => ({ key: String(service.id), value: `${service.name} $${service.price}` })}
        required //
      />
    );
  };

  /**
   * Date and slot selection component to render the dropdown input of dates and slots to be selected
   */
  const DateSlotSelect = () => {
    const { fields } = useForm();

    /**
     * Function that fetches all availabilities dates of the selected barber from the API (useCallback to fix endless loop)
     */
    const fetchAvailabilities = useCallback(async (barberId) => {
      if (!barberId) return [];

      const { availabilities } = await api.pub.getBarberAvailabilitiesPublic(barberId);
      return availabilities;
    }, []);

    /**
     * Function that fetches all slots of the selected availability date from the API (useCallback to fix endless loop)
     */
    const fetchSlots = useCallback(async (barberId, date) => {
      if (!barberId || !date) return [];
      const { slots } = await api.pub.getBarberSlotsPublic(barberId, { date });

      return slots;
    }, []);

    // If no barber is selected render error
    if (!fields.barber_id) return <div>Please select a barber first.</div>;

    return (
      <>
        <Input
          type="dropdown"
          size="md"
          name="date"
          label="Date"
          fetcher={() => fetchAvailabilities(fields.barber_id)}
          mapOption={(availability) => ({ key: availability.date, value: availability.date })}
          required //
        />

        <Input
          type="dropdown"
          size="md"
          name="slot"
          label="Slot"
          fetcher={() => fetchSlots(fields.barber_id, fields.date)}
          reloadKey={`${fields.barber_id}-${fields.date}`}
          mapOption={(slot) => ({ key: slot, value: slot })}
          disabled={!fields.date}
          required //
        />
      </>
    );
  };

  /**
   * Confirmation step component to display current selection prior to submission
   */
  function ConfirmationStep() {
    const { fields } = useForm();

    const [barbers, setBarbers] = useState([]);
    const [services, setServices] = useState([]);
    const [loadingBarbers, setLoadingBarbers] = useState(false);
    const [loadingServices, setLoadingServices] = useState(false);

    /**
     * Function that fetches all barbers from API
     */
    const loadBarbers = useCallback(async () => {
      setLoadingBarbers(true);

      try {
        const result = await fetchBarbers();
        setBarbers(result || []);
      } finally {
        setLoadingBarbers(false);
      }
    }, []);

    /**
     * Function that fetches all services for the selected barber from API
     */
    const loadServices = useCallback(async (barberId) => {
      setLoadingServices(true);

      try {
        const result = await fetchServices(barberId);
        setServices(result || []);
      } finally {
        setLoadingServices(false);
      }
    }, []);

    /**
     * Fetches all barbers on mount
     */
    useEffect(() => {
      loadBarbers();
    }, [loadBarbers]);

    /**
     * Fetches all selected barber's offered services on mount
     */
    useEffect(() => {
      loadServices(fields.barber_id);
    }, [loadServices, fields.barber_id]);

    // Find selected barber and services
    const selectedBarber = barbers.find((barber) => String(barber.id) === String(fields.barber_id));
    const selectedServices = services.filter((service) => fields.services?.includes(String(service.id)));

    return (
      <div className={styles.confirmation}>
        <div className={styles.confirmRow}>
          <div className={styles.confirmBlock}>
            <Icon name="barber" size="ty" black />
            <span className={styles.confirmLabel}>Barber:</span>
          </div>
          <div className={styles.confirmContent}>
            <div className={styles.confirmValue}>
              {loadingBarbers ? (
                <Spinner size="sm" />
              ) : selectedBarber ? (
                `(${selectedBarber.username}) ${selectedBarber.name} ${selectedBarber.surname}`
              ) : fields.barber_id ? (
                fields.barber_id
              ) : (
                '-'
              )}
            </div>
          </div>
        </div>

        <div className={styles.confirmRow}>
          <div className={styles.confirmBlock}>
            <Icon name="service" size="ty" black />
            <span className={styles.confirmLabel}>Services:</span>
          </div>
          <div className={styles.confirmContent}>
            <div className={styles.confirmValue}>
              {loadingServices ? (
                <Spinner size="sm" />
              ) : selectedServices.length ? (
                selectedServices.map((s) => s.name).join(', ')
              ) : fields.services?.length ? (
                fields.services.join(', ')
              ) : (
                '-'
              )}
            </div>
          </div>
        </div>

        <div className={styles.confirmRow}>
          <div className={styles.confirmBlock}>
            <Icon name="calendar" size="ty" black />
            <span className={styles.confirmLabel}>Date:</span>
          </div>
          <div className={styles.confirmContent}>
            <div className={styles.confirmValue}>{fields.date || '-'}</div>
          </div>
        </div>

        <div className={styles.confirmRow}>
          <div className={styles.confirmBlock}>
            <Icon name="availability" size="ty" black />
            <span className={styles.confirmLabel}>Slot:</span>
          </div>
          <div className={styles.confirmContent}>
            <div className={styles.confirmValue}>{fields.slot || '-'}</div>
          </div>
        </div>
      </div>
    );
  }
  // Only render UI for clients otherwise render nothing
  if (!profile || profile.role !== 'CLIENT') return null;

  return (
    <>
      <Pagination
        className={styles.clientAppointments}
        icon="appointment"
        label="Appointments"
        itemsPerPage={7}
        loading={isLoadingAppointments}
        emptyMessage="No appointments found." //
      >
        <Pagination.Action>
          <div className={styles.action}>
            <Button
              className={styles.refreshBtn}
              type="button"
              color="primary"
              size="md"
              onClick={fetchAppointments}
              disabled={isLoadingAppointments} //
            >
              <span className={styles.line}>
                {isLoadingAppointments ? (
                  <>
                    <Spinner size="sm" /> Refreshing...
                  </>
                ) : (
                  <>
                    <Icon name="refresh" size="ty" /> Refresh appointments
                  </>
                )}
              </span>
            </Button>

            <Button
              className={styles.actionBtn}
              type="button"
              color="primary"
              size="md"
              onClick={openBookPopup} //
            >
              <Icon name="plus" size="ty" />
              <span>Book appointment</span>
            </Button>
          </div>
        </Pagination.Action>

        {/* Table headers */}
        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="barber" size="ty" black />
            <span className={styles.tableTitleName}>Barber</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="calendar" size="ty" black />
            <span className={styles.tableTitleName}>Date</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="revenue" size="ty" black />
            <span className={styles.tableTitleName}>Spent</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="service" size="ty" black />
            <span className={styles.tableTitleName}>Services</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="email_base" size="ty" black />
            <span className={styles.tableTitleName}>Reminder</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="spinner" size="ty" black />
            <span className={styles.tableTitleName}>Status</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="dial" size="ty" black />
            <span className={styles.tableTitleName}>Actions</span>
          </div>
        </Pagination.Column>

        {/* Table rows */}
        {appointments.map((appointment) => (
          <Pagination.Row key={appointment.id}>
            <Pagination.Cell>
              <Profile profile={barbers[appointment.barber_id]} loading={isLoadingBarberProfiles} />
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.dateContainer}>
                <div className={styles.date}>
                  <span className={styles.date}>{appointment.date.replaceAll('-', ' / ')}</span>
                  <span className={styles.slot}>( {appointment.slot} )</span>
                </div>
              </div>
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.amountSpent}>
                <span className={styles.amount}>${appointment.amount_spent}</span>
              </div>
            </Pagination.Cell>

            <Pagination.Cell>
              <span className={styles.services}>{appointment.services.map((service) => service.name).join(', ')}</span>
            </Pagination.Cell>

            <Pagination.Cell>
              <Tag className={styles.reminderTag} color={appointment.reminder_email_sent ? 'blue' : 'yellow'}>
                {appointment.reminder_email_sent ? 'Sent' : 'Not Sent'}
              </Tag>
            </Pagination.Cell>

            <Pagination.Cell>
              <Tag
                className={styles.statusTag}
                color={appointment.status === 'COMPLETED' ? 'green' : appointment.status === 'ONGOING' ? 'yellow' : 'red'}
              >
                {appointment.status.charAt(0) + appointment.status.slice(1).toLowerCase()}
              </Tag>
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.actions}>
                <Button
                  type="button"
                  size="sm"
                  color="animated"
                  disabled={appointment.status !== 'ONGOING'}
                  onClick={() => openCancelPopup(appointment)} //
                >
                  <Icon name="trash" size="ty" black />
                </Button>
              </div>
            </Pagination.Cell>
          </Pagination.Row>
        ))}
      </Pagination>

      {/* Book Appointment Modal */}
      <Modal
        open={bookPopup}
        fields={bookFields}
        initialStepIndex={bookFields.barber_id ? 1 : 0}
        action={{ submit: 'Book', loading: 'Booking...' }}
        onSubmit={handleBookAppointment}
        onClose={closeBookPopup}
      >
        {/* STEP 1: Select Barber */}
        <Modal.Step validate={(fields) => (!fields.barber_id ? 'You must select a barber.' : undefined)}>
          <Modal.Title icon="barber">Choose Barber</Modal.Title>
          <Modal.Description>Please choose the barber you want to book.</Modal.Description>

          <Input
            type="dropdown"
            size="md"
            name="barber_id"
            label="Barber"
            fetcher={fetchBarbers}
            mapOption={(barber) => ({ key: barber.id, value: `(${barber.username}) ${barber.name} ${barber.surname}` })}
            required //
          />
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

      {/* Cancel Appointment Modal */}
      <Modal
        open={cancelPopup.open}
        action={{ submit: 'Cancel', loading: 'Canceling...' }}
        onSubmit={() => handleCancelAppointment(cancelPopup.appointment?.id)}
        onClose={closeCancelPopup}
      >
        <Modal.Title icon="warning">Cancel Appointment</Modal.Title>
        <Modal.Description>
          Are you sure you want to cancel your appointment at <strong>{cancelPopup.appointment?.date}</strong>? This action cannot
          be undone.
        </Modal.Description>
      </Modal>
    </>
  );
}

export default ClientAppointments;
