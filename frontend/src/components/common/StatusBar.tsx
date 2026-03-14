import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { getHealthStatus } from "@/api/client";

import styles from "./StatusBar.module.css";

interface StatusBarProps {
  nodeCount?: number;
  edgeCount?: number;
}

export function StatusBar({ nodeCount, edgeCount }: StatusBarProps) {
  const { t } = useTranslation();

  const [isConnected, setIsConnected] = useState(true);

  useEffect(() => {
    let cancelled = false;

    function poll() {
      getHealthStatus()
        .then(() => { if (!cancelled) setIsConnected(true); })
        .catch(() => { if (!cancelled) setIsConnected(false); });
    }

    poll();
    const interval = setInterval(poll, 30_000);
    return () => { cancelled = true; clearInterval(interval); };
  }, []);

  return (
    <div className={styles.statusBar}>
      <div className={styles.left}>
        <span
          className={`${styles.dot} ${isConnected ? styles.connected : styles.disconnected}`}
        />
        <span>
          {isConnected
            ? t("statusBar.connected")
            : t("statusBar.disconnected")}
        </span>
      </div>
      <div className={styles.center}>
        {nodeCount != null && (
          <span className={styles.stat}>
            {nodeCount.toLocaleString()} {t("statusBar.nodes")}
          </span>
        )}
        {edgeCount != null && (
          <span className={styles.stat}>
            {edgeCount.toLocaleString()} {t("statusBar.edges")}
          </span>
        )}
      </div>
      <div className={styles.right}>
        <span>
          {t("statusBar.lastRefresh")}{" "}
          {new Date().toLocaleTimeString()}
        </span>
      </div>
    </div>
  );
}
