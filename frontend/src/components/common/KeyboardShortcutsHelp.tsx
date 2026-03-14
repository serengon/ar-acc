import { useTranslation } from "react-i18next";

import { getActions } from "@/actions/registry";
import { Kbd } from "@/components/common/Kbd";

import styles from "./KeyboardShortcutsHelp.module.css";

interface KeyboardShortcutsHelpProps {
  open: boolean;
  onClose: () => void;
}

function formatShortcutParts(shortcut: string): string[] {
  return shortcut.split("+").map((part) => {
    const p = part.trim();
    switch (p.toLowerCase()) {
      case "cmd":
      case "meta":
        return "\u2318";
      case "ctrl":
        return "Ctrl";
      case "shift":
        return "\u21E7";
      case "alt":
        return "\u2325";
      default:
        return p.toUpperCase();
    }
  });
}

export function KeyboardShortcutsHelp({
  open,
  onClose,
}: KeyboardShortcutsHelpProps) {
  const { t } = useTranslation();

  if (!open) return null;

  const actions = getActions().filter((a) => a.shortcut);

  const groups = new Map<string, typeof actions>();
  for (const action of actions) {
    const existing = groups.get(action.group);
    if (existing) {
      existing.push(action);
    } else {
      groups.set(action.group, [action]);
    }
  }

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.card} onClick={(e) => e.stopPropagation()}>
        <div className={styles.header}>
          <h2 className={styles.title}>{t("shortcuts.title")}</h2>
          <button
            className={styles.closeButton}
            onClick={onClose}
            aria-label={t("common.close")}
          >
            &times;
          </button>
        </div>
        <div className={styles.content}>
          {Array.from(groups.entries()).map(([group, groupActions]) => (
            <div key={group} className={styles.group}>
              <h3 className={styles.groupTitle}>{group}</h3>
              {groupActions.map((action) => (
                <div key={action.id} className={styles.row}>
                  <span className={styles.label}>{action.label}</span>
                  <span className={styles.keys}>
                    {action.shortcut &&
                      formatShortcutParts(action.shortcut).map((part, i) => (
                        <Kbd key={i}>{part}</Kbd>
                      ))}
                  </span>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
