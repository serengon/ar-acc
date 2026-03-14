import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { beforeEach, describe, expect, it, vi } from "vitest";

import "@/i18n";

vi.mock("@/api/client", () => ({
  searchEntities: vi.fn(),
}));

import { searchEntities } from "@/api/client";
import { Search } from "./Search";

const mockSearchEntities = vi.mocked(searchEntities);

function renderSearch() {
  return render(
    <MemoryRouter>
      <Search />
    </MemoryRouter>,
  );
}

describe("Search", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders search bar", () => {
    renderSearch();
    expect(screen.getByPlaceholderText(/CPF/)).toBeInTheDocument();
    expect(screen.getByRole("button")).toBeInTheDocument();
  });

  it("shows results after search", async () => {
    const user = userEvent.setup();
    mockSearchEntities.mockResolvedValueOnce({
      results: [
        { id: "e1", name: "João Silva", type: "person", sources: [{ database: "TSE" }], score: 1.0 },
      ],
      total: 1,
      page: 1,
      size: 20,
    });

    renderSearch();

    await user.type(screen.getByPlaceholderText(/CPF/), "João");
    await user.click(screen.getByRole("button", { name: /buscar/i }));

    await waitFor(() => {
      expect(screen.getByText("João Silva")).toBeInTheDocument();
    });
  });

  it("shows spinner during loading", async () => {
    const user = userEvent.setup();
    let resolve: (v: unknown) => void;
    const pending = new Promise((r) => {
      resolve = r;
    });
    mockSearchEntities.mockReturnValueOnce(pending as ReturnType<typeof searchEntities>);

    renderSearch();

    await user.type(screen.getByPlaceholderText(/CPF/), "test");
    await user.click(screen.getByRole("button", { name: /buscar/i }));

    expect(screen.getByRole("status")).toBeInTheDocument();

    resolve!({ results: [], total: 0, page: 1, size: 20 });
    await waitFor(() => {
      expect(screen.queryByRole("status")).not.toBeInTheDocument();
    });
  });

  it("shows error message on failure", async () => {
    const user = userEvent.setup();
    mockSearchEntities.mockRejectedValueOnce(new Error("Network error"));

    renderSearch();

    await user.type(screen.getByPlaceholderText(/CPF/), "test");
    await user.click(screen.getByRole("button", { name: /buscar/i }));

    await waitFor(() => {
      expect(screen.getByText(/erro ao buscar/i)).toBeInTheDocument();
    });
  });

  it("does not show results before first search", () => {
    renderSearch();
    expect(screen.queryByText(/nenhum resultado/i)).not.toBeInTheDocument();
  });
});
