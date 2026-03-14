import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { useInvestigationStore } from "@/stores/investigation";

import styles from "./TagManager.module.css";

const PRESET_COLORS = [
  "#e07a2f", // accent orange
  "#38a169", // green
  "#3b82f6", // blue
  "#dc2626", // red
  "#a855f7", // purple
  "#ca8a04", // yellow
  "#ec4899", // pink
  "#0d9488", // teal
];

export function TagManager() {
  const { t } = useTranslation();
  const { activeInvestigationId, tags, fetchTags, addTag, deleteTag } =
    useInvestigationStore();

  const [name, setName] = useState("");
  const [color, setColor] = useState(PRESET_COLORS[0]!);

  useEffect(() => {
    if (activeInvestigationId) {
      fetchTags(activeInvestigationId);
    }
  }, [activeInvestigationId, fetchTags]);

  const handleAdd = useCallback(async () => {
    if (!activeInvestigationId || !name.trim()) return;
    await addTag(activeInvestigationId, name.trim(), color);
    setName("");
  }, [activeInvestigationId, name, color, addTag]);

  const handleDelete = useCallback(
    async (tagId: string) => {
      if (!activeInvestigationId) return;
      await deleteTag(activeInvestigationId, tagId);
    },
    [activeInvestigationId, deleteTag],
  );

  if (!activeInvestigationId) return null;

  return (
    <div className={styles.manager}>
      <h3 className={styles.sectionTitle}>{t("investigation.tags")}</h3>

      <div className={styles.inputRow}>
        <input
          className={styles.nameInput}
          value={name}
          onChange={(e) => setName(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter") handleAdd(); }}
          placeholder={t("investigation.tags")}
        />
        <div className={styles.colorPicker}>
          {PRESET_COLORS.map((c) => (
            <button
              key={c}
              className={`${styles.colorDot} ${color === c ? styles.colorDotActive : ""}`}
              style={{ backgroundColor: c }}
              onClick={() => setColor(c)}
              type="button"
              aria-label={c}
            />
          ))}
        </div>
        <button className={styles.addButton} onClick={handleAdd} type="button">
          +
        </button>
      </div>

      <div className={styles.tags}>
        {tags.length === 0 && (
          <p className={styles.empty}>{t("investigation.noTags")}</p>
        )}
        {tags.map((tag) => (
          <span key={tag.id} className={styles.tag}>
            <span className={styles.tagDot} style={{ backgroundColor: tag.color }} />
            {tag.name}
            <button
              className={styles.deleteButton}
              onClick={() => handleDelete(tag.id)}
              type="button"
              aria-label={t("investigation.deleteTag")}
            >
              x
            </button>
          </span>
        ))}
      </div>
    </div>
  );
}
