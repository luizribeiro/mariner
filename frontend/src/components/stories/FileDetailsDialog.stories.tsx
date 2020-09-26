import { Story } from "@storybook/react";
import axios from "axios";
import MockAdapter from "axios-mock-adapter";
import React from "react";
import FileDetailsDialog from "../FileDetailsDialog";

const axiosMock = new MockAdapter(axios, { delayResponse: 500 });

export default {
  title: "FileDetailsDialog",
  component: FileDetailsDialog,
};

const Template: Story = (_args) => {
  axiosMock.onGet("api/file_details").reply(200, {
    filename: "stairs.ctb",
    bed_size_mm: [68.04, 120.96, 150.0],
    height_mm: 20.0,
    layer_count: 400,
    layer_height_mm: 0.05,
    resolution: [1440, 2560],
    print_time_secs: 5621,
  });
  return <FileDetailsDialog filename="stairs.ctb" />;
};

export const Default = Template.bind({});
