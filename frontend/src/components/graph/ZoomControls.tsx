import { memo } from "react";
import { useTranslation } from "react-i18next";
import { Plus, Minus, Maximize2, RotateCcw } from "lucide-react";

import styles from "./ZoomControls.module.css";

interface ZoomControlsProps {
  onZoomIn: () => void;
  onZoomOut: () => void;
  onFitView: () => void;
  onResetZoom: () => void;
}

function ZoomControlsInner({
  onZoomIn,
  onZoomOut,
  onFitView,
  onResetZoom,
}: ZoomControlsProps) {
  const { t } = useTranslation();

  return (
    <div className={styles.controls}>
      <button
        className={styles.button}
        onClick={onZoomIn}
        title={t("graph.zoomIn")}
      >
        <Plus size={16} />
      </button>
      <button
        className={styles.button}
        onClick={onZoomOut}
        title={t("graph.zoomOut")}
      >
        <Minus size={16} />
      </button>
      <button
        className={styles.button}
        onClick={onFitView}
        title={t("graph.fitView")}
      >
        <Maximize2 size={16} />
      </button>
      <button
        className={styles.button}
        onClick={onResetZoom}
        title={t("graph.resetZoom")}
      >
        <RotateCcw size={16} />
      </button>
    </div>
  );
}

export const ZoomControls = memo(ZoomControlsInner);
