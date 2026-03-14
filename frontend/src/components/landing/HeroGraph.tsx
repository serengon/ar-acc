import styles from "./HeroGraph.module.css";

interface GraphNode {
  x: number;
  y: number;
  r: number;
  color: string;
  label: string;
  pulse?: boolean;
}

interface GraphEdge {
  from: number;
  to: number;
}

const nodes: GraphNode[] = [
  { x: 400, y: 80, r: 18, color: "#4EA8DE", label: "Político A", pulse: true },
  { x: 200, y: 140, r: 14, color: "#E07A5F", label: "Empresa X" },
  { x: 600, y: 130, r: 14, color: "#E07A5F", label: "Empresa Y" },
  { x: 120, y: 60, r: 10, color: "#F2CC8F", label: "Contrato" },
  { x: 300, y: 220, r: 12, color: "#81B29A", label: "Doação" },
  { x: 500, y: 210, r: 12, color: "#E56B6F", label: "Sanção" },
  { x: 680, y: 60, r: 10, color: "#B8A9C9", label: "Emenda" },
  { x: 100, y: 200, r: 8, color: "#4EA8DE", label: "Pessoa B" },
  { x: 700, y: 200, r: 8, color: "#4EA8DE", label: "Pessoa C" },
  { x: 400, y: 260, r: 10, color: "#3B82F6", label: "BNDES" },
];

const edges: GraphEdge[] = [
  { from: 0, to: 1 },
  { from: 0, to: 2 },
  { from: 1, to: 3 },
  { from: 0, to: 4 },
  { from: 2, to: 5 },
  { from: 2, to: 6 },
  { from: 1, to: 7 },
  { from: 2, to: 8 },
  { from: 0, to: 9 },
  { from: 4, to: 1 },
  { from: 5, to: 6 },
];

export function HeroGraph() {
  return (
    <div className={styles.container} aria-hidden="true">
      <div className={styles.frame}>
        <div className={styles.toolbar}>
          <span className={styles.dot} />
          <span className={styles.dot} />
          <span className={styles.dot} />
          <span className={styles.toolbarLabel}>graph-explorer</span>
        </div>
        <div className={styles.canvas}>
          <svg className={styles.svg} viewBox="0 0 800 280" preserveAspectRatio="xMidYMid meet">
            {edges.map((edge, i) => {
              const from = nodes[edge.from];
              const to = nodes[edge.to];
              if (!from || !to) return null;
              return (
                <line
                  key={`e${i}`}
                  x1={from.x}
                  y1={from.y}
                  x2={to.x}
                  y2={to.y}
                  className={styles.edgeLine}
                  style={{ animationDelay: `${i * 0.08}s` }}
                />
              );
            })}
            {nodes.map((node, i) => (
              <g
                key={`n${i}`}
                className={styles.node}
                style={{ animationDelay: `${0.3 + i * 0.06}s` }}
              >
                <circle
                  cx={node.x}
                  cy={node.y}
                  r={node.r}
                  fill={node.color}
                  className={`${styles.nodeCircle} ${node.pulse ? styles.pulse : ""}`}
                  style={{ "--glow": node.color } as React.CSSProperties}
                />
                <text
                  x={node.x}
                  y={node.y + node.r + 14}
                  className={styles.nodeLabel}
                  style={{ animationDelay: `${0.6 + i * 0.06}s` }}
                >
                  {node.label}
                </text>
              </g>
            ))}
          </svg>
          <div className={styles.fadeOverlay} />
        </div>
      </div>
    </div>
  );
}
