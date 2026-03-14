import { memo, useEffect, useRef } from "react";

import { NODE_COLORS } from "./graphConstants";
import styles from "./GraphMinimap.module.css";

interface MinimapNode {
  x: number;
  y: number;
  type: string;
}

interface GraphMinimapProps {
  nodes: MinimapNode[];
  width?: number;
  height?: number;
}

const DEFAULT_WIDTH = 160;
const DEFAULT_HEIGHT = 120;
const DEBOUNCE_MS = 1000;

function GraphMinimapInner({
  nodes,
  width = DEFAULT_WIDTH,
  height = DEFAULT_HEIGHT,
}: GraphMinimapProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
    }

    timerRef.current = setTimeout(() => {
      const canvas = canvasRef.current;
      if (!canvas) return;

      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      ctx.clearRect(0, 0, width, height);

      if (nodes.length === 0) return;

      // Compute bounds
      let minX = Infinity;
      let maxX = -Infinity;
      let minY = Infinity;
      let maxY = -Infinity;

      for (const node of nodes) {
        if (node.x < minX) minX = node.x;
        if (node.x > maxX) maxX = node.x;
        if (node.y < minY) minY = node.y;
        if (node.y > maxY) maxY = node.y;
      }

      const rangeX = maxX - minX || 1;
      const rangeY = maxY - minY || 1;
      const padding = 8;
      const drawW = width - padding * 2;
      const drawH = height - padding * 2;

      for (const node of nodes) {
        const nx = padding + ((node.x - minX) / rangeX) * drawW;
        const ny = padding + ((node.y - minY) / rangeY) * drawH;
        const color =
          NODE_COLORS[node.type as keyof typeof NODE_COLORS] ?? "#5a6b60";

        ctx.beginPath();
        ctx.arc(nx, ny, 2, 0, 2 * Math.PI);
        ctx.fillStyle = color;
        ctx.fill();
      }
    }, DEBOUNCE_MS);

    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
    };
  }, [nodes, width, height]);

  return (
    <div className={styles.minimap}>
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        className={styles.canvas}
      />
    </div>
  );
}

export const GraphMinimap = memo(GraphMinimapInner);
