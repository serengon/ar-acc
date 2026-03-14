import { memo } from "react";
import { useTranslation } from "react-i18next";
import { Network, Users, Clock, Download } from "lucide-react";

import styles from "./AnalysisNav.module.css";

type AnalysisTab = "graph" | "connections" | "timeline" | "export";

interface AnalysisNavProps {
  activeTab: AnalysisTab;
  onTabChange: (tab: AnalysisTab) => void;
}

const TABS: { id: AnalysisTab; icon: typeof Network; labelKey: string }[] = [
  { id: "graph", icon: Network, labelKey: "analysis.graph" },
  { id: "connections", icon: Users, labelKey: "analysis.connections" },
  { id: "timeline", icon: Clock, labelKey: "analysis.timeline" },
  { id: "export", icon: Download, labelKey: "analysis.export" },
];

function AnalysisNavInner({ activeTab, onTabChange }: AnalysisNavProps) {
  const { t } = useTranslation();

  return (
    <nav className={styles.nav} aria-label={t("analysis.navigation")}>
      {TABS.map(({ id, icon: Icon, labelKey }) => (
        <button
          key={id}
          className={`${styles.btn} ${activeTab === id ? styles.active : ""}`}
          onClick={() => onTabChange(id)}
          title={t(labelKey)}
          aria-label={t(labelKey)}
          aria-current={activeTab === id ? "page" : undefined}
        >
          <Icon size={18} />
        </button>
      ))}
    </nav>
  );
}

export const AnalysisNav = memo(AnalysisNavInner);
