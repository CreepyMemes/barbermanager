import axiosInstance from '../axiosInstance';
import { ENDPOINTS } from '../endpoints';

/**
 * Retrieves the admin's profile information from the server.
 */
export async function getAdminProfile() {
  const data = await axiosInstance.get(ENDPOINTS.admin.profile);
  return data;
}

/**
 * Retrieves all client accounts from the server.
 */
export async function getAllClients() {
  const data = await axiosInstance.get(ENDPOINTS.admin.clients);
  return data;
}

/**
 * Fetches the list of all barbers registered in the system.
 */
export async function getAllBarbers() {
  const data = await axiosInstance.get(ENDPOINTS.admin.barbers);
  return data;
}

/**
 * Sends an invitation to a barber via email.
 */
export async function inviteBarber(email) {
  const data = await axiosInstance.post(ENDPOINTS.admin.inviteBarber, { email });
  return data;
}

/**
 * Deletes a barber account by its unique identifier.
 */
export async function deleteBarber(barberId) {
  await axiosInstance.delete(ENDPOINTS.admin.barber(barberId));
}

/**
 * Creates a new availability entry for a specific barber.
 */
export async function createBarberAvailability(barberId, availabilityData) {
  const data = await axiosInstance.post(ENDPOINTS.admin.barberAvailabilities(barberId), availabilityData);
  return data;
}

/**
 * Updates an existing availability slot for a barber.
 */
export async function updateBarberAvailability(barberId, availabilityId, patchData) {
  const data = await axiosInstance.patch(ENDPOINTS.admin.barberAvailability(barberId, availabilityId), patchData);
  return data;
}

/**
 * Deletes a specific availability slot for a barber.
 */
export async function deleteBarberAvailability(barberId, availabilityId) {
  await axiosInstance.delete(ENDPOINTS.admin.barberAvailability(barberId, availabilityId));
}

/**
 * Fetches the complete list of appointments managed by the admin.
 */
export async function getAllAppointments() {
  const data = await axiosInstance.get(ENDPOINTS.admin.appointments);
  return data;
}
