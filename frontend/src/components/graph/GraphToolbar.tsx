import { memo, useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { Maximize, Download, GitBranch, Network } from "lucide-react";

import styles from "./GraphToolbar.module.css";

interface GraphToolbarProps {
  onSearch: (query: string) => void;
  layoutMode: "force" | "hierarchy";
  onLayoutChange: (mode: "force" | "hierarchy") => void;
  onFullscreen: () => void;
  onExportPng: () => void;
}

function GraphToolbarInner({
  onSearch,
  layoutMode,
  onLayoutChange,
  onFullscreen,
  onExportPng,
}: GraphToolbarProps) {
  const { t } = useTranslation();
  const [query, setQuery] = useState("");

  const handleSearchChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value;
      setQuery(value);
      onSearch(value);
    },
    [onSearch],
  );

  const handleForce = useCallback(() => {
    onLayoutChange("force");
  }, [onLayoutChange]);

  const handleHierarchy = useCallback(() => {
    onLayoutChange("hierarchy");
  }, [onLayoutChange]);

  return (
    <div className={styles.toolbar}>
      <input
        type="text"
        className={styles.search}
        placeholder={t("graph.searchInGraph")}
        value={query}
        onChange={handleSearchChange}
      />

      <div className={styles.actions}>
        <button
          className={`${styles.button} ${layoutMode === "force" ? styles.active : ""}`}
          onClick={handleForce}
          title={t("graph.layoutForce")}
        >
          <Network size={16} />
        </button>
        <button
          className={`${styles.button} ${layoutMode === "hierarchy" ? styles.active : ""}`}
          onClick={handleHierarchy}
          title={t("graph.layoutHierarchy")}
        >
          <GitBranch size={16} />
        </button>

        <span className={styles.separator} />

        <button
          className={styles.button}
          onClick={onFullscreen}
          title={t("graph.fullscreen")}
        >
          <Maximize size={16} />
        </button>
        <button
          className={styles.button}
          onClick={onExportPng}
          title={t("graph.exportPng")}
        >
          <Download size={16} />
        </button>
      </div>
    </div>
  );
}

export const GraphToolbar = memo(GraphToolbarInner);
