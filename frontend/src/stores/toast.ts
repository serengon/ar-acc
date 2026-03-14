import { create } from "zustand";

type ToastType = "success" | "error" | "info" | "warning";

interface Toast {
  id: string;
  type: ToastType;
  message: string;
}

interface ToastState {
  toasts: Toast[];
  addToast: (type: ToastType, message: string) => void;
  removeToast: (id: string) => void;
}

const MAX_TOASTS = 5;

let counter = 0;

function generateId(): string {
  counter += 1;
  return `toast-${Date.now()}-${counter}`;
}

export const useToastStore = create<ToastState>((set, get) => ({
  toasts: [],

  addToast: (type, message) => {
    const id = generateId();
    const toast: Toast = { id, type, message };

    set((state) => {
      const next = [...state.toasts, toast];
      // Remove oldest if exceeded max
      if (next.length > MAX_TOASTS) {
        return { toasts: next.slice(next.length - MAX_TOASTS) };
      }
      return { toasts: next };
    });

    setTimeout(() => {
      get().removeToast(id);
    }, 3000);
  },

  removeToast: (id) => {
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    }));
  },
}));
