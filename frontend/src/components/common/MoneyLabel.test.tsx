import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { MoneyLabel } from "./MoneyLabel";

describe("MoneyLabel", () => {
  it("formats a value as Brazilian Real", () => {
    render(<MoneyLabel value={1234567.89} />);
    const el = screen.getByText(/1\.234\.567,89/);
    expect(el).toBeInTheDocument();
  });

  it("formats zero", () => {
    render(<MoneyLabel value={0} />);
    const el = screen.getByText(/0,00/);
    expect(el).toBeInTheDocument();
  });

  it("formats negative values", () => {
    render(<MoneyLabel value={-500.5} />);
    const el = screen.getByText(/500,50/);
    expect(el).toBeInTheDocument();
  });

  it("applies custom className", () => {
    render(<MoneyLabel value={100} className="custom" />);
    const el = screen.getByText(/100,00/);
    expect(el).toHaveClass("custom");
  });
});
