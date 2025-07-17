import styles from './NotFound.module.scss';

import Hero from '@components/common/Hero/Hero';
import Button from '@components/common/Button/Button';
import Image from '@components/common/Image/Image';

function NotFound() {
  return (
    <Hero>
      <Hero.Left>
        <section>
          <h1 className={styles.title}>
            <p>404</p>
            <p>NOT FOUND</p>
          </h1>
          <p className={styles.subtitle}>Oops! We can&apos;t seem to find the page you&apos;re looking for.</p>
          <div className={styles.desc}>
            <p>The page may have moved, or the URL may be incorrect.</p>
            <p>Go back to the homepage and continue browsing.</p>
          </div>
          <Button href="/" color="transdark" size="md" width="content">
            Go back to home
          </Button>
        </section>
      </Hero.Left>

      <Hero.Right>
        <section>
          <Image className={styles.logo} name="notfound" />
        </section>
      </Hero.Right>
    </Hero>
  );
}

export default NotFound;
