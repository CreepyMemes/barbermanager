import styles from './ProfileImage.module.scss';
import Image from '@components/common/Image/Image';

function ProfileImage({ src, size = '4rem' }) {
  // Support size as number (pixels) or as string
  const imgSize = typeof size === 'number' ? `${size}px` : size;

  return (
    <div className={styles.profileImage} style={{ width: imgSize, height: imgSize }}>
      <Image
        className={styles.image}
        src={src}
        name="avatar"
        alt="Profile Image"
        style={{ width: imgSize, height: imgSize }} //
      />
    </div>
  );
}

export default ProfileImage;
