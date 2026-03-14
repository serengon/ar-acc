import { useEffect, useRef, useState } from "react";

import { type GraphData, getGraphData } from "@/api/client";

const CACHE_MAX_ENTRIES = 20;
const CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes

interface CacheEntry {
  data: GraphData;
  timestamp: number;
}

/** Simple LRU cache with TTL for graph data. */
class LruCache {
  private entries = new Map<string, CacheEntry>();

  get(key: string): GraphData | null {
    const entry = this.entries.get(key);
    if (!entry) return null;

    // Evict expired entries
    if (Date.now() - entry.timestamp > CACHE_TTL_MS) {
      this.entries.delete(key);
      return null;
    }

    // Move to end (most recently used) by re-inserting
    this.entries.delete(key);
    this.entries.set(key, entry);
    return entry.data;
  }

  set(key: string, data: GraphData): void {
    // If key exists, delete first to update insertion order
    this.entries.delete(key);

    // Evict oldest (first) entry if at capacity
    if (this.entries.size >= CACHE_MAX_ENTRIES) {
      const oldest = this.entries.keys().next().value;
      if (oldest !== undefined) {
        this.entries.delete(oldest);
      }
    }

    this.entries.set(key, { data, timestamp: Date.now() });
  }
}

const cache = new LruCache();

interface UseGraphDataResult {
  data: GraphData | null;
  loading: boolean;
  error: string | null;
}

export function useGraphData(
  entityId: string | undefined,
  depth: number,
): UseGraphDataResult {
  const [data, setData] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    if (!entityId) return;

    const key = `${entityId}:${String(depth)}`;
    const cached = cache.get(key);
    if (cached) {
      setData(cached);
    }

    // Abort any in-flight request before starting a new one
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setLoading(true);
    setError(null);

    getGraphData(entityId, depth, undefined, controller.signal)
      .then((result) => {
        cache.set(key, result);
        setData(result);
      })
      .catch((err: Error) => {
        if (err.name !== "AbortError") {
          setError(err.message);
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      });

    return () => controller.abort();
  }, [entityId, depth]);

  return { data, loading, error };
}
