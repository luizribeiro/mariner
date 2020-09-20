import { Story } from "@storybook/react";
import axios from "axios";
import MockAdapter from "axios-mock-adapter";
import React from "react";
import FileList from "../FileList";

const axiosMock = new MockAdapter(axios);

export default {
  title: "FileList",
  component: FileList,
};

const Template: Story = (_args) => {
  axiosMock.onGet("api/file_list").reply(200, {
    files: [
      { filename: "z-axis-stabilizer.ctb" },
      { filename: "case v2.ctb" },
      { filename: "lattice.ctb" },
      { filename: "pi zero case 2.ctb" },
      { filename: "pi zero case.ctb" },
      { filename: "pi stem case.ctb" },
      { filename: "_Ark-chitu.ctb" },
      { filename: "_Ark-3.ctb" },
      { filename: "ark-base.ctb" },
      { filename: "rake-that-doesnt-break.ctb" },
      { filename: "sd card case.ctb" },
      { filename: "_rake_in_the_lake_-_rake.ctb" },
      { filename: "rake-no-gods-no-masters.ctb" },
      { filename: "Busbar-cover.ctb" },
      { filename: "Busbar-cover-again.ctb" },
      { filename: "LittleBBC.ctb" },
    ],
  });
  return <FileList />;
};

export const Default = Template.bind({});
