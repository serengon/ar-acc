import { memo } from "react";
import { useTranslation } from "react-i18next";

import { dataColors, type DataEntityType } from "@/styles/tokens";

import styles from "./NodeTooltip.module.css";

interface TooltipNode {
  id: string;
  label: string;
  type: string;
  connectionCount: number;
  document_id?: string;
}

interface NodeTooltipProps {
  node: TooltipNode | null;
  x: number;
  y: number;
}

function NodeTooltipInner({ node, x, y }: NodeTooltipProps) {
  const { t } = useTranslation();

  if (!node) return null;

  const color =
    dataColors[node.type as DataEntityType] ?? "#5a6b60";

  return (
    <div
      className={styles.tooltip}
      style={{ left: x, top: y }}
    >
      <div className={styles.header}>
        <span className={styles.dot} style={{ backgroundColor: color }} />
        <span className={styles.type}>
          {t(`entity.${node.type}`, node.type)}
        </span>
      </div>
      <span className={styles.name}>{node.label}</span>
      {node.document_id && (
        <span className={styles.document}>{node.document_id}</span>
      )}
      <span className={styles.connections}>
        {node.connectionCount} {t("common.connections")}
      </span>
    </div>
  );
}

export const NodeTooltip = memo(NodeTooltipInner);
