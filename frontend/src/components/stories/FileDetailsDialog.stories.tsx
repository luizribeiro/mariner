import Button from "@material-ui/core/Button";
import { Story } from "@storybook/react";
import axios from "axios";
import MockAdapter from "axios-mock-adapter";
import React from "react";
import FileDetailsDialog from "../FileDetailsDialog";

const axiosMock = new MockAdapter(axios);

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

  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
      <Button onClick={handleClickOpen}>Open</Button>
      <FileDetailsDialog
        filename="stairs.ctb"
        onCancel={handleClose}
        onClose={handleClose}
        onPrint={handleClose}
        open={open}
        scroll="paper"
      />
    </div>
  );
};

export const Default = Template.bind({});

export const Loading = (): React.ReactElement => {
  axiosMock.onGet("api/file_details").abortRequest();

  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
      <Button onClick={handleClickOpen}>Open</Button>
      <FileDetailsDialog
        filename="stairs.ctb"
        onCancel={handleClose}
        onClose={handleClose}
        onPrint={handleClose}
        open={open}
        scroll="paper"
      />
    </div>
  );
};
