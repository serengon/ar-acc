import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate, useParams } from "react-router";

import type { PatternInfo, PatternResult } from "@/api/client";
import { getEntityPatterns, listPatterns } from "@/api/client";
import { Spinner } from "@/components/common/Spinner";
import { PatternCard } from "@/components/pattern/PatternCard";
import { PatternResultCard } from "@/components/pattern/PatternResultCard";

import styles from "./Patterns.module.css";

export function Patterns() {
  const { t, i18n } = useTranslation();
  const { entityId } = useParams<{ entityId: string }>();
  const navigate = useNavigate();

  const [patterns, setPatterns] = useState<PatternInfo[]>([]);
  const [activePattern, setActivePattern] = useState<string | null>(null);
  const [results, setResults] = useState<PatternResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listPatterns()
      .then((res) => setPatterns(res.patterns))
      .catch(() => setError(t("patterns.loadError")));
  }, [t]);

  useEffect(() => {
    if (!entityId) {
      setResults([]);
      return;
    }
    setLoading(true);
    setError(null);
    const lang = i18n.language === "pt-BR" ? "pt" : "en";
    getEntityPatterns(entityId, lang)
      .then((res) => setResults(res.patterns))
      .catch(() => setError(t("patterns.runError")))
      .finally(() => setLoading(false));
  }, [entityId, i18n.language, t]);

  const handlePatternClick = useCallback((patternId: string) => {
    setActivePattern((prev) => (prev === patternId ? null : patternId));
  }, []);

  const handleEntityClick = useCallback(
    (id: string) => {
      navigate(`/app/analysis/${encodeURIComponent(id)}`);
    },
    [navigate],
  );

  const filteredResults = activePattern
    ? results.filter((r) => r.pattern_id === activePattern)
    : results;

  return (
    <div className={styles.page}>
      <div className={styles.sidebar}>
        <h2 className={styles.title}>{t("patterns.title")}</h2>
        <div className={styles.list}>
          {patterns.map((p) => (
            <PatternCard
              key={p.id}
              pattern={p}
              active={activePattern === p.id}
              onClick={handlePatternClick}
            />
          ))}
        </div>
      </div>

      <div className={styles.content}>
        {!entityId && (
          <p className={styles.hint}>{t("patterns.selectEntity")}</p>
        )}
        {loading && <Spinner />}
        {error && <p className={styles.error}>{error}</p>}
        {!loading && entityId && filteredResults.length === 0 && !error && (
          <p className={styles.status}>{t("patterns.noResults")}</p>
        )}
        <div className={styles.results}>
          {filteredResults.map((r, i) => (
            <PatternResultCard
              key={`${r.pattern_id}-${i}`}
              result={r}
              onEntityClick={handleEntityClick}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
