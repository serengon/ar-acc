import { Command } from "cmdk";
import { useTranslation } from "react-i18next";

import { getActions } from "@/actions/registry";
import { Kbd } from "@/components/common/Kbd";

import styles from "./CommandPalette.module.css";

interface CommandPaletteProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
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

export function CommandPalette({ open, onOpenChange }: CommandPaletteProps) {
  const { t } = useTranslation();
  const actions = getActions();

  if (!open) return null;

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
    <div className={styles.overlay} onClick={() => onOpenChange(false)}>
      <div className={styles.dialog} onClick={(e) => e.stopPropagation()}>
        <Command label={t("command.placeholder")}>
          <Command.Input
            className={styles.input}
            placeholder={t("command.placeholder")}
          />
          <Command.List className={styles.list}>
            <Command.Empty className={styles.empty}>
              {t("command.noResults")}
            </Command.Empty>
            {Array.from(groups.entries()).map(([group, groupActions]) => (
              <Command.Group key={group} heading={group} className={styles.group}>
                {groupActions.map((action) => (
                  <Command.Item
                    key={action.id}
                    className={styles.item}
                    value={action.label}
                    onSelect={() => {
                      action.handler();
                      onOpenChange(false);
                    }}
                  >
                    {action.icon && (
                      <span className={styles.itemIcon}>{action.icon}</span>
                    )}
                    <span className={styles.itemLabel}>{action.label}</span>
                    {action.shortcut && (
                      <span className={styles.itemShortcut}>
                        {formatShortcutParts(action.shortcut).map(
                          (part, i) => (
                            <Kbd key={i}>{part}</Kbd>
                          ),
                        )}
                      </span>
                    )}
                  </Command.Item>
                ))}
              </Command.Group>
            ))}
          </Command.List>
        </Command>
      </div>
    </div>
  );
}
