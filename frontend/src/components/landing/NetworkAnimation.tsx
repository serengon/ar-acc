import styles from "./NetworkAnimation.module.css";

const nodes = [
  { cx: 120, cy: 80, color: "var(--data-person)", delay: 0 },
  { cx: 280, cy: 60, color: "var(--data-company)", delay: 0.1 },
  { cx: 450, cy: 100, color: "var(--data-election)", delay: 0.2 },
  { cx: 600, cy: 70, color: "var(--data-contract)", delay: 0.3 },
  { cx: 180, cy: 200, color: "var(--data-sanction)", delay: 0.4 },
  { cx: 350, cy: 180, color: "var(--data-amendment)", delay: 0.5 },
  { cx: 520, cy: 220, color: "var(--data-person)", delay: 0.6 },
  { cx: 80, cy: 300, color: "var(--data-company)", delay: 0.7 },
  { cx: 250, cy: 320, color: "var(--data-election)", delay: 0.8 },
  { cx: 420, cy: 340, color: "var(--data-contract)", delay: 0.9 },
  { cx: 580, cy: 310, color: "var(--data-sanction)", delay: 1.0 },
  { cx: 700, cy: 180, color: "var(--data-amendment)", delay: 1.1 },
  { cx: 150, cy: 400, color: "var(--data-person)", delay: 1.2 },
  { cx: 480, cy: 420, color: "var(--data-company)", delay: 1.3 },
];

const edges = [
  { x1: 120, y1: 80, x2: 280, y2: 60, delay: 0.2 },
  { x1: 280, y1: 60, x2: 450, y2: 100, delay: 0.3 },
  { x1: 450, y1: 100, x2: 600, y2: 70, delay: 0.4 },
  { x1: 120, y1: 80, x2: 180, y2: 200, delay: 0.5 },
  { x1: 280, y1: 60, x2: 350, y2: 180, delay: 0.6 },
  { x1: 350, y1: 180, x2: 520, y2: 220, delay: 0.7 },
  { x1: 180, y1: 200, x2: 80, y2: 300, delay: 0.8 },
  { x1: 80, y1: 300, x2: 250, y2: 320, delay: 0.9 },
  { x1: 250, y1: 320, x2: 420, y2: 340, delay: 1.0 },
  { x1: 520, y1: 220, x2: 580, y2: 310, delay: 1.1 },
  { x1: 600, y1: 70, x2: 700, y2: 180, delay: 1.2 },
  { x1: 420, y1: 340, x2: 480, y2: 420, delay: 1.3 },
];

export function NetworkAnimation() {
  return (
    <div className={styles.container} aria-hidden="true">
      <svg
        className={styles.svg}
        viewBox="0 0 800 500"
        preserveAspectRatio="xMidYMid slice"
      >
        {edges.map((edge, i) => (
          <line
            key={`e${i}`}
            x1={edge.x1}
            y1={edge.y1}
            x2={edge.x2}
            y2={edge.y2}
            className={styles.edge}
            strokeDasharray="200"
            strokeDashoffset="200"
            style={{ animationDelay: `${edge.delay}s` }}
          />
        ))}
        {nodes.map((node, i) => (
          <circle
            key={`n${i}`}
            cx={node.cx}
            cy={node.cy}
            r="6"
            fill={node.color}
            className={styles.node}
            style={{ animationDelay: `${node.delay}s` }}
          />
        ))}
      </svg>
    </div>
  );
}
