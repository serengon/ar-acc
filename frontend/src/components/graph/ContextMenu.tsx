import { memo, useEffect, useRef, type ReactNode } from "react";

import styles from "./ContextMenu.module.css";

interface ContextMenuAction {
  id: string;
  label: string;
  icon?: ReactNode;
  handler: () => void;
}

interface ContextMenuProps {
  x: number;
  y: number;
  nodeId: string;
  onClose: () => void;
  actions: ContextMenuAction[];
}

function ContextMenuInner({ x, y, onClose, actions }: ContextMenuProps) {
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        onClose();
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [onClose]);

  return (
    <div
      ref={menuRef}
      className={styles.menu}
      style={{ left: x, top: y }}
    >
      {actions.map((action) => (
        <button
          key={action.id}
          className={styles.item}
          onClick={() => {
            action.handler();
            onClose();
          }}
        >
          {action.icon && <span className={styles.icon}>{action.icon}</span>}
          <span className={styles.label}>{action.label}</span>
        </button>
      ))}
    </div>
  );
}

export const ContextMenu = memo(ContextMenuInner);
