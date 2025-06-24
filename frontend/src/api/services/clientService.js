import axiosInstance from '../axiosInstance';
import { ENDPOINTS } from '../endpoints';

/**
 * Retrieves the current client's profile information.
 */
export async function getClientProfile() {
  const { data } = await axiosInstance.get(ENDPOINTS.client.profile);
  return data;
}

/**
 * Updates the client's profile with the provided partial data.
 */
export async function updateClientProfile(patchData) {
  const { data } = await axiosInstance.patch(ENDPOINTS.client.profile, patchData);
  return data;
}

/**
 * Deletes the currently authenticated client's account.
 */
export async function deleteClientProfile() {
  await axiosInstance.delete(ENDPOINTS.client.profile);
}

/**
 * Retrieves the list of appointments for the current client.
 */
export async function getClientAppointments() {
  const { data } = await axiosInstance.get(ENDPOINTS.client.appointments);
  return data;
}

/**
 * Creates a new appointment with the specified barber.
 */
export async function createClientAppointment(barberId, appointmentData) {
  const { data } = await axiosInstance.post(ENDPOINTS.client.createAppointment(barberId), appointmentData);
  return data;
}

/**
 * Cancels a specific appointment for the client.
 */
export async function cancelClientAppointment(appointmentId) {
  const { data } = await axiosInstance.delete(ENDPOINTS.client.appointment(appointmentId));
  return data;
}

/**
 * Retrieves the reviews submitted by the current client.
 */
export async function getClientReviews() {
  const { data } = await axiosInstance.get(ENDPOINTS.client.reviews);
  return data;
}

/**
 * Creates a new review for a completed appointment.
 */
export async function createClientReview(appointmentId, reviewData) {
  const { data } = await axiosInstance.post(ENDPOINTS.client.createReview(appointmentId), reviewData);
  return data;
}

/**
 * Updates an existing review left by the client.
 */
export async function updateClientReview(reviewId, patchData) {
  const { data } = await axiosInstance.patch(ENDPOINTS.client.review(reviewId), patchData);
  return data;
}

/**
 * Deletes a client's review.
 */
export async function deleteClientReview(reviewId) {
  await axiosInstance.delete(ENDPOINTS.client.review(reviewId));
}
