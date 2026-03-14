import { useTranslation } from "react-i18next";
import { Link } from "react-router";

import type { SearchResult } from "@/api/client";
import { SourceBadge } from "@/components/common/SourceBadge";
import { entityColors, type EntityType } from "@/styles/tokens";

import styles from "./SearchResults.module.css";

interface SearchResultsProps {
  results: SearchResult[];
}

export function SearchResults({ results }: SearchResultsProps) {
  const { t } = useTranslation();

  if (results.length === 0) {
    return (
      <div>
        <p className={styles.noResults}>{t("search.noResults")}</p>
        <p className={styles.emptyHint}>{t("search.emptyHint")}</p>
      </div>
    );
  }

  return (
    <ul className={styles.list}>
      {results.map((result) => {
        const color = entityColors[result.type as EntityType] ?? "var(--text-secondary)";
        return (
          <li key={result.id} className={styles.item}>
            <Link to={`/app/analysis/${result.id}`} className={styles.link}>
              <span className={styles.typeBadge} style={{ borderColor: color, color }}>
                {t(`entity.${result.type}`, result.type)}
              </span>
              <span className={styles.name}>{result.name}</span>
              {result.document && (
                <span className={styles.document}>{result.document}</span>
              )}
            </Link>
            <div className={styles.sources}>
              {result.sources.map((source) => (
                <SourceBadge key={source.database} source={source.database} />
              ))}
            </div>
          </li>
        );
      })}
    </ul>
  );
}
