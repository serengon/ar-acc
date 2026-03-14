import {
  NODE_COLORS,
  NODE_SIZE_MIN,
  NODE_SIZE_MAX,
  NODE_SIZE_CENTER,
  LOD_DOTS_ONLY,
  LOD_ICONS,
  getIconImage,
} from "./graphConstants";

interface NodeRenderOptions {
  x: number;
  y: number;
  type: string;
  label: string;
  connectionCount: number;
  isCenter: boolean;
  isSelected: boolean;
  isHovered: boolean;
  isDimmed: boolean;
  isPep: boolean;
  zoom: number;
}

export function getNodeSize(
  connectionCount: number,
  isCenter: boolean,
): number {
  if (isCenter) return NODE_SIZE_CENTER;
  return Math.max(
    NODE_SIZE_MIN,
    Math.min(NODE_SIZE_MAX, NODE_SIZE_MIN + connectionCount * 0.8),
  );
}

export function renderNode(
  ctx: CanvasRenderingContext2D,
  opts: NodeRenderOptions,
): void {
  const {
    x,
    y,
    type,
    label,
    connectionCount,
    isCenter,
    isSelected,
    isHovered,
    isDimmed,
    zoom,
  } = opts;
  const color =
    NODE_COLORS[type as keyof typeof NODE_COLORS] ?? "#5a6b60";
  const radius = getNodeSize(connectionCount, isCenter);

  // Alpha based on dimming
  const alpha = isDimmed ? 0.15 : 1;
  ctx.globalAlpha = alpha;

  // Outer glow for selected/hovered
  if (!isDimmed && (isSelected || isHovered)) {
    const glowRadius = radius + (isSelected ? 6 : 4);
    const gradient = ctx.createRadialGradient(x, y, radius, x, y, glowRadius);
    gradient.addColorStop(0, isSelected ? "rgba(0, 229, 195, 0.4)" : "rgba(0, 229, 195, 0.2)");
    gradient.addColorStop(1, "rgba(0, 229, 195, 0)");
    ctx.beginPath();
    ctx.arc(x, y, glowRadius, 0, 2 * Math.PI);
    ctx.fillStyle = gradient;
    ctx.fill();
  }

  // Subtle ambient glow for all nodes
  if (!isDimmed && !isCenter) {
    const ambientR = radius + 3;
    const amb = ctx.createRadialGradient(x, y, radius * 0.8, x, y, ambientR);
    amb.addColorStop(0, color + "30");
    amb.addColorStop(1, color + "00");
    ctx.beginPath();
    ctx.arc(x, y, ambientR, 0, 2 * Math.PI);
    ctx.fillStyle = amb;
    ctx.fill();
  }

  // Center node gets a brighter glow
  if (isCenter && !isDimmed) {
    const centerGlow = radius + 8;
    const cg = ctx.createRadialGradient(x, y, radius * 0.5, x, y, centerGlow);
    cg.addColorStop(0, color + "50");
    cg.addColorStop(1, color + "00");
    ctx.beginPath();
    ctx.arc(x, y, centerGlow, 0, 2 * Math.PI);
    ctx.fillStyle = cg;
    ctx.fill();
  }

  // === LOD: Dots only (zoom < 0.5) ===
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, 2 * Math.PI);
  ctx.fillStyle = color;
  ctx.fill();

  // Selection ring
  if (isSelected) {
    ctx.strokeStyle = "#00e5c3";
    ctx.lineWidth = 2;
    ctx.stroke();
  } else if (isHovered) {
    ctx.strokeStyle = "rgba(0, 229, 195, 0.6)";
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }

  if (zoom < LOD_DOTS_ONLY) {
    ctx.globalAlpha = 1;
    return;
  }

  // === LOD: Icons (zoom 0.5-1.5) ===
  if (zoom >= LOD_DOTS_ONLY) {
    const iconSize = Math.round(radius * 1.2);
    const icon = getIconImage(type, "#060a07", iconSize);
    if (icon && icon.complete) {
      ctx.drawImage(icon, x - iconSize / 2, y - iconSize / 2, iconSize, iconSize);
    }
  }

  // === LOD: Full detail (zoom > 1.5) ===
  if (zoom > LOD_ICONS) {
    // Label with text shadow for readability
    const fontSize = isCenter ? 7 : 5.5;
    ctx.font = `500 ${fontSize}px "IBM Plex Sans", sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    // Dark shadow behind label
    ctx.fillStyle = "rgba(6, 10, 7, 0.7)";
    ctx.fillText(label, x + 0.5, y + radius + 3.5);
    // Label text
    ctx.fillStyle = isDimmed
      ? "rgba(232, 237, 233, 0.15)"
      : "rgba(232, 237, 233, 0.9)";
    ctx.fillText(label, x, y + radius + 3);

    // Connection count badge (top-right)
    if (connectionCount > 1) {
      const badgeRadius = 3.5;
      const bx = x + radius * 0.75;
      const by = y - radius * 0.75;
      ctx.beginPath();
      ctx.arc(bx, by, badgeRadius, 0, 2 * Math.PI);
      ctx.fillStyle = color;
      ctx.fill();
      ctx.font = `700 3px "IBM Plex Mono", monospace`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillStyle = "#060a07";
      ctx.fillText(String(connectionCount), bx, by);
    }
  }

  ctx.globalAlpha = 1;
}
