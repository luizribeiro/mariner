import { Story } from "@storybook/react";
import axios from "axios";
import MockAdapter from "axios-mock-adapter";
import React from "react";
import PrintStatus from "../PrintStatus";

const axiosMock = new MockAdapter(axios);

export default {
  title: "Example/PrintStatus",
  component: PrintStatus,
  argTypes: {
    isPrinting: { control: "boolean" },
    progress: { control: { type: "number", min: 0, max: 100 } },
    selectedFile: { control: "text" },
  },
};

const Template: Story = (args) => {
  axiosMock.onGet("print_status").reply(200, {
    selected_file: args.selectedFile,
    is_printing: args.isPrinting,
    progress: args.progress,
  });
  return <PrintStatus />;
};

export const Printing = Template.bind({});
Printing.args = {
  isPrinting: true,
  selectedFile: "lattice.ctb",
  progress: 20.0,
};

export const Paused = Template.bind({});
Paused.args = {
  isPrinting: false,
  selectedFile: "lattice.ctb",
  progress: 20.0,
};

export const Stopped = Template.bind({});
Stopped.args = {
  isPrinting: false,
  selectedFile: "lattice.ctb",
  progress: 0.0,
};
