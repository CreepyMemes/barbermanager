const RADIUS = 32;
const STROKE = 8;
const CIRCUM = 2 * Math.PI * RADIUS;

function CakeChart({ value, max = 5, color = '#fec84b', size = 80 }) {
  const percent = value / max;
  const dash = percent * CIRCUM;

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={size / 2} cy={size / 2} r={RADIUS} stroke="#f3f3f3" strokeWidth={STROKE} fill="none" />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={RADIUS}
        stroke={color}
        strokeWidth={STROKE}
        fill="none"
        strokeDasharray={`${dash} ${CIRCUM - dash}`}
        strokeDashoffset={CIRCUM / 4}
        strokeLinecap="round"
        style={{ transition: 'stroke-dasharray 0.3s' }}
      />

      <text x="50%" y="50%" textAnchor="middle" dy="0.3em" fontSize="2rem" fontWeight="700" fill="#1b1b1b">
        {value}{' '}
        <tspan fontSize="1.2rem" fontWeight="400">
          / {max}
        </tspan>
      </text>
    </svg>
  );
}
export default CakeChart;
