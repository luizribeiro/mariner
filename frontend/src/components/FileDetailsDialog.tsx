import Button from "@material-ui/core/Button";
import CircularProgress from "@material-ui/core/CircularProgress";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogTitle from "@material-ui/core/DialogTitle";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableRow from "@material-ui/core/TableRow";
import axios, { AxiosResponse } from "axios";
import nullthrows from "nullthrows";
import React from "react";
import { renderTime } from "../utils";

interface FileDetailsAPIResponse {
  filename: string;
  bed_size_mm: [number, number, number];
  height_mm: number;
  layer_count: number;
  layer_height_mm: number;
  resolution: [number, number];
  print_time_secs: number;
}

interface FileDetailsState {
  isLoading: boolean;
  data?: FileDetailsAPIResponse;
}

class FileDetails extends React.Component<{}, FileDetailsState> {
  state: FileDetailsState = {
    isLoading: true,
  };

  async componentDidMount(): Promise<void> {
    const response: AxiosResponse<FileDetailsAPIResponse> = await axios.get(
      "api/file_details"
    );
    this.setState({
      isLoading: false,
      data: response.data,
    });
  }

  _getTableContent(data: FileDetailsAPIResponse): Array<[string, string]> {
    return [
      ["Print Time", renderTime(data.print_time_secs)],
      ["Height", `${data.height_mm}mm`],
      ["Layer Count", data.layer_count.toString()],
      ["Layer Height", `${data.layer_height_mm}mm`],
      ["Resolution", data.resolution.join(" x ")],
      ["Bed Size", data.bed_size_mm.map((d) => `${d}mm`).join(" x ")],
    ];
  }

  render(): React.ReactElement {
    if (this.state.isLoading) {
      return <CircularProgress />;
    }

    const data = nullthrows(this.state.data);

    return (
      <Table>
        <TableBody>
          {this._getTableContent(data).map((row) => (
            <TableRow key={row[0]}>
              <TableCell>{row[0]}</TableCell>
              <TableCell align="right">{row[1]}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    );
  }
}

export default function FileDetailsDialog({
  filename,
}: {
  filename: string;
}): React.ReactElement {
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
      <Button onClick={handleClickOpen()}>Open</Button>
      <Dialog
        open={open}
        onClose={handleClose}
        scroll="paper"
        aria-labelledby="scroll-dialog-title"
        aria-describedby="scroll-dialog-description"
      >
        <DialogTitle id="scroll-dialog-title">{filename}</DialogTitle>
        <DialogContent dividers>
          <FileDetails />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
          <Button onClick={handleClose} color="primary">
            Print
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
