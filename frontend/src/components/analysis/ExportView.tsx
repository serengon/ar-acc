import { memo } from "react";
import { useTranslation } from "react-i18next";
import { FileText, Table, Braces, Camera } from "lucide-react";

import styles from "./ExportView.module.css";

interface ExportViewProps {
  onExportPdf: () => void;
  onExportCsv: () => void;
  onExportJson: () => void;
  onExportScreenshot: () => void;
}

const EXPORT_OPTIONS = [
  { id: "pdf", icon: FileText, titleKey: "analysis.exportPdf", descKey: "analysis.exportPdfDesc" },
  { id: "csv", icon: Table, titleKey: "analysis.exportCsv", descKey: "analysis.exportCsvDesc" },
  { id: "json", icon: Braces, titleKey: "analysis.exportJson", descKey: "analysis.exportJsonDesc" },
  { id: "screenshot", icon: Camera, titleKey: "analysis.exportScreenshot", descKey: "analysis.exportScreenshotDesc" },
] as const;

function ExportViewInner({
  onExportPdf,
  onExportCsv,
  onExportJson,
  onExportScreenshot,
}: ExportViewProps) {
  const { t } = useTranslation();

  const handlers: Record<string, () => void> = {
    pdf: onExportPdf,
    csv: onExportCsv,
    json: onExportJson,
    screenshot: onExportScreenshot,
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2 className={styles.title}>{t("analysis.export")}</h2>
      </div>

      <div className={styles.grid}>
        {EXPORT_OPTIONS.map(({ id, icon: Icon, titleKey, descKey }) => (
          <button
            key={id}
            className={styles.card}
            onClick={handlers[id]}
            type="button"
          >
            <Icon size={24} className={styles.icon} />
            <span className={styles.cardTitle}>{t(titleKey)}</span>
            <span className={styles.cardDesc}>{t(descKey)}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

export const ExportView = memo(ExportViewInner);
