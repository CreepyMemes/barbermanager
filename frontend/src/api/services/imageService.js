import axiosInstance from '../axiosInstance';
import { ENDPOINTS } from '../endpoints';

/**
 * Uploads a new profile image to the server as multipart/form-data.
 */
export async function uploadProfileImage(formData) {
  const { data } = await axiosInstance.post(ENDPOINTS.image.profile, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
}

/**
 * Deletes the current user's profile image from the server.
 */
export async function deleteProfileImage() {
  await axiosInstance.delete(ENDPOINTS.image.profile);
}
