import styles from './Profile.module.scss';

import ProfileImage from '@components/common/ProfileImage/ProfileImage';

function Profile({ profile }) {
  return (
    <div className={styles.profile}>
      <ProfileImage src={profile.profile_image} />

      <div className={styles.profileText}>
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
