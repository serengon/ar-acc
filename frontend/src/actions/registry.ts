import type { ReactNode } from "react";

export interface Action {
  id: string;
  label: string;
  shortcut?: string;
  icon?: ReactNode;
  group: string;
  handler: () => void;
}

let actions: Action[] = [];

export function registerActions(newActions: Action[]): void {
  actions = newActions;
}

export function getActions(): Action[] {
  return actions;
}

export function getAction(id: string): Action | undefined {
  return actions.find((a) => a.id === id);
}
