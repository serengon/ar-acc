import { memo } from "react";
import { useTranslation } from "react-i18next";
import { ArrowLeft, Plus } from "lucide-react";

import type { EntityDetail, ExposureResponse } from "@/api/client";
import { entityColors } from "@/styles/tokens";

import { ScoreRing } from "./ScoreRing";
import styles from "./EntityHeader.module.css";

interface EntityHeaderProps {
  entity: EntityDetail;
  exposure: ExposureResponse | null;
  onBack: () => void;
  onAddToInvestigation: () => void;
}

function formatMoney(value: number): string {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
    notation: "compact",
  }).format(value);
}

function EntityHeaderInner({
  entity,
  exposure,
  onBack,
  onAddToInvestigation,
}: EntityHeaderProps) {
  const { t } = useTranslation();

  const rawName =
    entity.properties.nome ??
    entity.properties.razao_social ??
    entity.properties.name ??
    entity.id;
  const name = typeof rawName === "string" ? rawName : String(rawName);

  const typeColor = entityColors[entity.type] ?? "var(--text-muted)";

  const connectionCount = exposure?.factors.find((f) => f.name === "connections")?.value;
  const sourceCount = exposure?.factors.find((f) => f.name === "sources")?.value ?? entity.sources.length;
  const totalMoney = exposure?.factors.find((f) => f.name === "financial");

  return (
    <header className={styles.header}>
      <button
        className={styles.backBtn}
        onClick={onBack}
        aria-label={t("common.back")}
      >
        <ArrowLeft size={16} />
      </button>

      <span className={styles.name}>{name}</span>

      <span className={styles.typeBadge}>
        <span
          className={styles.typeDot}
          style={{ backgroundColor: typeColor }}
        />
        {t(`entity.${entity.type}`, entity.type)}
      </span>

      {exposure && (
        <ScoreRing value={exposure.exposure_index} size={40} />
      )}

      <div className={styles.sourceBadges}>
        {entity.sources.map((s) => (
          <span key={s.database} className={styles.sourcePill}>
            {s.database}
          </span>
        ))}
      </div>

      <div className={styles.stats}>
        {connectionCount != null && (
          <span className={styles.stat}>
            {connectionCount} {t("common.connections")}
          </span>
        )}
        <span className={styles.stat}>
          {sourceCount} {t("common.sources")}
        </span>
        {totalMoney && (
          <span className={styles.stat}>{formatMoney(totalMoney.value)}</span>
        )}
      </div>

      <button className={styles.addBtn} onClick={onAddToInvestigation}>
        <Plus size={14} />
        {t("investigation.addEntity")}
      </button>
    </header>
  );
}

export const EntityHeader = memo(EntityHeaderInner);
