import { memo } from "react";
import { useTranslation } from "react-i18next";

import { type EntityType, entityColors } from "@/styles/tokens";

import styles from "./GraphControls.module.css";

interface GraphControlsProps {
  depth: number;
  onDepthChange: (depth: number) => void;
  enabledTypes: Set<string>;
  onToggleType: (type: string) => void;
}

const ENTITY_TYPES = Object.keys(entityColors) as EntityType[];

function GraphControlsInner({
  depth,
  onDepthChange,
  enabledTypes,
  onToggleType,
}: GraphControlsProps) {
  const { t } = useTranslation();

  return (
    <div className={styles.controls}>
      <div className={styles.section}>
        <label className={styles.label}>
          {t("graph.depth")}: {depth}
        </label>
        <input
          type="range"
          min={1}
          max={4}
          value={depth}
          onChange={(e) => onDepthChange(Number(e.target.value))}
          className={styles.slider}
        />
      </div>

      <div className={styles.section}>
        <label className={styles.label}>{t("graph.entityTypes")}</label>
        <div className={styles.toggles}>
          {ENTITY_TYPES.map((type) => (
            <button
              key={type}
              onClick={() => onToggleType(type)}
              className={`${styles.toggle} ${enabledTypes.has(type) ? styles.active : ""}`}
              style={{
                borderColor: enabledTypes.has(type) ? entityColors[type] : undefined,
                color: enabledTypes.has(type) ? entityColors[type] : undefined,
              }}
            >
              {t(`entity.${type}`, type)}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export const GraphControls = memo(GraphControlsInner);
