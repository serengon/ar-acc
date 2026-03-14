import { useTranslation } from "react-i18next";

import styles from "./ConfidenceBadge.module.css";

interface ConfidenceBadgeProps {
  confidence: number;
}

export function ConfidenceBadge({ confidence }: ConfidenceBadgeProps) {
  const { t } = useTranslation();
  const isSolid = confidence >= 90;
  const percent = Math.round(confidence);

  return (
    <span
      className={`${styles.badge} ${isSolid ? styles.solid : styles.dashed}`}
      title={`${t("common.confidence")}: ${percent}%`}
    >
      {percent}%
    </span>
  );
}
