import axiosInstance from '@api/axiosInstance';
import { ENDPOINTS } from '@api/endpoints';

/**
 * Uploads a new profile image to the server as multipart/form-data.
 */
export async function uploadProfileImage(formData) {
  const { data } = await axiosInstance.post(ENDPOINTS.image.profile, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }, // TODO: This is wrong, look at backend test how it's sent
  });
  return data;
}

/**
 * Deletes the current user's profile image from the server.
 */
export async function deleteProfileImage() {
  await axiosInstance.delete(ENDPOINTS.image.profile);
}
