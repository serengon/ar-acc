import { useMemo } from "react";
import { useTranslation } from "react-i18next";

import { useInvestigationStore } from "@/stores/investigation";

import styles from "./Timeline.module.css";

interface TimelineEntry {
  id: string;
  type: "annotation" | "entity";
  text: string;
  date: string;
}

export function Timeline() {
  const { t } = useTranslation();
  const { investigations, activeInvestigationId, annotations } =
    useInvestigationStore();

  const investigation = useMemo(
    () => investigations.find((i) => i.id === activeInvestigationId),
    [investigations, activeInvestigationId],
  );

  const entries = useMemo<TimelineEntry[]>(() => {
    if (!investigation) return [];

    const items: TimelineEntry[] = [];

    // Add annotations as timeline entries
    for (const a of annotations) {
      items.push({
        id: `annotation-${a.id}`,
        type: "annotation",
        text: `[${a.entity_id}] ${a.text}`,
        date: a.created_at,
      });
    }

    // Investigation creation as an entry
    items.push({
      id: `created-${investigation.id}`,
      type: "entity",
      text: investigation.title,
      date: investigation.created_at,
    });

    // Sort by date descending (newest first)
    items.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

    return items;
  }, [investigation, annotations]);

  if (!investigation) return null;

  return (
    <div className={styles.timeline}>
      <h3 className={styles.sectionTitle}>{t("investigation.timeline")}</h3>

      {entries.length === 0 && (
        <p className={styles.empty}>{t("investigation.noAnnotations")}</p>
      )}

      <div className={styles.list}>
        {entries.map((entry) => (
          <div
            key={entry.id}
            className={`${styles.entry} ${entry.type === "annotation" ? styles.entryAnnotation : styles.entryEntity}`}
          >
            <span className={styles.entryText}>{entry.text}</span>
            <span className={styles.entryDate}>
              {new Date(entry.date).toLocaleString()}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
