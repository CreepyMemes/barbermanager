import styles from './Rating.module.scss';

function Rating({ rating = 0, maxRating = 5 }) {
  const intRating = Math.floor(rating);
  const displayRating = Number(rating).toFixed(1);

  return (
    <div className={styles.reviewStars}>
      <div className={styles.rating}>
        <span className={styles.ratingValue}>{displayRating}</span>
        <div className={styles.starsContainer}>
          <span className={styles.stars}>
            {'★'.repeat(intRating)}
            {'☆'.repeat(maxRating - intRating)}
          </span>
        </div>
      </div>
    </div>
  );
}

export default Rating;
