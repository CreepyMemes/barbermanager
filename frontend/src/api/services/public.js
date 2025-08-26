import api from '@api';
import { ENDPOINTS } from '@api/endpoints';

/**
 * Retrieves all public barbers.
 */
export async function getBarbersPublic() {
  const { data } = await api.instance.get(ENDPOINTS.public.barbers);
  return data;
}

/**
 * Retrieves the public profile of a specific client.
 */
export async function getClientProfilePublic(clientId) {
  const { data } = await api.instance.get(ENDPOINTS.public.clientProfile(clientId));
  return data;
}

/**
 * Retrieves the public profile of a specific barber.
 */
export async function getBarberProfilePublic(barberId) {
  const { data } = await api.instance.get(ENDPOINTS.public.barberProfile(barberId));
  return data;
}

/**
 * Retrieves the public availability schedule for a specific barber.
 */
export async function getBarberAvailabilitiesPublic(barberId) {
  const { data } = await api.instance.get(ENDPOINTS.public.barberAvailabilities(barberId));
  return data;
}

/**
 * Retrieves the public availability schedule for a specific barber.
 */
export async function getBarberSlotsPublic(barberId, date) {
  const { data } = await api.instance.post(ENDPOINTS.public.barberSlots(barberId), date);
  return data;
}

/**
 * Retrieves the services offered by a specific barber.
 */
export async function getBarberServicesPublic(barberId) {
  const { data } = await api.instance.get(ENDPOINTS.public.barberServices(barberId));
  return data;
}
