import styles from "./SourceBadge.module.css";

interface SourceBadgeProps {
  source: string;
}

export function SourceBadge({ source }: SourceBadgeProps) {
  return <span className={styles.badge}>{source}</span>;
}
