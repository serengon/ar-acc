import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import "@/i18n";

import { SearchBar } from "./SearchBar";

describe("SearchBar", () => {
  it("renders input, select, and button", () => {
    render(<SearchBar onSearch={vi.fn()} />);
    expect(screen.getByPlaceholderText(/CPF/)).toBeInTheDocument();
    expect(screen.getByRole("combobox")).toBeInTheDocument();
    expect(screen.getByRole("button")).toBeInTheDocument();
  });

  it("calls onSearch with query and type on submit", async () => {
    const onSearch = vi.fn();
    const user = userEvent.setup();

    render(<SearchBar onSearch={onSearch} />);

    await user.type(screen.getByPlaceholderText(/CPF/), "João Silva");
    await user.click(screen.getByRole("button"));

    expect(onSearch).toHaveBeenCalledWith({ query: "João Silva", type: "all" });
  });

  it("does not call onSearch with empty query", async () => {
    const onSearch = vi.fn();
    const user = userEvent.setup();

    render(<SearchBar onSearch={onSearch} />);
    await user.click(screen.getByRole("button"));

    expect(onSearch).not.toHaveBeenCalled();
  });

  it("shows loading text when isLoading is true", () => {
    render(<SearchBar onSearch={vi.fn()} isLoading />);
    expect(screen.getByRole("button")).toHaveTextContent(/Carregando/);
  });

  it("allows selecting a type filter", async () => {
    const onSearch = vi.fn();
    const user = userEvent.setup();

    render(<SearchBar onSearch={onSearch} />);

    await user.selectOptions(screen.getByRole("combobox"), "company");
    await user.type(screen.getByPlaceholderText(/CPF/), "Acme");
    await user.click(screen.getByRole("button"));

    expect(onSearch).toHaveBeenCalledWith({ query: "Acme", type: "company" });
  });
});
