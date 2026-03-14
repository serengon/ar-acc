import { useCallback, useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import { useInvestigationStore } from "@/stores/investigation";

import styles from "./AnnotationEditor.module.css";

export function AnnotationEditor() {
  const { t } = useTranslation();
  const {
    investigations,
    activeInvestigationId,
    annotations,
    fetchAnnotations,
    addAnnotation,
    deleteAnnotation,
  } = useInvestigationStore();

  const [text, setText] = useState("");
  const [entityId, setEntityId] = useState("");

  const investigation = useMemo(
    () => investigations.find((i) => i.id === activeInvestigationId),
    [investigations, activeInvestigationId],
  );

  useEffect(() => {
    if (activeInvestigationId) {
      fetchAnnotations(activeInvestigationId);
    }
  }, [activeInvestigationId, fetchAnnotations]);

  // Default entity selection to first entity
  useEffect(() => {
    if (investigation?.entity_ids.length && !entityId) {
      setEntityId(investigation.entity_ids[0] ?? "");
    }
  }, [investigation, entityId]);

  const handleAdd = useCallback(async () => {
    if (!activeInvestigationId || !text.trim() || !entityId) return;
    await addAnnotation(activeInvestigationId, entityId, text.trim());
    setText("");
  }, [activeInvestigationId, entityId, text, addAnnotation]);

  const handleDelete = useCallback(
    async (annotationId: string) => {
      if (!activeInvestigationId) return;
      await deleteAnnotation(activeInvestigationId, annotationId);
    },
    [activeInvestigationId, deleteAnnotation],
  );

  if (!investigation) return null;

  return (
    <div className={styles.editor}>
      <h3 className={styles.sectionTitle}>{t("investigation.annotations")}</h3>

      <div className={styles.inputRow}>
        <select
          className={styles.entitySelect}
          value={entityId}
          onChange={(e) => setEntityId(e.target.value)}
        >
          {investigation.entity_ids.map((eid) => (
            <option key={eid} value={eid}>{eid}</option>
          ))}
        </select>
        <input
          className={styles.textInput}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter") handleAdd(); }}
          placeholder={t("investigation.annotations")}
        />
        <button className={styles.addButton} onClick={handleAdd} type="button">
          +
        </button>
      </div>

      <div className={styles.list}>
        {annotations.length === 0 && (
          <p className={styles.empty}>{t("investigation.noAnnotations")}</p>
        )}
        {annotations.map((a) => (
          <div key={a.id} className={styles.annotation}>
            <div className={styles.annotationHeader}>
              <p className={styles.annotationText}>{a.text}</p>
              <button
                className={styles.deleteButton}
                onClick={() => handleDelete(a.id)}
                type="button"
                aria-label={t("investigation.deleteAnnotation")}
              >
                x
              </button>
            </div>
            <div className={styles.annotationMeta}>
              <span>{a.entity_id}</span>
              <span>{new Date(a.created_at).toLocaleString()}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
