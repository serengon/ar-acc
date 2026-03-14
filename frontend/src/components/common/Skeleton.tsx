import styles from "./Skeleton.module.css";

type SkeletonVariant = "text" | "rect" | "circle";

interface SkeletonProps {
  variant?: SkeletonVariant;
  width?: string;
  height?: string;
  className?: string;
}

export function Skeleton({
  variant = "text",
  width,
  height,
  className,
}: SkeletonProps) {
  const classNames = [
    styles.skeleton,
    styles[variant],
    className ?? "",
  ]
    .filter(Boolean)
    .join(" ");

  const style: React.CSSProperties = {};

  if (variant === "circle") {
    const size = width ?? height ?? "40px";
    style.width = size;
    style.height = size;
  } else {
    if (width) style.width = width;
    if (height) style.height = height;
  }

  return <div className={classNames} style={style} />;
}
