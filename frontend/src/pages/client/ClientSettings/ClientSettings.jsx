import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './ClientSettings.module.scss';
import api from '@api';

import StatCard from '@components/ui/StatCard/StatCard';
import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Icon from '@components/common/Icon/Icon';
import Button from '@components/common/Button/Button';
import ProfileImage from '@components/ui/ProfileImage/ProfileImage';
import Spinner from '@components/common/Spinner/Spinner';
import Error from '@components/common/Error/Error';

import UploadPicturePopup from '@components/ui/UploadPicturePopup/UploadPicturePopup';
import DeletePicturePopup from '@components/ui/DeletePicturePopup/DeletePicturePopup';
import DeleteProfilePopup from '@components/ui/DeleteProfilePopup/DeleteProfilePopup';

function ClientSettings() {
  const { profile, setProfile, logout } = useAuth();
  const [isLoading, setIsLoading] = useState(true);

  const [isUpdatingProfile, setIsUpdatingProfile] = useState(false); // Used to disable the update profile button

  // Popup states
  const [uploadPicurePopup, setUploadPicurePopup] = useState(false);
  const [deletePicurePopup, setDeletePicurePopup] = useState(false);
  const [deleteProfilePopup, setDeleteProfilePopup] = useState(false);

  /**
   * Defines fetching latest profile data
   */
  const fetchProfile = useCallback(async () => {
    setIsLoading(true);

    try {
      const { profile } = await api.client.getClientProfile();
      setProfile(profile);
    } finally {
      setIsLoading(false);
    }
  }, [setProfile]);

  /**
   *  Fetches on mount to keep profile data always up to date
   */
  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  // While fetching latest profile data show loading spinner
  if (isLoading) return <Spinner />;

  // Upload picture popup state handlers
  const openUploadPicurePopup = () => setUploadPicurePopup(true);
  const closeUploadPicurePopup = () => setUploadPicurePopup(false);

  // Delete picture popup state handlers
  const openDeletePicurePopup = () => setDeletePicurePopup(true);
  const closeDeletePicurePopup = () => setDeletePicurePopup(false);

  // Delete profile popup state handlers
  const openDeleteProfilePopup = () => setDeleteProfilePopup(true);
  const closeDeleteProfilePopup = () => setDeleteProfilePopup(false);

  /**
   * Handles uploading a new profile picture
   */
  const handleUploadPicure = async (file) => {
    await api.image.uploadProfileImage(file);
    closeUploadPicurePopup();
    await fetchProfile();
  };

  /**
   * Handles deleting a new profile picture
   */
  const handleDeletePicure = async () => {
    await api.image.deleteProfileImage();
    closeDeletePicurePopup();
    await fetchProfile();
  };

  /**
   * Handles deleting a new profile picture
   */
  const handleDeleteProfile = async () => {
    await api.client.deleteClientProfile();
    closeDeleteProfilePopup();
    await logout();
  };

  /**
   * Validate at least one field is provided, matching backend logic
   */
  const validateUpdateProfile = ({ username, name, surname, phone_number }) => {
    if (
      (!username || username.trim() === '') &&
      (!name || name.trim() === '') &&
      (!surname || surname.trim() === '') &&
      (!phone_number || phone_number.trim() === '')
    ) {
      return 'Provide at least one field to update: Username, Name, Surname or Phone Number.';
    }
    return undefined;
  };

  /**
   * Handles form submission for updating the profile data
   * Send only the filled fields to the API
   */
  const handleUpdateProfile = async ({ username, name, surname, phone_number }) => {
    setIsUpdatingProfile(true);

    const payload = {};
    if (username && username.trim() !== '') payload.username = username.trim();
    if (name && name.trim() !== '') payload.name = name.trim();
    if (surname && surname.trim() !== '') payload.surname = surname.trim();
    if (phone_number && phone_number.trim() !== '') payload.phone_number = phone_number.trim();

    try {
      await api.client.updateClientProfile(payload);
      await fetchProfile(); // Refresh profile after update
    } finally {
      setIsUpdatingProfile(false);
    }
  };

  return (
    <>
      <div className={styles.clientSettings}>
        <StatCard icon="pen" label="Update Profile">
          {/* Profile Picture Management */}
          <section className={styles.profileImageSection}>
            <ProfileImage src={profile.profile_image} size="15rem" />

            <div className={styles.imageAction}>
              <Button
                className={styles.actionBtn}
                type="button"
                color="primary"
                size="md"
                onClick={openUploadPicurePopup} //
              >
                <Icon name="plus" size="ty" />
                <span>Upload picture</span>
              </Button>

              <Button
                className={styles.actionBtn}
                type="button"
                color="translight"
                autoIconInvert
                size="md"
                onClick={openDeletePicurePopup} //
              >
                <Icon name="trash" size="ty" black />
                <span>Delete picture</span>
              </Button>
            </div>
          </section>

          {/* Profile Updating Management  */}
          <section className={styles.updateProfileSection}>
            <Form
              className={styles.updateProfileForm}
              initialFields={{ username: '', name: '', surname: '', phone_number: '' }}
              onSubmit={handleUpdateProfile}
              validate={validateUpdateProfile} //
            >
              <div className={styles.inputGroup}>
                <Input
                  label="Username"
                  name="username"
                  type="text"
                  placeholder={profile.username}
                  size="md"
                  disabled={isUpdatingProfile}
                />
                <Input
                  label="Phone Number"
                  name="phone_number"
                  type="tel"
                  placeholder={profile.phone_number}
                  size="md"
                  disabled={isUpdatingProfile}
                />
              </div>

              <div className={styles.inputGroup}>
                <Input
                  label="Name"
                  name="name"
                  type="text"
                  placeholder={profile.name}
                  size="md"
                  disabled={isUpdatingProfile}
                />
                <Input
                  label="Surname"
                  name="surname"
                  type="text"
                  placeholder={profile.surname}
                  size="md"
                  disabled={isUpdatingProfile}
                />
              </div>

              <Button
                className={styles.saveBtn}
                type="submit"
                size="md"
                color="primary"
                disabled={isUpdatingProfile}
                wide
              >
                <span className={styles.line}>
                  {isUpdatingProfile ? (
                    <>
                      <Spinner size="sm" /> Saving...
                    </>
                  ) : (
                    'Save Changes'
                  )}
                </span>
              </Button>

              <Error />
            </Form>
          </section>
        </StatCard>

        {/* Profile Deletion Management */}
        <StatCard icon="trash" label="Delete Profile">
          <section className={styles.deleteProfileSection}>
            <Button
              className={styles.actionBtn}
              type="button"
              color="translight"
              autoIconInvert
              size="md"
              onClick={openDeleteProfilePopup} //
            >
              <Icon name="warning" size="ty" black />
              <span>Delete profile</span>
            </Button>
          </section>
        </StatCard>
      </div>

      <UploadPicturePopup
        open={uploadPicurePopup}
        onClose={closeUploadPicurePopup}
        onUpload={handleUploadPicure} //
      />

      <DeletePicturePopup
        open={deletePicurePopup}
        onClose={closeDeletePicurePopup}
        onDelete={handleDeletePicure} //
      />

      <DeleteProfilePopup
        open={deleteProfilePopup}
        onClose={closeDeleteProfilePopup}
        onDelete={handleDeleteProfile} //
      />
    </>
  );
}

export default ClientSettings;
