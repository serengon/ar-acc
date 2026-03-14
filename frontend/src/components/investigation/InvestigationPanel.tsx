import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { useInvestigationStore } from "@/stores/investigation";

import styles from "./InvestigationPanel.module.css";

export function InvestigationPanel() {
  const { t } = useTranslation();
  const {
    investigations,
    activeInvestigationId,
    loading,
    fetchInvestigations,
    createInvestigation,
    setActiveInvestigation,
  } = useInvestigationStore();

  const [creating, setCreating] = useState(false);
  const [newTitle, setNewTitle] = useState("");

  useEffect(() => {
    fetchInvestigations();
  }, [fetchInvestigations]);

  const handleCreate = useCallback(async () => {
    if (!newTitle.trim()) return;
    const inv = await createInvestigation(newTitle.trim());
    setActiveInvestigation(inv.id);
    setNewTitle("");
    setCreating(false);
  }, [newTitle, createInvestigation, setActiveInvestigation]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === "Enter") handleCreate();
      if (e.key === "Escape") setCreating(false);
    },
    [handleCreate],
  );

  return (
    <div className={styles.panel}>
      <div className={styles.header}>
        <h2 className={styles.title}>{t("investigation.title")}</h2>
        <button
          className={styles.newButton}
          onClick={() => setCreating(true)}
          type="button"
        >
          + {t("investigation.newInvestigation")}
        </button>
      </div>

      {creating && (
        <input
          type="text"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={() => { if (!newTitle.trim()) setCreating(false); }}
          placeholder={t("investigation.newInvestigation")}
          autoFocus
          className={styles.item}
        />
      )}

      {loading && <p className={styles.empty}>{t("common.loading")}</p>}

      <div className={styles.list}>
        {!loading && investigations.length === 0 && (
          <p className={styles.empty}>{t("investigation.noInvestigations")}</p>
        )}
        {investigations.map((inv) => (
          <button
            key={inv.id}
            className={`${styles.item} ${activeInvestigationId === inv.id ? styles.active : ""}`}
            onClick={() => setActiveInvestigation(inv.id)}
            type="button"
          >
            <span className={styles.itemTitle}>{inv.title}</span>
            <div className={styles.itemMeta}>
              <span>{inv.entity_ids.length} {t("common.connections")}</span>
              <span>{new Date(inv.created_at).toLocaleDateString()}</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
