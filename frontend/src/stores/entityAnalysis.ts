import { create } from "zustand";

type AnalysisTab = "graph" | "connections" | "timeline" | "export";
type RightPanelTab = "insights" | "detail";

interface EntityAnalysisState {
  activeTab: AnalysisTab;
  setActiveTab: (tab: AnalysisTab) => void;
  rightPanelTab: RightPanelTab;
  setRightPanelTab: (tab: RightPanelTab) => void;
  selectedNodeId: string | null;
  setSelectedNodeId: (id: string | null) => void;
  hoveredNodeId: string | null;
  setHoveredNodeId: (id: string | null) => void;
  highlightedNodeIds: Set<string>;
  setHighlightedNodeIds: (ids: Set<string>) => void;
  timelineCursor: string | null;
  setTimelineCursor: (cursor: string | null) => void;
}

export const useEntityAnalysisStore = create<EntityAnalysisState>((set) => ({
  activeTab: "graph",
  setActiveTab: (tab) => set({ activeTab: tab }),
  rightPanelTab: "insights",
  setRightPanelTab: (tab) => set({ rightPanelTab: tab }),
  selectedNodeId: null,
  setSelectedNodeId: (id) => set({ selectedNodeId: id }),
  hoveredNodeId: null,
  setHoveredNodeId: (id) => set({ hoveredNodeId: id }),
  highlightedNodeIds: new Set(),
  setHighlightedNodeIds: (ids) => set({ highlightedNodeIds: ids }),
  timelineCursor: null,
  setTimelineCursor: (cursor) => set({ timelineCursor: cursor }),
}));
