import api from '@api';
import { ENDPOINTS } from '@api/endpoints';

/**
 * Retrieves the current admin's profile information.
 */
export async function getAdminProfile() {
  const { data } = await api.instance.get(ENDPOINTS.admin.profile);
  return data;
}

/**
 * Updates the admin profile with provided fields.
 */
export async function updateAdminProfile(patchData) {
  const { data } = await api.instance.patch(ENDPOINTS.admin.profile, patchData);
  return data;
}

/**
 * Deletes the admin's account from the system.
 */
export async function deleteAdminProfile() {
  await api.instance.delete(ENDPOINTS.admin.profile);
}

/**
 * Fetches the list of all barbers registered in the system.
 */
export async function getAllBarbers() {
  const { data } = await api.instance.get(ENDPOINTS.admin.barbers);
  return data;
}

/**
 * Retrieves all client accounts from the server.
 */
export async function getAllClients() {
  const { data } = await api.instance.get(ENDPOINTS.admin.clients);
  return data;
}

/**
 * Fetches the complete list of appointments managed by the admin.
 */
export async function getAllAppointments() {
  const { data } = await api.instance.get(ENDPOINTS.admin.appointments);
  return data;
}

/**
 * Sends an invitation to a barber via email.
 */
export async function inviteBarber(email) {
  const { data } = await api.instance.post(ENDPOINTS.admin.inviteBarber, email);
  return data;
}

/**
 * Deletes a barber account by its unique identifier.
 */
export async function deleteBarber(barberId) {
  await api.instance.delete(ENDPOINTS.admin.barber(barberId));
}

/**
 * Creates a new availability entry for a specific barber.
 */
export async function createBarberAvailability(barberId, availabilityData) {
  const { data } = await api.instance.post(ENDPOINTS.admin.barberAvailabilities(barberId), availabilityData);
  return data;
}

/**
 * Updates an existing availability slot for a barber.
 */
export async function updateBarberAvailability(barberId, availabilityId, patchData) {
  const { data } = await api.instance.patch(ENDPOINTS.admin.barberAvailability(barberId, availabilityId), patchData);
  return data;
}

/**
 * Deletes a specific availability slot for a barber.
 */
export async function deleteBarberAvailability(barberId, availabilityId) {
  await api.instance.delete(ENDPOINTS.admin.barberAvailability(barberId, availabilityId));
}
