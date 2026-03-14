import { memo } from "react";

import styles from "./ScoreRing.module.css";

interface ScoreRingProps {
  value: number;
  size?: number;
  className?: string;
}

function ScoreRingInner({ value, size = 48, className }: ScoreRingProps) {
  const clamped = Math.max(0, Math.min(100, value));
  const strokeWidth = size >= 64 ? 4 : 3;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - clamped / 100);

  // Interpolate from muted gray to amber based on value
  const t = clamped / 100;
  const r = Math.round(90 + t * (255 - 90));
  const g = Math.round(107 + t * (154 - 107));
  const b = Math.round(96 + t * (60 - 96));
  const strokeColor = `rgb(${String(r)}, ${String(g)}, ${String(b)})`;

  return (
    <div
      className={`${styles.ring} ${className ?? ""}`}
      style={{ width: size, height: size }}
    >
      <svg viewBox={`0 0 ${String(size)} ${String(size)}`} className={styles.svg}>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="var(--text-muted)"
          strokeOpacity={0.2}
          strokeWidth={strokeWidth}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={strokeColor}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className={styles.foreground}
          transform={`rotate(-90 ${String(size / 2)} ${String(size / 2)})`}
        />
      </svg>
      <span
        className={styles.value}
        style={{ fontSize: size >= 64 ? 16 : 12 }}
      >
        {Math.round(clamped)}
      </span>
    </div>
  );
}

export const ScoreRing = memo(ScoreRingInner);
