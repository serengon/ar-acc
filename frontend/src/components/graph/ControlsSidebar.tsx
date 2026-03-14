import { memo, useCallback, useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { ChevronLeft, ChevronRight, Layers, GitFork, SlidersHorizontal } from "lucide-react";

import { dataColors, type DataEntityType, relationshipColors } from "@/styles/tokens";

import styles from "./ControlsSidebar.module.css";

interface ControlsSidebarProps {
  collapsed: boolean;
  onToggle: () => void;
  depth: number;
  onDepthChange: (d: number) => void;
  enabledTypes: Set<string>;
  onToggleType: (t: string) => void;
  enabledRelTypes: Set<string>;
  onToggleRelType: (t: string) => void;
  typeCounts: Record<string, number>;
  relTypeCounts: Record<string, number>;
}

const ENTITY_TYPES = Object.keys(dataColors) as DataEntityType[];
const REL_TYPES = Object.keys(relationshipColors);
const DEPTH_DEBOUNCE_MS = 400;

function ControlsSidebarInner({
  collapsed,
  onToggle,
  depth,
  onDepthChange,
  enabledTypes,
  onToggleType,
  enabledRelTypes,
  onToggleRelType,
  typeCounts,
  relTypeCounts,
}: ControlsSidebarProps) {
  const { t } = useTranslation();

  // Local slider value for immediate UI feedback; debounce actual store update
  const [localDepth, setLocalDepth] = useState(depth);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Sync local state when parent prop changes (e.g. reset)
  useEffect(() => {
    setLocalDepth(depth);
  }, [depth]);

  const handleDepthChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = Number(e.target.value);
      setLocalDepth(value);
      if (debounceRef.current) clearTimeout(debounceRef.current);
      debounceRef.current = setTimeout(() => {
        onDepthChange(value);
      }, DEPTH_DEBOUNCE_MS);
    },
    [onDepthChange],
  );

  // Commit immediately on mouseup/touchend (user released slider)
  const handleDepthCommit = useCallback(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    onDepthChange(localDepth);
  }, [onDepthChange, localDepth]);

  // Cleanup timer on unmount
  useEffect(() => {
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, []);

  const visibleCount = Object.entries(typeCounts).reduce(
    (sum, [type, count]) => (enabledTypes.has(type) ? sum + count : sum),
    0,
  );
  const totalCount = Object.values(typeCounts).reduce((a, b) => a + b, 0);

  return (
    <div className={`${styles.sidebar} ${collapsed ? styles.collapsed : ""}`}>
      <button className={styles.toggle} onClick={onToggle}>
        {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
      </button>

      {collapsed ? (
        <div className={styles.icons}>
          <span title={t("graph.depth")}><SlidersHorizontal size={16} className={styles.sidebarIcon} /></span>
          <span title={t("graph.entityTypes")}><Layers size={16} className={styles.sidebarIcon} /></span>
          <span title={t("graph.relationshipTypes")}><GitFork size={16} className={styles.sidebarIcon} /></span>
        </div>
      ) : (
        <div className={styles.content}>
          {/* Depth slider */}
          <div className={styles.section}>
            <label className={styles.sectionLabel}>
              {t("graph.depth")}: {localDepth}
            </label>
            <input
              type="range"
              min={1}
              max={4}
              value={localDepth}
              onChange={handleDepthChange}
              onMouseUp={handleDepthCommit}
              onTouchEnd={handleDepthCommit}
              className={styles.slider}
            />
          </div>

          {/* Entity type toggles */}
          <div className={styles.section}>
            <label className={styles.sectionLabel}>
              {t("graph.entityTypes")}
            </label>
            <div className={styles.toggleList}>
              {ENTITY_TYPES.map((type) => {
                const count = typeCounts[type] ?? 0;
                const enabled = enabledTypes.has(type);
                return (
                  <button
                    key={type}
                    className={`${styles.toggleItem} ${enabled ? styles.enabled : ""}`}
                    onClick={() => onToggleType(type)}
                  >
                    <span
                      className={styles.dot}
                      style={{
                        backgroundColor: enabled
                          ? dataColors[type]
                          : "var(--text-muted)",
                      }}
                    />
                    <span className={styles.toggleLabel}>
                      {t(`entity.${type}`, type)}
                    </span>
                    <span className={styles.count}>{count}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Relationship type toggles */}
          <div className={styles.section}>
            <label className={styles.sectionLabel}>
              {t("graph.relationshipTypes")}
            </label>
            <div className={styles.toggleList}>
              {REL_TYPES.map((type) => {
                const count = relTypeCounts[type] ?? 0;
                const enabled = enabledRelTypes.has(type);
                return (
                  <button
                    key={type}
                    className={`${styles.toggleItem} ${enabled ? styles.enabled : ""}`}
                    onClick={() => onToggleRelType(type)}
                  >
                    <span
                      className={styles.dot}
                      style={{
                        backgroundColor: enabled
                          ? (relationshipColors[type] ?? "var(--text-muted)")
                          : "var(--text-muted)",
                      }}
                    />
                    <span className={styles.toggleLabel}>{type}</span>
                    <span className={styles.count}>{count}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Filter summary */}
          <div className={styles.summary}>
            {t("graph.filterSummary", {
              visible: visibleCount,
              total: totalCount,
            })}
          </div>
        </div>
      )}
    </div>
  );
}

export const ControlsSidebar = memo(ControlsSidebarInner);
