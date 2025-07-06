import { useState } from 'react';
import styles from './Pagination.module.scss';

import StatCard from '@components/common/StatCard/StatCard';
import Icon from '@components/common/Icon/Icon';
import Button from '@components/common/Button/Button';

function Pagination({ icon, label, children, itemsPerPage = 3, emptyMessage = 'No items' }) {
  const items = Array.isArray(children) ? children : children ? [children] : [];
  const [page, setPage] = useState(0);
  const pageCount = Math.ceil(items.length / itemsPerPage);

  // children for current page
  let pageItems = items.slice(page * itemsPerPage, (page + 1) * itemsPerPage);

  return (
    <StatCard className={styles.paginationCard} icon={icon} label={label}>
      <ul className={styles.list}>
        {items.length > 0 ? (
          pageItems.map((item, idx) => (
            <li className={styles.listItem} key={item.key || idx}>
              {item}
            </li>
          ))
        ) : (
          <li className={styles.empty}>{emptyMessage}</li>
        )}
      </ul>

      {pageCount > 1 && (
        <nav className={styles.paginationNav}>
          <Button
            className={styles.pageButton}
            type="button"
            onClick={() => setPage(page - 1)}
            color="animated"
            size="sm"
            disabled={page === 0}
          >
            <Icon name={'left'} size="sm" black />
          </Button>

          <span className={styles.pageStatus}>
            Page {page + 1} / {pageCount}
          </span>

          <Button
            className={styles.pageButton}
            type="button"
            onClick={() => setPage(page + 1)}
            color="animated"
            size="sm"
            disabled={page + 1 >= pageCount}
          >
            <Icon name={'right'} size="sm" black />
          </Button>
        </nav>
      )}
    </StatCard>
  );
}

export default Pagination;
