import { Story } from "@storybook/react";
import axios from "axios";
import MockAdapter from "axios-mock-adapter";
import React from "react";
import { MemoryRouter } from "react-router";
import PrintStatus from "../PrintStatus";

const axiosMock = new MockAdapter(axios);

export default {
  title: "PrintStatus",
  component: PrintStatus,
  argTypes: {
    state: {
      control: {
        type: "select",
        options: ["IDLE", "STARTING_PRINT", "PRINTING"],
      },
    },
    progress: { control: { type: "number", min: 0, max: 100 } },
    selectedFile: { control: "text" },
  },
};

const Template: Story = (args) => {
  axiosMock.onGet("api/print_status").reply(200, {
    state: args.state,
    selected_file: args.selectedFile,
    progress: args.progress,
    current_layer: args.current_layer,
    layer_count: args.layer_count,
    print_time_secs: args.print_time_secs,
  });
  return (
    <MemoryRouter>
      <PrintStatus />
    </MemoryRouter>
  );
};

export const Printing = Template.bind({});
Printing.args = {
  state: "PRINTING",
  selectedFile: "lattice.ctb",
  progress: 20.0,
  current_layer: 120,
  layer_count: 600,
  print_time_secs: 4800,
};

export const Paused = Template.bind({});
Paused.args = {
  state: "PAUSED",
  selectedFile: "lattice.ctb",
  progress: 20.0,
  current_layer: 120,
  layer_count: 600,
  print_time_secs: 4800,
};

export const Idle = Template.bind({});
Idle.args = {
  state: "IDLE",
  selectedFile: "lattice.ctb",
  progress: 0.0,
};

export const StartingPrint = Template.bind({});
StartingPrint.args = {
  state: "STARTING_PRINT",
  selectedFile: "lattice.ctb",
  progress: 0.0,
  current_layer: 1,
  layer_count: 600,
  print_time_secs: 4800,
};
