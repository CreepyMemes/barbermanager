import { Children } from 'react';
import styles from './SidePanel.module.scss';

import Logo from '@components/common/Logo/Logo';

function SidePanel({ heading, children }) {
  // Extracts first SidePanelInner and SidePanelActions children by displayName
  const [inner, actions] = ['SidePanelInner', 'SidePanelActions'].map((name) =>
    Children.toArray(children).find((child) => child.type.displayName === name),
  );

  return (
    <section className={styles.sidePanel}>
      <h1 className={styles.heading}>{heading}</h1>

      <div className={styles.container}>
        <Logo size="hg" split />
        {inner}
      </div>

      {actions}
    </section>
  );
}

// Simple Inner and Actions subcomponents
const Inner = ({ children }) => {
  // return <div className={styles.inner}>{children}</div>;
  return <>{children}</>;
};

const Actions = ({ children }) => {
  return <div className={styles.actions}>{children}</div>;
};

// Set display names for subcomponent identification
Inner.displayName = 'SidePanelInner';
Actions.displayName = 'SidePanelActions';

// Attach to main component for namespacing
SidePanel.Inner = Inner;
SidePanel.Actions = Actions;

export default SidePanel;
