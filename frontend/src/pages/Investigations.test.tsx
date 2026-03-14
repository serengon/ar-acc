import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router";
import { beforeEach, describe, expect, it, vi } from "vitest";

import "@/i18n";

// Mock investigation sub-components to avoid deep dependency tree
vi.mock("@/components/investigation/InvestigationPanel", () => ({
  InvestigationPanel: () => <div data-testid="investigation-panel">Panel</div>,
}));

vi.mock("@/components/investigation/InvestigationDetail", () => ({
  InvestigationDetail: () => <div data-testid="investigation-detail">Detail</div>,
}));

vi.mock("@/components/investigation/AnnotationEditor", () => ({
  AnnotationEditor: () => <div data-testid="annotation-editor" />,
}));

vi.mock("@/components/investigation/TagManager", () => ({
  TagManager: () => <div data-testid="tag-manager" />,
}));

vi.mock("@/components/investigation/Timeline", () => ({
  Timeline: () => <div data-testid="timeline" />,
}));

// Mock investigation store
const mockSetActiveInvestigation = vi.fn();
vi.mock("@/stores/investigation", () => ({
  useInvestigationStore: (selector?: (state: Record<string, unknown>) => unknown) => {
    const state = {
      setActiveInvestigation: mockSetActiveInvestigation,
      activeInvestigationId: null,
    };
    return selector ? selector(state) : state;
  },
}));

import { Investigations } from "./Investigations";

function renderInvestigations(path = "/investigations") {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="/investigations" element={<Investigations />} />
        <Route path="/investigations/:investigationId" element={<Investigations />} />
      </Routes>
    </MemoryRouter>,
  );
}

describe("Investigations", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders without crashing", () => {
    renderInvestigations();
    expect(screen.getByTestId("investigation-panel")).toBeInTheDocument();
    expect(screen.getByTestId("investigation-detail")).toBeInTheDocument();
  });

  it("renders panel and detail sub-components", () => {
    renderInvestigations();
    expect(screen.getByText("Panel")).toBeInTheDocument();
    expect(screen.getByText("Detail")).toBeInTheDocument();
  });

  it("does not render annotation/tag/timeline without active investigation", () => {
    renderInvestigations();
    expect(screen.queryByTestId("annotation-editor")).not.toBeInTheDocument();
    expect(screen.queryByTestId("tag-manager")).not.toBeInTheDocument();
    expect(screen.queryByTestId("timeline")).not.toBeInTheDocument();
  });
});
