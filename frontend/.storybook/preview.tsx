import React from "react";
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
];
