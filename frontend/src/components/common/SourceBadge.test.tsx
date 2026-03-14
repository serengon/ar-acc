import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { SourceBadge } from "./SourceBadge";

describe("SourceBadge", () => {
  it("renders the source name", () => {
    render(<SourceBadge source="TSE" />);
    expect(screen.getByText("TSE")).toBeInTheDocument();
  });

  it("renders different source names", () => {
    render(<SourceBadge source="CNPJ" />);
    expect(screen.getByText("CNPJ")).toBeInTheDocument();
  });
});
