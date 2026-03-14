import { useEffect, useState } from "react";

import { getEntityExposure, type ExposureResponse } from "@/api/client";

export function useEntityExposure(entityId: string) {
  const [data, setData] = useState<ExposureResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    getEntityExposure(entityId)
      .then(setData)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, [entityId]);

  return { data, loading, error };
}
