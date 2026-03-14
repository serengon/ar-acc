import { memo } from "react";
import { useTranslation } from "react-i18next";

import { dataColors, type DataEntityType } from "@/styles/tokens";

import styles from "./GraphLegend.module.css";

interface GraphLegendProps {
  visible: boolean;
}

const ENTITY_TYPES = Object.keys(dataColors) as DataEntityType[];

function GraphLegendInner({ visible }: GraphLegendProps) {
  const { t } = useTranslation();

  if (!visible) return null;

  return (
    <div className={styles.legend}>
      <span className={styles.title}>{t("graph.legend.title")}</span>
      <ul className={styles.list}>
        {ENTITY_TYPES.map((type) => (
          <li key={type} className={styles.item}>
            <span
              className={styles.dot}
              style={{ backgroundColor: dataColors[type] }}
            />
            <span className={styles.label}>
              {t(`entity.${type}`, type)}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export const GraphLegend = memo(GraphLegendInner);
