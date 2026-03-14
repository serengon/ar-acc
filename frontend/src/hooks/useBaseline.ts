import { useCallback, useEffect, useState } from "react";

import { type BaselineResponse, getBaseline } from "@/api/client";

interface UseBaselineResult {
  data: BaselineResponse | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useBaseline(entityId: string | undefined): UseBaselineResult {
  const [data, setData] = useState<BaselineResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refetch = useCallback(() => {
    if (!entityId) return;
    setLoading(true);
    setError(null);
    getBaseline(entityId)
      .then(setData)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [entityId]);

  useEffect(() => {
    refetch();
  }, [refetch]);

  return { data, loading, error, refetch };
}
