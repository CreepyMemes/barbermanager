import { useState, useEffect, Children } from 'react';
import styles from './Pagination.module.scss';

import StatCard from '@components/ui/StatCard/StatCard';
import Icon from '@components/common/Icon/Icon';
import Button from '@components/common/Button/Button';
import Spinner from '@components/common/Spinner/Spinner';

function Pagination({ icon, label, children, itemsPerPage = 3, loading, emptyMessage = 'No items' }) {
  // Extracts first PaginationColumn and PaginationRow children by displayName
  const [action, columns, rows] = [Action.displayName, Column.displayName, Row.displayName].map((name) =>
    Children.toArray(children).filter((child) => child.type.displayName === name),
  );

  // Pagination state
  const [page, setPage] = useState(0);
  const pageCount = Math.ceil(rows.length / itemsPerPage);
  const pageRows = rows.slice(page * itemsPerPage, (page + 1) * itemsPerPage);

  // Generates a stable row identity signature for pagination reset logic
  const rowKeys = rows.map((r) => r.key).join(',');

  /**
   *  Always reset to first page when table content or paging changes
   */
  useEffect(() => {
    setPage(0);
  }, [rowKeys, itemsPerPage]);

  return (
    <StatCard icon={icon} label={label}>
      {action}
      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead className={styles.tableHead}>
            <tr>
              {columns.map((column, idx) => (
                <th className={styles.tableHeadRow} key={idx}>
                  {column.props.children}
                </th>
              ))}
            </tr>
          </thead>

          <tbody className={styles.tableBody}>
            {loading && (
              <tr>
                <td colSpan={columns.length || 1} className={styles.empty}>
                  <Spinner />
                </td>
              </tr>
            )}

            {!loading &&
              rows.length > 0 &&
              pageRows.map((row, ridx) => {
                const cells = Children.toArray(row.props.children).filter(
                  (cell) => cell.type.displayName === Cell.displayName,
                );

                return (
                  <tr key={row.key || ridx}>
                    {cells.map((cell, cidx) => (
                      <td className={styles.tableBodyRow} key={cidx}>
                        {cell.props.children}
                      </td>
                    ))}
                  </tr>
                );
              })}

            {!loading && rows.length === 0 && (
              <tr>
                <td colSpan={columns.length || 1} className={styles.empty}>
                  {emptyMessage}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination nav */}
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
            <Icon name="left" size="sm" black />
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
            <Icon name="right" size="sm" black />
          </Button>
        </nav>
      )}
    </StatCard>
  );
}

// Subcomponents for clean declarative
const Action = ({ children }) => <>{children}</>;
const Column = ({ children }) => <>{children}</>;
const Row = ({ children }) => <>{children}</>;
const Cell = ({ children }) => <>{children}</>;

// Set display names for subcomponent identification
Action.displayName = 'PaginationAction';
Column.displayName = 'PaginationColumn';
Row.displayName = 'PaginationRow';
Cell.displayName = 'PaginationCell';

// Attach to main component for namespacing
Pagination.Action = Action;
Pagination.Column = Column;
Pagination.Row = Row;
Pagination.Cell = Cell;

export default Pagination;
