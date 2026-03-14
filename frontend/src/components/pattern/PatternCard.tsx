import { useTranslation } from "react-i18next";

import type { PatternInfo } from "@/api/client";

import styles from "./PatternCard.module.css";

interface PatternCardProps {
  pattern: PatternInfo;
  active?: boolean;
  onClick?: (patternId: string) => void;
}

export function PatternCard({ pattern, active, onClick }: PatternCardProps) {
  const { i18n } = useTranslation();
  const lang = i18n.language === "pt-BR" ? "pt" : "en";
  const name = lang === "pt" ? pattern.name_pt : pattern.name_en;
  const description = lang === "pt" ? pattern.description_pt : pattern.description_en;

  return (
    <button
      className={`${styles.card} ${active ? styles.active : ""}`}
      onClick={() => onClick?.(pattern.id)}
      type="button"
    >
      <h3 className={styles.name}>{name}</h3>
      <p className={styles.description}>{description}</p>
      <span className={styles.id}>{pattern.id}</span>
    </button>
  );
}
