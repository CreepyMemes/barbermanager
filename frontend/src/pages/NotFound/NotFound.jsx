import styles from './NotFound.module.scss';
import logo from '@assets/images/notfound-logo.png';

import Hero from '@components/common/Hero/Hero';
import Button from '@components/common/Button/Button';

export default function NotFound() {
  return (
    <Hero>
      <Hero.Left>
        <div className={styles.textContainer}>
          <h1 className={styles.title}>
            <p>404</p>
            <p>NOT FOUND</p>
          </h1>
          <p className={styles.subtitle}>Oops! We can&apos;t seem to find the page you&apos;re looking for.</p>
          <p className={styles.desc}>
            <p>The page may have moved, or the URL may be incorrect.</p>
            <p>Go back to the homepage and continue browsing.</p>
          </p>
          <Button href="/" color="accent" size="lg" width="content">
            GO HOME
          </Button>
        </div>
      </Hero.Left>

      <Hero.Right>
        <div className={styles.imageContainer}>
          <img className={styles.logo} src={logo} alt="Logo" />
        </div>
      </Hero.Right>
    </Hero>
  );
}
