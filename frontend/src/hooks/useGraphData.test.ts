import { renderHook, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("@/api/client", () => ({
  getGraphData: vi.fn(),
}));

import { getGraphData } from "@/api/client";
import { useGraphData } from "./useGraphData";

const mockGetGraphData = vi.mocked(getGraphData);

describe("useGraphData", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns loading state when entityId is provided", () => {
    mockGetGraphData.mockReturnValue(new Promise(() => {}));

    const { result } = renderHook(() => useGraphData("entity-1", 1));

    expect(result.current.loading).toBe(true);
    expect(result.current.data).toBeNull();
    expect(result.current.error).toBeNull();
  });

  it("returns data after successful fetch", async () => {
    const graphData = {
      nodes: [{ id: "n1", label: "Test", type: "person", properties: {}, sources: [] }],
      edges: [],
    };
    mockGetGraphData.mockResolvedValue(graphData);

    const { result } = renderHook(() => useGraphData("entity-1", 1));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.data).toEqual(graphData);
    expect(result.current.error).toBeNull();
  });

  it("returns error on fetch failure", async () => {
    mockGetGraphData.mockRejectedValue(new Error("Network error"));

    // Use a unique entityId to avoid LRU cache hits from previous tests
    const { result } = renderHook(() => useGraphData("entity-error-test", 1));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.error).toBe("Network error");
  });

  it("does not fetch when entityId is undefined", () => {
    const { result } = renderHook(() => useGraphData(undefined, 1));

    expect(result.current.loading).toBe(false);
    expect(result.current.data).toBeNull();
    expect(mockGetGraphData).not.toHaveBeenCalled();
  });
});
