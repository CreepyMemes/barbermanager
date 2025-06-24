import axiosInstance from '../axiosInstance';
import { ENDPOINTS } from '../endpoints';

/**
 * Retrieves a list of all public barbers.
 */
export async function getBarbersPublic() {
  const data = await axiosInstance.get(ENDPOINTS.public.barbers);
  return data;
}

/**
 * Retrieves the public profile of a specific client.
 */
export async function getClientProfilePublic(clientId) {
  const data = await axiosInstance.get(ENDPOINTS.public.clientProfile(clientId));
  return data;
}

/**
 * Retrieves the public profile of a specific barber.
 */
export async function getBarberProfilePublic(barberId) {
  const data = await axiosInstance.get(ENDPOINTS.public.barberProfile(barberId));
  return data;
}

/**
 * Retrieves the public availability schedule for a specific barber.
 */
export async function getBarberAvailabilitiesPublic(barberId) {
  const data = await axiosInstance.get(ENDPOINTS.public.barberAvailabilities(barberId));
  return data;
}

/**
 * Retrieves the services offered by a specific barber.
 */
export async function getBarberServicesPublic(barberId) {
  const data = await axiosInstance.get(ENDPOINTS.public.barberServices(barberId));
  return data;
}
