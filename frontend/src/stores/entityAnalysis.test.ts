import { describe, expect, it, beforeEach } from "vitest";

import { useEntityAnalysisStore } from "./entityAnalysis";

describe("useEntityAnalysisStore", () => {
  beforeEach(() => {
    useEntityAnalysisStore.setState({
      activeTab: "graph",
      rightPanelTab: "insights",
      selectedNodeId: null,
      hoveredNodeId: null,
      highlightedNodeIds: new Set(),
      timelineCursor: null,
    });
  });

  it("sets activeTab", () => {
    useEntityAnalysisStore.getState().setActiveTab("timeline");
    expect(useEntityAnalysisStore.getState().activeTab).toBe("timeline");
  });

  it("sets rightPanelTab", () => {
    useEntityAnalysisStore.getState().setRightPanelTab("detail");
    expect(useEntityAnalysisStore.getState().rightPanelTab).toBe("detail");
  });

  it("sets selectedNodeId", () => {
    useEntityAnalysisStore.getState().setSelectedNodeId("node-1");
    expect(useEntityAnalysisStore.getState().selectedNodeId).toBe("node-1");
  });

  it("clears selectedNodeId with null", () => {
    useEntityAnalysisStore.getState().setSelectedNodeId("node-1");
    useEntityAnalysisStore.getState().setSelectedNodeId(null);
    expect(useEntityAnalysisStore.getState().selectedNodeId).toBeNull();
  });

  it("sets hoveredNodeId", () => {
    useEntityAnalysisStore.getState().setHoveredNodeId("node-2");
    expect(useEntityAnalysisStore.getState().hoveredNodeId).toBe("node-2");
  });

  it("sets highlightedNodeIds", () => {
    const ids = new Set(["a", "b", "c"]);
    useEntityAnalysisStore.getState().setHighlightedNodeIds(ids);
    expect(useEntityAnalysisStore.getState().highlightedNodeIds).toEqual(ids);
  });

  it("sets timelineCursor", () => {
    useEntityAnalysisStore.getState().setTimelineCursor("cursor-abc");
    expect(useEntityAnalysisStore.getState().timelineCursor).toBe("cursor-abc");
  });

  it("defaults to graph tab", () => {
    expect(useEntityAnalysisStore.getState().activeTab).toBe("graph");
  });

  it("defaults to insights panel", () => {
    expect(useEntityAnalysisStore.getState().rightPanelTab).toBe("insights");
  });
});
