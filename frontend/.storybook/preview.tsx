import React from "react";
import { MemoryRouter } from "react-router";
import { AlertServiceProvider } from "../src/components/AlertServiceProvider";

export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
};

export const decorators = [
  (Story) => (
    <AlertServiceProvider>
      <Story />
    </AlertServiceProvider>
  ),
  (Story) => (
    <MemoryRouter initialEntries={["/"]}>
      <Story />
    </MemoryRouter>
  ),
];
