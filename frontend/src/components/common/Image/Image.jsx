import images from '@assets/images';
import styles from './Image.module.scss';

function Image({ src, name, className, alt }) {
  const isValidSrc = typeof src === 'string' && src.trim() !== '';
  const imgSrc = isValidSrc ? src : images[name];

  if (!imgSrc) return null;
  return <img src={imgSrc} className={className} alt={alt || name} />;
}

export default Image;
