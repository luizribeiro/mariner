import { Story } from "@storybook/react";
import React from "react";
import FilePreview from "../FilePreview";

export default {
  title: "FilePreview",
  component: FilePreview,
};

const Template: Story = (_args) => {
  return <FilePreview src="" />;
};

export const Default = Template.bind({});
