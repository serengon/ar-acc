import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import es from "./locales/es.json";

const resources = {
  es: { translation: es },
};

i18n.use(initReactI18next).init({
  resources,
  lng: "es",
  fallbackLng: "es",
  interpolation: { escapeValue: false },
});

export default i18n;
