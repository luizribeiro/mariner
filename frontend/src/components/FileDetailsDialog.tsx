import Button from "@material-ui/core/Button";
import CircularProgress from "@material-ui/core/CircularProgress";
import Dialog, { DialogProps } from "@material-ui/core/Dialog";
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
import FilePreview from "./FilePreview";

interface FileDetailsAPIResponse {
  filename: string;
  bed_size_mm: [number, number, number];
  height_mm: number;
  layer_count: number;
  layer_height_mm: number;
  resolution: [number, number];
  print_time_secs: number;
}

interface FileDetailsProps {
  filename: string;
}

interface FileDetailsState {
  isLoading: boolean;
  data?: FileDetailsAPIResponse;
}

class FileDetails extends React.Component<FileDetailsProps, FileDetailsState> {
  state: FileDetailsState = {
    isLoading: true,
  };

  async componentDidMount(): Promise<void> {
    const response: AxiosResponse<FileDetailsAPIResponse> = await axios.get(
      "api/file_details",
      { params: { filename: this.props.filename } }
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
    const imgURL = `api/file_preview?filename=${data.filename}`;

    return (
      <React.Fragment>
        <FilePreview src={imgURL} />
        <Table>
          <TableBody>
            {this._getTableContent(data).map((row) => (
              <TableRow key={row[0]}>
                <TableCell>
                  <b>{row[0]}</b>
                </TableCell>
                <TableCell align="right">{row[1]}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </React.Fragment>
    );
  }
}

export default function FileDetailsDialog(
  props: {
    filename: string;
    onCancel: () => void;
    onPrint: () => void;
  } & DialogProps
): React.ReactElement {
  return (
    <Dialog {...props}>
      <DialogTitle>{props.filename}</DialogTitle>
      <DialogContent dividers>
        <FileDetails filename={props.filename} />
      </DialogContent>
      <DialogActions>
        <Button onClick={props.onCancel} color="primary">
          Cancel
        </Button>
        <Button onClick={props.onPrint} color="primary">
          Print
        </Button>
      </DialogActions>
    </Dialog>
  );
}
