import styles from './NotFoundPage.module.scss';

import Button from '@components/common/Button/Button';

export default function NotFoundPage() {
  return (
    <div className={styles.container}>
      <div className={styles.left}>
        <h1 className={styles.title}>
          404
          <br />
          NOT FOUND
        </h1>
        <p className={styles.subtitle}>Oops! We can&apos;t seem to find the page you&apos;re looking for.</p>
        <p className={styles.desc}>
          The page may have moved, or the URL may be incorrect.
          <br />
          Go back to the homepage and continue browsing.
        </p>

        <Button href="/" color="accent" size="lg" width="content">
          GO HOME
        </Button>
      </div>

      <div className={styles.right}>
        <img className={styles.logo} src="/assets/images/logo.png" alt="Logo" />
      </div>
    </div>
  );
}
