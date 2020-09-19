import React from "react";
import { Story } from "@storybook/react";

import PrintStatus from "../components/PrintStatus";

import type { PrintStatusProps } from "../components/PrintStatus";

export default {
  title: "Example/PrintStatus",
  component: PrintStatus,
  argTypes: {
    progress: { control: { type: "number", min: 0, max: 100 } },
  },
};

const Template: Story<PrintStatusProps> = (args: PrintStatusProps) => (
  <PrintStatus {...args} />
);

export const Primary = Template.bind({});
Primary.args = {
  progress: 20.0,
};
