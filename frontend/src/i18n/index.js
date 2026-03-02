import { createI18n } from "vue-i18n";

import en from "./en.json";
import es from "./es.json";
import ca from "./ca.json";
import ar from "./ar.json";
import de from "./de.json";
import fr from "./fr.json";
import ur from "./ur.json";
import hi from "./hi.json";

const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem("locale") || "en",
  fallbackLocale: "en",
  messages: { en, es, ca, ar, de, fr, ur, hi },
});

export default i18n;
