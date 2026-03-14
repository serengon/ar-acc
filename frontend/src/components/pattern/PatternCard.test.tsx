import { render, screen, fireEvent } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { PatternCard } from "./PatternCard";
import "../../i18n";

const mockPattern = {
  id: "self_dealing_amendment",
  name_pt: "Emenda autodirecionada",
  name_en: "Self-dealing amendment",
  description_pt: "Parlamentar autor de emenda com empresa familiar",
  description_en: "Legislator authored amendment where family company won",
};

describe("PatternCard", () => {
  it("renders pattern name and description in PT", () => {
    render(<PatternCard pattern={mockPattern} />);
    expect(screen.getByText("Emenda autodirecionada")).toBeDefined();
    expect(
      screen.getByText("Parlamentar autor de emenda com empresa familiar"),
    ).toBeDefined();
  });

  it("renders pattern id", () => {
    render(<PatternCard pattern={mockPattern} />);
    expect(screen.getByText("self_dealing_amendment")).toBeDefined();
  });

  it("calls onClick with pattern id", () => {
    const onClick = vi.fn();
    render(<PatternCard pattern={mockPattern} onClick={onClick} />);
    fireEvent.click(screen.getByRole("button"));
    expect(onClick).toHaveBeenCalledWith("self_dealing_amendment");
  });

  it("applies active class when active", () => {
    const { container } = render(<PatternCard pattern={mockPattern} active />);
    const button = container.querySelector("button");
    expect(button?.className).toContain("active");
  });
});
