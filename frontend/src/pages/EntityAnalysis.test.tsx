import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router";
import { beforeEach, describe, expect, it, vi } from "vitest";

import "@/i18n";

// Mock API client
vi.mock("@/api/client", () => ({
  getEntityByElementId: vi.fn(),
  getEntityPatterns: vi.fn(),
  getBaseline: vi.fn(),
  listInvestigations: vi.fn(),
  addEntityToInvestigation: vi.fn(),
  createInvestigation: vi.fn(),
}));

// Mock heavy sub-components
vi.mock("@/components/graph/GraphCanvas", () => ({
  GraphCanvas: () => <div data-testid="graph-canvas" />,
}));

vi.mock("@/components/graph/ControlsSidebar", () => ({
  ControlsSidebar: () => <div data-testid="controls-sidebar" />,
}));

vi.mock("@/components/analysis/AnalysisNav", () => ({
  AnalysisNav: () => <div data-testid="analysis-nav" />,
}));

vi.mock("@/components/analysis/ConnectionsList", () => ({
  ConnectionsList: () => <div data-testid="connections-list" />,
}));

vi.mock("@/components/analysis/EntityHeader", () => ({
  EntityHeader: ({ entity }: { entity: { id: string } }) => (
    <div data-testid="entity-header">Entity: {entity.id}</div>
  ),
}));

vi.mock("@/components/analysis/ExportView", () => ({
  ExportView: () => <div data-testid="export-view" />,
}));

vi.mock("@/components/analysis/InsightsPanel", () => ({
  InsightsPanel: () => <div data-testid="insights-panel" />,
}));

vi.mock("@/components/analysis/TimelineView", () => ({
  TimelineView: () => <div data-testid="timeline-view" />,
}));

// Mock hooks
vi.mock("@/hooks/useEntityExposure", () => ({
  useEntityExposure: () => ({ data: null, loading: false, error: null }),
}));

vi.mock("@/hooks/useGraphData", () => ({
  useGraphData: () => ({
    data: { nodes: [], edges: [] },
    loading: false,
    error: null,
  }),
}));

vi.mock("@/hooks/useEntityTimeline", () => ({
  useEntityTimeline: () => ({
    events: [],
    loading: false,
    hasMore: false,
    loadMore: vi.fn(),
  }),
}));

// Mock stores
vi.mock("@/stores/entityAnalysis", () => ({
  useEntityAnalysisStore: Object.assign(
    () => ({
      activeTab: "graph",
      setActiveTab: vi.fn(),
      selectedNodeId: null,
      setSelectedNodeId: vi.fn(),
      hoveredNodeId: null,
      setHoveredNodeId: vi.fn(),
      highlightedNodeIds: new Set<string>(),
    }),
    {
      getState: () => ({
        setRightPanelTab: vi.fn(),
      }),
    },
  ),
}));

vi.mock("@/stores/graphExplorer", () => ({
  useGraphExplorerStore: () => ({
    depth: 1,
    enabledTypes: new Set<string>(),
    enabledRelTypes: new Set<string>(),
    selectedNodeIds: new Set<string>(),
    sidebarCollapsed: false,
    detailPanelOpen: false,
    hoveredNodeId: null,
    hiddenNodeIds: new Set<string>(),
    layoutMode: "force" as const,
    reset: vi.fn(),
    toggleSidebar: vi.fn(),
    setDepth: vi.fn(),
    toggleType: vi.fn(),
    toggleRelType: vi.fn(),
    selectNode: vi.fn(),
    setHoveredNode: vi.fn(),
    setContextMenu: vi.fn(),
    setLayoutMode: vi.fn(),
    toggleFullscreen: vi.fn(),
  }),
}));

import { getEntityByElementId, getEntityPatterns, getBaseline } from "@/api/client";
import { EntityAnalysis } from "./EntityAnalysis";

const mockGetEntity = vi.mocked(getEntityByElementId);
const mockGetPatterns = vi.mocked(getEntityPatterns);
const mockGetBaseline = vi.mocked(getBaseline);

function renderEntityAnalysis(entityId = "entity-42") {
  return render(
    <MemoryRouter initialEntries={[`/analysis/${entityId}`]}>
      <Routes>
        <Route path="/analysis/:entityId" element={<EntityAnalysis />} />
      </Routes>
    </MemoryRouter>,
  );
}

describe("EntityAnalysis", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockGetPatterns.mockResolvedValue({ entity_id: null, patterns: [], total: 0 });
    mockGetBaseline.mockResolvedValue({ entity_id: "entity-42", comparisons: [], total: 0 });
  });

  it("shows loading spinner while fetching entity", () => {
    mockGetEntity.mockReturnValue(new Promise(() => {}));
    renderEntityAnalysis();

    expect(screen.getByRole("status")).toBeInTheDocument();
  });

  it("shows entity not found when fetch fails", async () => {
    mockGetEntity.mockRejectedValue(new Error("Not found"));
    renderEntityAnalysis();

    await waitFor(() => {
      expect(screen.getByText("Entidade n\u00E3o encontrada.")).toBeInTheDocument();
    });
  });

  it("renders entity header after successful fetch", async () => {
    mockGetEntity.mockResolvedValue({
      id: "entity-42",
      type: "person",
      properties: { nome: "Jo\u00E3o Silva" },
      sources: [{ database: "TSE" }],
      is_pep: false,
    });

    renderEntityAnalysis();

    await waitFor(() => {
      expect(screen.getByTestId("entity-header")).toBeInTheDocument();
    });

    expect(screen.getByText("Entity: entity-42")).toBeInTheDocument();
  });
});
