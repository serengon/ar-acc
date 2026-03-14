import type { ReactNode } from "react";

import styles from "./FeatureCard.module.css";

interface FeatureCardProps {
  icon: ReactNode;
  iconBg: string;
  title: string;
  description: string;
}

export function FeatureCard({
  icon,
  iconBg,
  title,
  description,
}: FeatureCardProps) {
  return (
    <div className={styles.card}>
      <div
        className={styles.icon}
        style={{ background: iconBg }}
      >
        {icon}
      </div>
      <div className={styles.body}>
        <h3 className={styles.title}>{title}</h3>
        <p className={styles.description}>{description}</p>
      </div>
    </div>
  );
}
