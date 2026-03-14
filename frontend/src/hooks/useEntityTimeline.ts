import { useCallback, useEffect, useRef, useState } from "react";

import { getEntityTimeline, type TimelineEvent } from "@/api/client";

export function useEntityTimeline(entityId: string) {
  const [events, setEvents] = useState<TimelineEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(false);
  const cursorRef = useRef<string | null>(null);

  useEffect(() => {
    if (!entityId) {
      setEvents([]);
      setLoading(false);
      setError(null);
      setHasMore(false);
      cursorRef.current = null;
      return;
    }

    setEvents([]);
    setLoading(true);
    setError(null);
    cursorRef.current = null;

    getEntityTimeline(entityId)
      .then((res) => {
        setEvents(res.events);
        cursorRef.current = res.next_cursor;
        setHasMore(res.next_cursor !== null);
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, [entityId]);

  const loadMore = useCallback(() => {
    if (!cursorRef.current) return;
    setLoading(true);
    getEntityTimeline(entityId, cursorRef.current)
      .then((res) => {
        setEvents((prev) => [...prev, ...res.events]);
        cursorRef.current = res.next_cursor;
        setHasMore(res.next_cursor !== null);
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, [entityId]);

  return { events, loading, error, hasMore, loadMore };
}
