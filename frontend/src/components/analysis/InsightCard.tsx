import { memo } from "react";

import type { PatternResult } from "@/api/client";
import { entityColors } from "@/styles/tokens";

import styles from "./InsightCard.module.css";

interface InsightCardProps {
  pattern: PatternResult;
  onClick: () => void;
}

function formatMoney(value: number): string {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
    notation: "compact",
  }).format(value);
}

function InsightCardInner({ pattern, onClick }: InsightCardProps) {
  const amount = pattern.data.total_value as number | undefined;
  const chain = pattern.data.entity_chain as
    | { name: string; type: string }[]
    | undefined;
  const confidence = (pattern.data.confidence as number) ?? 1;

  return (
    <button className={styles.card} onClick={onClick} type="button">
      <div className={styles.header}>
        <span className={styles.title}>{pattern.pattern_name}</span>
        {amount != null && amount > 0 && (
          <span className={styles.amount}>{formatMoney(amount)}</span>
        )}
      </div>

      <div className={styles.confidenceTrack}>
        <div
          className={styles.confidenceFill}
          style={{ width: `${String(Math.round(confidence * 100))}%` }}
        />
      </div>

      {chain && chain.length > 0 && (
        <div className={styles.chain}>
          {chain.map((node, i) => (
            <span key={i} className={styles.chainNode}>
              {i > 0 && <span className={styles.arrow}>&rarr;</span>}
              <span
                className={styles.chainDot}
                style={{
                  backgroundColor:
                    entityColors[node.type] ?? "var(--text-muted)",
                }}
              />
              <span className={styles.chainLabel}>{node.name}</span>
            </span>
          ))}
        </div>
      )}

      {pattern.description && (
        <p className={styles.description}>{pattern.description}</p>
      )}

      <div className={styles.sources}>
        {pattern.sources.map((s) => (
          <span key={s.database} className={styles.sourcePill}>
            {s.database}
          </span>
        ))}
      </div>
    </button>
  );
}

export const InsightCard = memo(InsightCardInner);
