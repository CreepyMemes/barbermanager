import api from '@api';
import { ENDPOINTS } from '@api/endpoints';

/**
 * Upload a profile image file, (File object from an <input type="file"> element)
 */
export async function uploadProfileImage(file) {
  const formData = new FormData();
  formData.append('profile_image', file);

  const { data } = await api.instance.post(ENDPOINTS.image.profile, formData);
  return data;
}

/**
 * Deletes the current user's profile image from the server.
 */
export async function deleteProfileImage() {
  await api.instance.delete(ENDPOINTS.image.profile);
}
