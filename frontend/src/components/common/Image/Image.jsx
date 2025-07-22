import images from '@assets/images';

function Image({ src, name, className, alt, style }) {
  const isValidSrc = typeof src === 'string' && src.trim() !== '';
  const imgSrc = isValidSrc ? src : images[name];

  if (!imgSrc) return null;
  return <img src={imgSrc} className={className} alt={alt || name} style={style} />;
}

export default Image;
