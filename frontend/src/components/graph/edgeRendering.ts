import { EDGE_COLORS } from "./graphConstants";

interface EdgeRenderOptions {
  sourceX: number;
  sourceY: number;
  targetX: number;
  targetY: number;
  type: string;
  confidence: number;
  value: number;
  isDimmed: boolean;
}

export function renderEdge(
  ctx: CanvasRenderingContext2D,
  opts: EdgeRenderOptions,
): void {
  const { sourceX, sourceY, targetX, targetY, type, confidence, value, isDimmed } =
    opts;
  const color = EDGE_COLORS[type] ?? "rgba(255, 255, 255, 0.12)";
  const alpha = isDimmed ? 0.05 : 0.4;

  // Width based on confidence + value
  const baseWidth = confidence >= 0.9 ? 1.5 : 0.5;
  const valueWidth =
    value > 0 ? Math.min(3, Math.log10(value + 1) * 0.4) : 0;
  const width = baseWidth + valueWidth;

  ctx.beginPath();
  ctx.moveTo(sourceX, sourceY);
  ctx.lineTo(targetX, targetY);
  ctx.strokeStyle = color;
  ctx.globalAlpha = alpha;
  ctx.lineWidth = width;

  // Dashed if low confidence
  if (confidence < 0.9) {
    ctx.setLineDash([4, 2]);
  } else {
    ctx.setLineDash([]);
  }

  ctx.stroke();
  ctx.setLineDash([]);
  ctx.globalAlpha = 1;
}
