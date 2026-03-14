import type { PatternResult } from "@/api/client";
import { MoneyLabel } from "@/components/common/MoneyLabel";
import { SourceBadge } from "@/components/common/SourceBadge";

import styles from "./PatternResultCard.module.css";

interface PatternResultCardProps {
  result: PatternResult;
  onEntityClick?: (entityId: string) => void;
}

export function PatternResultCard({ result, onEntityClick }: PatternResultCardProps) {
  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <span className={styles.patternName}>{result.pattern_name}</span>
        <span className={styles.sources}>
          {result.sources.map((s) => (
            <SourceBadge key={s.database} source={s.database} />
          ))}
        </span>
      </div>
      <p className={styles.description}>{result.description}</p>
      <div className={styles.data}>
        {Object.entries(result.data).map(([key, value]) => (
          <div key={key} className={styles.field}>
            <span className={styles.fieldKey}>{key}</span>
            <span className={styles.fieldValue}>
              {typeof value === "number" && key.includes("value") ? (
                <MoneyLabel value={value} />
              ) : (
                String(value ?? "")
              )}
            </span>
          </div>
        ))}
      </div>
      {result.entity_ids.length > 0 && (
        <div className={styles.entities}>
          {result.entity_ids.map((id) => (
            <button
              key={id}
              className={styles.entityLink}
              onClick={() => onEntityClick?.(id)}
              type="button"
            >
              {id}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
