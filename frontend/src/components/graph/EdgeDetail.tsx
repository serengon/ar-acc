import { useTranslation } from "react-i18next";

import { MoneyLabel } from "@/components/common/MoneyLabel";

import styles from "./EdgeDetail.module.css";

interface EdgeDetailProps {
  edge: {
    type: string;
    source?: string | number | { id?: string | number; [k: string]: unknown };
    target?: string | number | { id?: string | number; [k: string]: unknown };
    value?: number;
    confidence?: number;
    properties: Record<string, unknown>;
  };
  onClose: () => void;
}

function resolveId(ref: string | number | { id?: string | number; [k: string]: unknown } | undefined): string {
  if (ref == null) return "";
  if (typeof ref === "string") return ref;
  if (typeof ref === "number") return String(ref);
  return String(ref.id ?? "");
}

export function EdgeDetail({ edge, onClose }: EdgeDetailProps) {
  const { t } = useTranslation();

  const sourceId = resolveId(edge.source);
  const targetId = resolveId(edge.target);
  const databases = edge.properties.database
    ? [String(edge.properties.database)]
    : edge.properties.databases
      ? (edge.properties.databases as string[])
      : [];

  return (
    <div className={styles.panel}>
      <button className={styles.close} onClick={onClose} aria-label="Close">
        &times;
      </button>

      <h3 className={styles.type}>{edge.type}</h3>

      <dl className={styles.fields}>
        <dt>{t("graph.edge.source")}</dt>
        <dd className={styles.mono}>{sourceId}</dd>

        <dt>{t("graph.edge.target")}</dt>
        <dd className={styles.mono}>{targetId}</dd>

        <dt>{t("graph.edge.value")}</dt>
        <dd>
          {edge.value != null && edge.value > 0 ? (
            <MoneyLabel value={edge.value} />
          ) : (
            <span className={styles.muted}>{t("graph.edge.noValue")}</span>
          )}
        </dd>

        <dt>{t("graph.edge.confidence")}</dt>
        <dd>{Math.round((edge.confidence ?? 1) * 100)}%</dd>

        {databases.length > 0 && (
          <>
            <dt>{t("graph.edge.sources")}</dt>
            <dd>{databases.join(", ")}</dd>
          </>
        )}
      </dl>
    </div>
  );
}
