import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ScoreRing } from "./ScoreRing";

describe("ScoreRing", () => {
  it("renders SVG with value", () => {
    render(<ScoreRing value={42} />);
    expect(screen.getByText("42")).toBeInTheDocument();
  });

  it("handles value 0", () => {
    render(<ScoreRing value={0} />);
    expect(screen.getByText("0")).toBeInTheDocument();
  });

  it("handles value 100", () => {
    render(<ScoreRing value={100} />);
    expect(screen.getByText("100")).toBeInTheDocument();
  });

  it("clamps value above 100", () => {
    render(<ScoreRing value={150} />);
    expect(screen.getByText("100")).toBeInTheDocument();
  });

  it("clamps value below 0", () => {
    render(<ScoreRing value={-10} />);
    expect(screen.getByText("0")).toBeInTheDocument();
  });

  it("renders with custom size", () => {
    const { container } = render(<ScoreRing value={50} size={64} />);
    const ring = container.firstElementChild as HTMLElement;
    expect(ring.style.width).toBe("64px");
    expect(ring.style.height).toBe("64px");
  });

  it("applies custom className", () => {
    const { container } = render(
      <ScoreRing value={50} className="custom-class" />,
    );
    expect(container.firstElementChild?.className).toContain("custom-class");
  });
});
