import api from '@api';
import { ENDPOINTS } from '@api/endpoints';

/**
 * Retrieves the current barber's profile information.
 */
export async function getBarberProfile() {
  const { data } = await api.instance.get(ENDPOINTS.barber.profile);
  return data;
}

/**
 * Updates the barber profile with provided fields.
 */
export async function updateBarberProfile(patchData) {
  const { data } = await api.instance.patch(ENDPOINTS.barber.profile, patchData);
  return data;
}

/**
 * Deletes the barber's account from the system.
 */
export async function deleteBarberProfile() {
  await api.instance.delete(ENDPOINTS.barber.profile);
}

/**
 * Retrieves the list of services offered by the barber.
 */
export async function getBarberServices() {
  const { data } = await api.instance.get(ENDPOINTS.barber.services);
  return data;
}

/**
 * Creates a new service for the barber.
 */
export async function createBarberService(serviceData) {
  const { data } = await api.instance.post(ENDPOINTS.barber.services, serviceData);
  return data;
}

/**
 * Updates the details of an existing barber service.
 */
export async function updateBarberService(serviceId, patchData) {
  const { data } = await api.instance.patch(ENDPOINTS.barber.service(serviceId), patchData);
  return data;
}

/**
 * Deletes a specific service from the barber's offerings.
 */
export async function deleteBarberService(serviceId) {
  await api.instance.delete(ENDPOINTS.barber.service(serviceId));
}

/**
 * Retrieves all availability slots for the current barber.
 */
export async function getBarberAvailabilities() {
  const { data } = await api.instance.get(ENDPOINTS.barber.availabilities);
  return data;
}

/**
 * Lists all appointments for the current barber.
 */
export async function getBarberAppointments() {
  const { data } = await api.instance.get(ENDPOINTS.barber.appointments);
  return data;
}

/**
 * Retrieves all reviews written for the current barber.
 */
export async function getBarberReviews() {
  const { data } = await api.instance.get(ENDPOINTS.barber.reviews);
  return data;
}
