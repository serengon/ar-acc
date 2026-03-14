import { useToastStore } from "@/stores/toast";

import styles from "./ToastContainer.module.css";

export function ToastContainer() {
  const toasts = useToastStore((s) => s.toasts);
  const removeToast = useToastStore((s) => s.removeToast);

  if (toasts.length === 0) return null;

  return (
    <div className={styles.container} role="region" aria-label="Notifications">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`${styles.toast} ${styles[toast.type]}`}
          role="alert"
        >
          <span className={styles.message}>{toast.message}</span>
          <button
            className={styles.close}
            onClick={() => removeToast(toast.id)}
            aria-label="Close"
          >
            &times;
          </button>
        </div>
      ))}
    </div>
  );
}
