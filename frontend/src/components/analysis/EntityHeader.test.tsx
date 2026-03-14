import { render, screen, fireEvent } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import "@/i18n";

import type { EntityDetail, ExposureResponse } from "@/api/client";

import { EntityHeader } from "./EntityHeader";

const mockEntity: EntityDetail = {
  id: "entity-1",
  type: "person",
  properties: { nome: "Joao da Silva" },
  sources: [{ database: "TSE" }],
  is_pep: false,
};

const mockExposure: ExposureResponse = {
  entity_id: "entity-1",
  exposure_index: 65,
  factors: [
    { name: "connections", value: 12, percentile: 80, weight: 1, sources: ["TSE"] },
    { name: "money_involved", value: 500000, percentile: 70, weight: 1, sources: ["Transparencia"] },
  ],
  peer_group: "person",
  peer_count: 100,
  sources: [{ database: "TSE" }],
};

describe("EntityHeader", () => {
  it("renders entity name", () => {
    render(
      <EntityHeader
        entity={mockEntity}
        exposure={null}
        onBack={vi.fn()}
        onAddToInvestigation={vi.fn()}
      />,
    );
    expect(screen.getByText("Joao da Silva")).toBeInTheDocument();
  });

  it("renders type badge", () => {
    render(
      <EntityHeader
        entity={mockEntity}
        exposure={null}
        onBack={vi.fn()}
        onAddToInvestigation={vi.fn()}
      />,
    );
    expect(screen.getByText("Pessoa")).toBeInTheDocument();
  });

  it("renders source badge", () => {
    render(
      <EntityHeader
        entity={mockEntity}
        exposure={null}
        onBack={vi.fn()}
        onAddToInvestigation={vi.fn()}
      />,
    );
    expect(screen.getByText("TSE")).toBeInTheDocument();
  });

  it("calls onBack when back button clicked", () => {
    const onBack = vi.fn();
    render(
      <EntityHeader
        entity={mockEntity}
        exposure={null}
        onBack={onBack}
        onAddToInvestigation={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByLabelText("Voltar"));
    expect(onBack).toHaveBeenCalledOnce();
  });

  it("calls onAddToInvestigation when add button clicked", () => {
    const onAdd = vi.fn();
    render(
      <EntityHeader
        entity={mockEntity}
        exposure={null}
        onBack={vi.fn()}
        onAddToInvestigation={onAdd}
      />,
    );
    fireEvent.click(screen.getByText("Adicionar entidade"));
    expect(onAdd).toHaveBeenCalledOnce();
  });

  it("renders ScoreRing when exposure is provided", () => {
    render(
      <EntityHeader
        entity={mockEntity}
        exposure={mockExposure}
        onBack={vi.fn()}
        onAddToInvestigation={vi.fn()}
      />,
    );
    expect(screen.getByText("65")).toBeInTheDocument();
  });
});
