import { AxiosError } from "axios";
import React from "react";
import { AlertFunction } from "./components/AlertServiceProvider";

export function renderTime(time_secs: number): string {
  const printHours = Math.floor(time_secs / 3600);
  const printMinutes = Math.floor((time_secs % 3600) / 60)
    .toString()
    .padStart(2, "0");
  return `${printHours}h${printMinutes}`;
}

export function setState<TProps, TState>(
  component: React.Component<TProps, TState>,
  newState: TState
): Promise<void> {
  return new Promise((resolve) => component.setState(newState, resolve));
}

export function isAxiosError(error: Error): error is AxiosError {
  return (error as AxiosError).isAxiosError !== undefined;
}

export async function handleError(
  error: Error,
  alertFn: AlertFunction
): Promise<void> {
  if (isAxiosError(error)) {
    if (error.response && error.response.data) {
      await alertFn({
        title: error.response.data.title,
        description: error.response.data.description,
        traceback: error.response.data.traceback,
      });
    } else if (error.response) {
      await alertFn({
        title: "Something went wrong",
        description: `The server replied with a ${error.response.status} HTTP status code.`,
      });
    } else {
      await alertFn({
        title: "Something went wrong",
        description: "Sorry, I don't know what happened.",
      });
    }
  }
}
