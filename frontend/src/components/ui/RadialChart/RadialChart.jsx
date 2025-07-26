import styles from './RadialChart.module.scss';

const RADIUS = 100 / (Math.PI * 2);

export default function RadialChart({ value, max = 5, color = '#fed54f', size = 80 }) {
  return (
    <svg
      viewBox="0 0 36 36"
      className={styles.radialChart}
      width={size}
      height={size} //
    >
      <path
        className={styles.circleBg}
        d={`
              M18 2.0845
              a ${RADIUS} ${RADIUS} 0 0 1 0 ${2 * RADIUS}
              a ${RADIUS} ${RADIUS} 0 0 1 0 -${2 * RADIUS}
            `}
      />
      <path
        className={styles.circle}
        style={{ stroke: color }}
        strokeDasharray={`${(value / max) * 100}, 100`}
        d={`
              M18 2.0845
              a ${RADIUS} ${RADIUS} 0 0 1 0 ${2 * RADIUS}
              a ${RADIUS} ${RADIUS} 0 0 1 0 -${2 * RADIUS}
            `}
      />
      <text x="18" y="20.35" className={styles.numerator}>
        {value} <tspan className={styles.denominator}> / {max}</tspan>
      </text>
    </svg>
  );
}
