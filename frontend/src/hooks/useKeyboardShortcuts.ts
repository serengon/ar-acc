import { useEffect } from "react";

import { getActions } from "@/actions/registry";

function matchShortcut(e: KeyboardEvent, shortcut: string): boolean {
  const parts = shortcut.toLowerCase().split("+");
  const needsMeta = parts.includes("cmd") || parts.includes("meta");
  const needsCtrl = parts.includes("ctrl");
  const needsShift = parts.includes("shift");
  const needsAlt = parts.includes("alt");
  const key = parts.filter(
    (p) => !["cmd", "meta", "ctrl", "shift", "alt"].includes(p),
  )[0];

  if (needsMeta && !e.metaKey) return false;
  if (needsCtrl && !e.ctrlKey) return false;
  if (needsShift && !e.shiftKey) return false;
  if (needsAlt && !e.altKey) return false;
  if (!key) return false;
  if (e.key.toLowerCase() !== key) return false;
  return true;
}

export function useKeyboardShortcuts(): void {
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      const tag = (e.target as HTMLElement).tagName;
      const isInput = tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT";
      const hasModifier = e.metaKey || e.ctrlKey;

      // In input fields, only allow shortcuts with modifier keys (e.g. Cmd+K)
      if (isInput && !hasModifier) return;

      const actions = getActions();
      for (const action of actions) {
        if (!action.shortcut) continue;
        if (matchShortcut(e, action.shortcut)) {
          e.preventDefault();
          action.handler();
          return;
        }
      }
    }

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);
}
