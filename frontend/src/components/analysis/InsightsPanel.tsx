import { memo, useMemo } from "react";
import { useTranslation } from "react-i18next";

import type {
  BaselineResponse,
  ExposureResponse,
  GraphNode,
  PatternResponse,
} from "@/api/client";
import { entityColors } from "@/styles/tokens";
import { useEntityAnalysisStore } from "@/stores/entityAnalysis";

import { InsightCard } from "./InsightCard";
import { ScoreRing } from "./ScoreRing";
import styles from "./InsightsPanel.module.css";

interface InsightsPanelProps {
  exposure: ExposureResponse | null;
  patterns: PatternResponse | null;
  baseline: BaselineResponse | null;
  nodes: GraphNode[];
  exposureLoading: boolean;
}

function InsightsPanelInner({
  exposure,
  patterns,
  baseline,
  nodes,
  exposureLoading,
}: InsightsPanelProps) {
  const { t } = useTranslation();
  const {
    rightPanelTab,
    setRightPanelTab,
    selectedNodeId,
    setHighlightedNodeIds,
  } = useEntityAnalysisStore();

  const selectedNode = useMemo(
    () => nodes.find((n) => n.id === selectedNodeId) ?? null,
    [nodes, selectedNodeId],
  );

  return (
    <aside className={styles.panel}>
      <div className={styles.tabs}>
        <button
          className={`${styles.tab} ${rightPanelTab === "insights" ? styles.activeTab : ""}`}
          onClick={() => setRightPanelTab("insights")}
        >
          {t("analysis.insights")}
        </button>
        <button
          className={`${styles.tab} ${rightPanelTab === "detail" ? styles.activeTab : ""}`}
          onClick={() => setRightPanelTab("detail")}
        >
          {t("analysis.detail")}
        </button>
      </div>

      <div className={styles.content}>
        {rightPanelTab === "insights" ? (
          <InsightsContent
            exposure={exposure}
            patterns={patterns}
            baseline={baseline}
            exposureLoading={exposureLoading}
            onPatternClick={(entityIds) =>
              setHighlightedNodeIds(new Set(entityIds))
            }
          />
        ) : (
          <DetailContent node={selectedNode} />
        )}
      </div>
    </aside>
  );
}

function InsightsContent({
  exposure,
  patterns,
  baseline,
  exposureLoading,
  onPatternClick,
}: {
  exposure: ExposureResponse | null;
  patterns: PatternResponse | null;
  baseline: BaselineResponse | null;
  exposureLoading: boolean;
  onPatternClick: (entityIds: string[]) => void;
}) {
  const { t } = useTranslation();

  return (
    <div className={styles.insightsScroll}>
      {/* Exposure Summary */}
      <section className={styles.section}>
        <h3 className={styles.sectionTitle}>{t("analysis.exposureIndex")}</h3>
        {exposureLoading ? (
          <div className={styles.skeleton} />
        ) : exposure ? (
          <div className={styles.exposureRow}>
            <ScoreRing value={exposure.exposure_index} size={64} />
            <div className={styles.factors}>
              {exposure.factors.map((f) => (
                <div key={f.name} className={styles.factor}>
                  <span className={styles.factorLabel}>{t(`analysis.factor.${f.name}`, f.name)}</span>
                  <div className={styles.factorTrack}>
                    <div
                      className={styles.factorFill}
                      style={{ width: `${String(Math.round(f.percentile))}%` }}
                    />
                  </div>
                  <span className={styles.factorPct}>
                    p{Math.round(f.percentile)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <p className={styles.muted}>{t("analysis.noExposure")}</p>
        )}
      </section>

      {/* Patterns */}
      <section className={styles.section}>
        <h3 className={styles.sectionTitle}>{t("analysis.patterns")}</h3>
        {patterns && patterns.patterns.length > 0 ? (
          <div className={styles.patternList}>
            {patterns.patterns.map((p, i) => (
              <InsightCard
                key={`${p.pattern_id}-${String(i)}`}
                pattern={p}
                onClick={() => onPatternClick(p.entity_ids)}
              />
            ))}
          </div>
        ) : (
          <p className={styles.muted}>{t("patterns.noResults")}</p>
        )}
      </section>

      {/* Baseline */}
      {baseline && baseline.comparisons.length > 0 && (
        <section className={styles.section}>
          <h3 className={styles.sectionTitle}>{t("analysis.baselineComparison")}</h3>
          <div className={styles.baselineTable}>
            {baseline.comparisons.map((c, i) => (
              <div key={i} className={styles.baselineRow}>
                <span className={styles.baselineLabel}>
                  {c.comparison_dimension}: {c.comparison_key}
                </span>
                <span className={styles.baselineValue}>
                  {Math.round(c.contract_ratio * 100)}%
                </span>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

function DetailContent({ node }: { node: GraphNode | null }) {
  const { t } = useTranslation();

  if (!node) {
    return (
      <div className={styles.emptyDetail}>
        <p className={styles.muted}>{t("analysis.selectNode")}</p>
      </div>
    );
  }

  const typeColor = entityColors[node.type] ?? "var(--text-muted)";
  const entries = Object.entries(node.properties).filter(
    ([, v]) => v != null && v !== "",
  );

  return (
    <div className={styles.detailScroll}>
      <div className={styles.detailHeader}>
        <span
          className={styles.detailDot}
          style={{ backgroundColor: typeColor }}
        />
        <span className={styles.detailType}>
          {t(`entity.${node.type}`, node.type)}
        </span>
      </div>
      <h3 className={styles.detailName}>{node.label}</h3>
      <dl className={styles.propList}>
        {entries.map(([key, val]) => (
          <div key={key} className={styles.propRow}>
            <dt className={styles.propKey}>{key}</dt>
            <dd className={styles.propVal}>{String(val)}</dd>
          </div>
        ))}
      </dl>
      {node.sources.length > 0 && (
        <div className={styles.detailSources}>
          {node.sources.map((s) => (
            <span key={s.database} className={styles.sourcePill}>
              {s.database}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

export const InsightsPanel = memo(InsightsPanelInner);
