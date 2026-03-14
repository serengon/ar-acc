import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { describe, expect, it } from "vitest";

import "@/i18n";

import type { SearchResult } from "@/api/client";
import { SearchResults } from "./SearchResults";

const sampleResults: SearchResult[] = [
  {
    id: "e1",
    name: "João Silva",
    type: "person",
    document: "***.***.***-34",
    sources: [{ database: "TSE" }, { database: "CNPJ" }],
    score: 1.0,
  },
  {
    id: "e2",
    name: "Acme Ltda",
    type: "company",
    sources: [{ database: "CNPJ" }],
    score: 0.9,
  },
];

function renderResults(results: SearchResult[]) {
  return render(
    <MemoryRouter>
      <SearchResults results={results} />
    </MemoryRouter>,
  );
}

describe("SearchResults", () => {
  it("shows no results message when empty", () => {
    renderResults([]);
    expect(screen.getByText(/nenhum resultado/i)).toBeInTheDocument();
  });

  it("renders result items with names", () => {
    renderResults(sampleResults);
    expect(screen.getByText("João Silva")).toBeInTheDocument();
    expect(screen.getByText("Acme Ltda")).toBeInTheDocument();
  });

  it("renders type badges", () => {
    renderResults(sampleResults);
    expect(screen.getByText("Pessoa")).toBeInTheDocument();
    expect(screen.getByText("Empresa")).toBeInTheDocument();
  });

  it("links to graph page for each result", () => {
    renderResults(sampleResults);
    const links = screen.getAllByRole("link");
    expect(links[0]).toHaveAttribute("href", "/app/analysis/e1");
    expect(links[1]).toHaveAttribute("href", "/app/analysis/e2");
  });

  it("shows source badges", () => {
    renderResults(sampleResults);
    expect(screen.getByText("TSE")).toBeInTheDocument();
    expect(screen.getAllByText("CNPJ")).toHaveLength(2);
  });

  it("shows document when available", () => {
    renderResults(sampleResults);
    expect(screen.getByText("***.***.***-34")).toBeInTheDocument();
  });
});
