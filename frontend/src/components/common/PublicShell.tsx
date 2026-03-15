import { useTranslation } from "react-i18next";
import { Link, Outlet } from "react-router";

import { IS_PUBLIC_MODE } from "@/config/runtime";
import { useAuthStore } from "@/stores/auth";

import styles from "./PublicShell.module.css";

export function PublicShell() {
  const { t } = useTranslation();
  const token = useAuthStore((s) => s.token);


  return (
    <div className={styles.shell}>
      <header className={styles.header}>
        <Link to="/" className={styles.logo}>
          {t("app.title")}
        </Link>
        <div className={styles.actions}>
          {IS_PUBLIC_MODE ? (
            <Link to="/app/search" className={styles.registerLink}>
              {t("landing.cta")}
            </Link>
          ) : !token && (
            <>
              <Link to="/login" className={styles.authLink}>
                {t("nav.login")}
              </Link>
              <Link to="/register" className={styles.registerLink}>
                {t("nav.register")}
              </Link>
            </>
          )}
        </div>
      </header>
      <main className={styles.content}>
        <Outlet />
      </main>
    </div>
  );
}
