import styles from "./Spinner.module.css";

interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  variant?: "ring" | "scan";
}

export function Spinner({ size = "md", variant = "ring" }: SpinnerProps) {
  if (variant === "scan") {
    return <span className={`${styles.scan} ${styles[size]}`} role="status" />;
  }
  return <span className={`${styles.spinner} ${styles[size]}`} role="status" />;
}
