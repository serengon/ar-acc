import { render, screen, fireEvent } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import "@/i18n";

import { Button } from "./Button";

describe("Button", () => {
  it("renders children text", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole("button", { name: "Click me" })).toBeInTheDocument();
  });

  it("applies variant class for primary", () => {
    render(<Button variant="primary">Primary</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("primary");
  });

  it("applies variant class for secondary", () => {
    render(<Button variant="secondary">Secondary</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("secondary");
  });

  it("applies variant class for ghost", () => {
    render(<Button variant="ghost">Ghost</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("ghost");
  });

  it("applies variant class for danger", () => {
    render(<Button variant="danger">Danger</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("danger");
  });

  it("applies variant class for system", () => {
    render(<Button variant="system">System</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("system");
  });

  it("shows spinner when loading=true", () => {
    render(<Button loading>Save</Button>);
    // Spinner renders with role="status"
    expect(screen.getByRole("status")).toBeInTheDocument();
    // Children text should not be visible while loading
    expect(screen.queryByText("Save")).not.toBeInTheDocument();
  });

  it("is disabled when disabled prop is true", () => {
    render(<Button disabled>Disabled</Button>);
    expect(screen.getByRole("button")).toBeDisabled();
  });

  it("is disabled when loading is true", () => {
    render(<Button loading>Loading</Button>);
    expect(screen.getByRole("button")).toBeDisabled();
  });

  it("renders icon when icon prop provided", () => {
    render(
      <Button icon={<span data-testid="icon">*</span>}>With Icon</Button>,
    );
    expect(screen.getByTestId("icon")).toBeInTheDocument();
    expect(screen.getByText("With Icon")).toBeInTheDocument();
  });

  it("calls onClick handler", () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole("button"));
    expect(handleClick).toHaveBeenCalledOnce();
  });

  it("does not call onClick when disabled", () => {
    const handleClick = vi.fn();
    render(
      <Button onClick={handleClick} disabled>
        Click
      </Button>,
    );
    fireEvent.click(screen.getByRole("button"));
    expect(handleClick).not.toHaveBeenCalled();
  });

  it("icon-only mode when no children but icon provided", () => {
    render(<Button icon={<span data-testid="solo-icon">X</span>} />);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("iconOnly");
    expect(screen.getByTestId("solo-icon")).toBeInTheDocument();
  });

  it("applies custom className alongside internal classes", () => {
    render(<Button className="custom-extra">Styled</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("custom-extra");
    expect(btn.className).toContain("button");
  });
});
