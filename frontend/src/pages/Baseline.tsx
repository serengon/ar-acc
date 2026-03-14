import { useMemo } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router";

import { type BaselineMetrics } from "@/api/client";
import { MoneyLabel } from "@/components/common/MoneyLabel";
import { Spinner } from "@/components/common/Spinner";
import { useBaseline } from "@/hooks/useBaseline";

import styles from "./Baseline.module.css";

export function Baseline() {
  const { t } = useTranslation();
  const { entityId } = useParams<{ entityId: string }>();
  const { data, loading, error } = useBaseline(entityId);

  const grouped = useMemo(() => {
    if (!data) return new Map<string, BaselineMetrics[]>();
    const map = new Map<string, BaselineMetrics[]>();
    for (const c of data.comparisons) {
      const key = c.comparison_dimension;
      const list = map.get(key) ?? [];
      list.push(c);
      map.set(key, list);
    }
    return map;
  }, [data]);

  if (!entityId) {
    return (
      <div className={styles.page}>
        <h2 className={styles.title}>{t("baseline.title")}</h2>
        <p className={styles.hint}>{t("baseline.noData")}</p>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <h2 className={styles.title}>{t("baseline.title")}</h2>

      {loading && (
        <div className={styles.loading}>
          <Spinner />
        </div>
      )}

      {error && <p className={styles.error}>{error}</p>}

      {!loading && !error && data && data.comparisons.length === 0 && (
        <p className={styles.hint}>{t("baseline.noData")}</p>
      )}

      {[...grouped.entries()].map(([dimension, comparisons]) => (
        <div key={dimension} className={styles.section}>
          <h3 className={styles.sectionHeader}>
            {dimension === "sector"
              ? t("baseline.sector")
              : t("baseline.region")}
            {": "}
            {comparisons[0]?.comparison_key}
          </h3>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>{t("baseline.company")}</th>
                <th>{t("baseline.contracts")}</th>
                <th>{t("baseline.totalValue")}</th>
                <th>{t("baseline.peerAvgContracts")}</th>
                <th>{t("baseline.peerAvgValue")}</th>
                <th>{t("baseline.comparison")}</th>
              </tr>
            </thead>
            <tbody>
              {comparisons.map((c) => (
                <tr key={c.company_id}>
                  <td>{c.company_name}</td>
                  <td>{c.contract_count}</td>
                  <td>
                    <MoneyLabel value={c.total_value} />
                  </td>
                  <td>{c.peer_avg_contracts.toFixed(1)}</td>
                  <td>
                    <MoneyLabel value={c.peer_avg_value} />
                  </td>
                  <td>
                    <span className={styles.ratio}>
                      {t("baseline.ratio", {
                        value: (c.contract_ratio * 100).toFixed(0),
                        dimension:
                          dimension === "sector"
                            ? t("baseline.sector").toLowerCase()
                            : t("baseline.region").toLowerCase(),
                      })}
                    </span>
                    <br />
                    <span className={styles.peers}>
                      {t("baseline.peers", { count: c.peer_count })}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
}
