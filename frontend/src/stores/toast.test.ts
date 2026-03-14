import {
  afterEach,
  beforeEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";

import { useToastStore } from "./toast";

function resetStore() {
  useToastStore.setState({ toasts: [] });
}

describe("useToastStore", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    resetStore();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("initial state has empty toasts array", () => {
    expect(useToastStore.getState().toasts).toEqual([]);
  });

  it("addToast adds a toast with correct type and message", () => {
    useToastStore.getState().addToast("success", "Saved");
    const toasts = useToastStore.getState().toasts;
    expect(toasts).toHaveLength(1);
    expect(toasts[0]!.type).toBe("success");
    expect(toasts[0]!.message).toBe("Saved");
    expect(toasts[0]!.id).toMatch(/^toast-/);
  });

  it("multiple toasts can be added", () => {
    useToastStore.getState().addToast("success", "First");
    useToastStore.getState().addToast("error", "Second");
    useToastStore.getState().addToast("info", "Third");
    const toasts = useToastStore.getState().toasts;
    expect(toasts).toHaveLength(3);
    expect(toasts[0]!.message).toBe("First");
    expect(toasts[1]!.message).toBe("Second");
    expect(toasts[2]!.message).toBe("Third");
  });

  it("removeToast removes by id", () => {
    useToastStore.getState().addToast("info", "Keep");
    useToastStore.getState().addToast("warning", "Remove me");
    const idToRemove = useToastStore.getState().toasts[1]!.id;

    useToastStore.getState().removeToast(idToRemove);

    const toasts = useToastStore.getState().toasts;
    expect(toasts).toHaveLength(1);
    expect(toasts[0]!.message).toBe("Keep");
  });

  it("max 5 toasts enforced — oldest removed", () => {
    for (let i = 1; i <= 6; i++) {
      useToastStore.getState().addToast("info", `Toast ${i}`);
    }
    const toasts = useToastStore.getState().toasts;
    expect(toasts).toHaveLength(5);
    // The first toast ("Toast 1") should have been evicted
    expect(toasts[0]!.message).toBe("Toast 2");
    expect(toasts[4]!.message).toBe("Toast 6");
  });

  it("auto-dismiss after 3 seconds", () => {
    useToastStore.getState().addToast("success", "Vanishing");
    expect(useToastStore.getState().toasts).toHaveLength(1);

    vi.advanceTimersByTime(2999);
    expect(useToastStore.getState().toasts).toHaveLength(1);

    vi.advanceTimersByTime(1);
    expect(useToastStore.getState().toasts).toHaveLength(0);
  });

  it("auto-dismiss removes only the specific toast", () => {
    useToastStore.getState().addToast("info", "First");

    // Add a second toast 1 second later
    vi.advanceTimersByTime(1000);
    useToastStore.getState().addToast("info", "Second");

    // After 2 more seconds, the first should be gone (3s total), second stays
    vi.advanceTimersByTime(2000);
    const toasts = useToastStore.getState().toasts;
    expect(toasts).toHaveLength(1);
    expect(toasts[0]!.message).toBe("Second");
  });
});
