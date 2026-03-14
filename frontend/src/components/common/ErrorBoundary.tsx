import { Component, type ErrorInfo, type ReactNode } from "react";
import i18n from "@/i18n";

import styles from "./ErrorBoundary.module.css";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    console.error("ErrorBoundary caught:", error, info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      const t = i18n.t.bind(i18n);
      return (
        <div className={styles.container}>
          <div className={styles.content}>
            <h1 className={styles.title}>{t("error.title")}</h1>
            <p className={styles.message}>{t("error.message")}</p>
            <button
              onClick={() => window.location.reload()}
              className={styles.reloadBtn}
            >
              {t("error.reload")}
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
