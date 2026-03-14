import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router";
import { beforeEach, describe, expect, it, vi } from "vitest";

import "@/i18n";

// Mock useBaseline hook
const mockUseBaseline = vi.fn();
vi.mock("@/hooks/useBaseline", () => ({
  useBaseline: (...args: unknown[]) => mockUseBaseline(...args),
}));

// Mock MoneyLabel
vi.mock("@/components/common/MoneyLabel", () => ({
  MoneyLabel: ({ value }: { value: number }) => <span>R$ {value}</span>,
}));

import { Baseline } from "./Baseline";

function renderBaseline(path = "/baseline") {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="/baseline" element={<Baseline />} />
        <Route path="/baseline/:entityId" element={<Baseline />} />
      </Routes>
    </MemoryRouter>,
  );
}

describe("Baseline", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders without crashing and shows title", () => {
    mockUseBaseline.mockReturnValue({ data: null, loading: false, error: null });
    renderBaseline();

    expect(screen.getByText("Compara\u00E7\u00E3o com Pares")).toBeInTheDocument();
  });

  it("shows no-data message when no entityId", () => {
    mockUseBaseline.mockReturnValue({ data: null, loading: false, error: null });
    renderBaseline();

    expect(screen.getByText("Sem dados de compara\u00E7\u00E3o.")).toBeInTheDocument();
  });

  it("shows comparison table when data is available", () => {
    mockUseBaseline.mockReturnValue({
      data: {
        entity_id: "test-entity",
        comparisons: [
          {
            company_name: "Empresa Teste",
            company_cnpj: "12345678000190",
            company_id: "c1",
            contract_count: 15,
            total_value: 1_500_000,
            peer_count: 10,
            peer_avg_contracts: 5.0,
            peer_avg_value: 500_000,
            contract_ratio: 3.0,
            value_ratio: 3.0,
            comparison_dimension: "sector",
            comparison_key: "Constru\u00E7\u00E3o",
            sources: [],
          },
        ],
        total: 1,
      },
      loading: false,
      error: null,
    });

    renderBaseline("/baseline/test-entity");

    expect(screen.getByText("Empresa Teste")).toBeInTheDocument();
    expect(screen.getByText("15")).toBeInTheDocument();
  });
});
