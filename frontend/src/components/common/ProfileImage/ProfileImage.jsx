import styles from './ProfileImage.module.scss';

import Image from '@components/common/Image/Image';

function ProfileImage({ src }) {
  return (
    <div className={styles.profileImage}>
      <Image className={styles.image} src={src} name="avatar" alt="Profile Image" />
    </div>
  );
}

export default ProfileImage;
