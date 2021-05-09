import React from "react";

export function renderTime(time_secs: number): string {
  const printHours = Math.floor(time_secs / 3600);
  const printMinutes = Math.floor((time_secs % 3600) / 60)
    .toString()
    .padStart(2, "0");
  return `${printHours}h${printMinutes}m`;
}

export function setState<TProps, TState>(
  component: React.Component<TProps, TState>,
  newState: TState
): Promise<void> {
  return new Promise((resolve) => component.setState(newState, resolve));
}

export async function sleep(waitInMilliseconds: number): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve, waitInMilliseconds));
}

export function getSupportedExtensions(): string {
  const element: HTMLMetaElement | null = document.head.querySelector(
    'meta[name="supported-extensions"]'
  );

  return element?.content ?? "";
}

export function getPrinterDisplayName(): string | undefined {
  const element: HTMLMetaElement | null = document.head.querySelector(
    'meta[name="printer-display-name"]'
  );

  return element?.content;
}
