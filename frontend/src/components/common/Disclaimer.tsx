import { useTranslation } from "react-i18next";

import styles from "./Disclaimer.module.css";

export function Disclaimer() {
  const { t } = useTranslation();

  return <p className={styles.disclaimer}>{t("app.disclaimer")}</p>;
}
