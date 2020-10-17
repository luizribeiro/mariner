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
  axiosMock.onGet("api/list_files?path=figures/").reply(200, {
    directories: [],
    files: [
      {
        filename: "batman.ctb",
        path: "figures/batman.ctb",
        print_time_secs: 3600,
        can_be_printed: true,
      },
    ],
  });

  axiosMock.onGet("api/list_files?path=functional/").reply(200, {
    directories: [],
    files: [
      {
        filename: "headphone-holder.ctb",
        path: "functional/headphone-holder.ctb",
        print_time_secs: 3600,
        can_be_printed: true,
      },
    ],
  });

  axiosMock.onGet("api/list_files?path=").reply(200, {
    directories: [{ dirname: "figures" }, { dirname: "functional" }],
    files: [
      {
        filename: "z-axis-stabilizer.ctb",
        path: "z-axis-stabilizer.ctb",
        print_time_secs: 3600,
        can_be_printed: true,
      },
      {
        filename: "case v2.ctb",
        path: "case v2.ctb",
        print_time_secs: 3540,
        can_be_printed: true,
      },
      {
        filename: "lattice.ctb",
        path: "lattice.ctb",
        print_time_secs: 11100,
        can_be_printed: true,
      },
      {
        filename: "pi zero case 2.ctb",
        path: "pi zero case 2.ctb",
        print_time_secs: 1800,
        can_be_printed: true,
      },
      {
        filename: "pi zero case.ctb",
        path: "pi zero case.ctb",
        print_time_secs: 9000,
        can_be_printed: true,
      },
      {
        filename: "pi stem case.ctb",
        path: "pi stem case.ctb",
        print_time_secs: 3600,
        can_be_printed: true,
      },
      {
        filename: "_Ark-chitu.ctb",
        path: "_Ark-chitu.ctb",
        print_time_secs: 3600,
        can_be_printed: true,
      },
      {
        filename: "_Ark-3.ctb",
        path: "_Ark-3.ctb",
        print_time_secs: 3600,
        can_be_printed: true,
      },
      {
        filename: "ark-base.ctb",
        path: "ark-base.ctb",
        print_time_secs: 3600,
        can_be_printed: true,
      },
      {
        filename: "rake-that-doesnt-break.ctb",
        path: "rake-that-doesnt-break.ctb",
        print_time_secs: 3600,
        can_be_printed: true,
      },
      {
        filename: "sd card case.ctb",
        path: "sd card case.ctb",
        print_time_secs: 3600,
        can_be_printed: true,
      },
      {
        filename: "_rake_in_the_lake_-_rake.ctb",
        path: "_rake_in_the_lake_-_rake.ctb",
        print_time_secs: 3600,
        can_be_printed: true,
      },
      {
        filename: "rake-no-gods-no-masters.ctb",
        path: "rake-no-gods-no-masters.ctb",
        print_time_secs: 3600,
        can_be_printed: true,
      },
      {
        filename: "Busbar-cover.ctb",
        path: "Busbar-cover.ctb",
        print_time_secs: 3600,
        can_be_printed: true,
      },
      {
        filename: "Busbar-cover-again.ctb",
        path: "Busbar-cover-again.ctb",
        print_time_secs: 3600,
        can_be_printed: true,
      },
      {
        filename: "LittleBBC.ctb",
        path: "LittleBBC.ctb",
        print_time_secs: 3600,
        can_be_printed: true,
      },
      {
        filename: "random_file.txt",
        path: "random_file.txt",
        can_be_printed: false,
      },
    ],
  });
  return <FileList />;
};

export const Default = Template.bind({});
