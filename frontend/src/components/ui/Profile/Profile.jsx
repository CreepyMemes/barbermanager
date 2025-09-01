import styles from './Profile.module.scss';

import Spinner from '@components/common/Spinner/Spinner';
import ProfileImage from '@components/ui/ProfileImage/ProfileImage';

function Profile({ profile, imageSize, className, fontSize = '1.3rem', loading }) {
  // Get all style classes into a string
  const computedClassName = [className, styles.profile].join(' ');

  // Render loading spinner if profile data is still loading
  if (loading || !profile) {
    return <Spinner size="sm" />;
  }
  return (
    <div className={computedClassName}>
      <ProfileImage src={profile.profile_image} size={imageSize} />

      <div className={styles.profileText} style={{ fontSize: fontSize }}>
        {profile.name && profile.surname && (
          <div className={styles.fullname}>
            <span>
              {profile.name} {profile.surname}
            </span>
          </div>
        )}

        {(!profile.name || !profile.surname) && (
          <div className={styles.noname}>
            <span>[no name]</span>
          </div>
        )}

        <div className={styles.username}>{profile.username}</div>
      </div>
    </div>
  );
}

export default Profile;
