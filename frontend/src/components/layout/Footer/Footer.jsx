import styles from './Footer.module.scss';

import Logo from '@components/common/Logo/Logo';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';

function Footer() {
  return (
    <footer className={styles.footerArea}>
      <div className={styles.footer}>
        <Logo size="md" />

        <ul className={styles.links}>
          <li>
            <Button href="https://github.com/CreepyMemes/barbermanager" size="md" color="animated">
              <Icon name="github" size={'md'} />
            </Button>
          </li>

          <li>
            <Button href="https://github.com/CreepyMemes/barbermanager/tree/master/docs" size="md" color="animated">
              <Icon name="docs" size={'md'} />
            </Button>
          </li>

          <li>
            <Button href="https://github.com/CreepyMemes/barbermanager/issues/new" size="md" color="animated">
              <Icon name="bug" size={'md'} />
            </Button>
          </li>
        </ul>

        <div className={styles.copyright}>&copy; {new Date().getFullYear()} CreepyMemes. All rights reserved.</div>
      </div>
    </footer>
  );
}

export default Footer;
