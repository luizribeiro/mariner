import Box from "@material-ui/core/Box";
import Button from "@material-ui/core/Button";
import CircularProgress from "@material-ui/core/CircularProgress";
import Dialog, { DialogProps } from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import IconButton from "@material-ui/core/IconButton";
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableRow from "@material-ui/core/TableRow";
import Typography from "@material-ui/core/Typography";
import DeleteForeverIcon from "@material-ui/icons/DeleteForever";
import nullthrows from "nullthrows";
import React from "react";
import { FileDetailsAPIResponse, withAPI, WithAPIProps } from "../api";
import { renderTime } from "../utils";
import FilePreview from "./FilePreview";

interface FileDetailsProps extends WithAPIProps {
  filename: string;
  path: string;
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
    const response = await this.props.api.fileDetails(this.props.path);
    if (response) {
      this.setState({
        isLoading: false,
        data: response,
      });
    }
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
      return (
        <CircularProgress
          style={{
            paddingTop: 30,
            paddingBottom: 30,
            paddingLeft: 100,
            paddingRight: 100,
          }}
        />
      );
    }

    const data = nullthrows(this.state.data);
    const imgURL = `api/file_preview?filename=${data.path}`;

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

const useStyles = makeStyles({
  dialogTitle: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  moreOptionsButton: {
    padding: 4,
  },
});

const FileDetailsWithAPI = withAPI(FileDetails);

export default function FileDetailsDialog(
  props: {
    filename: string;
    canBePrinted: boolean;
    path: string;
    onCancel: () => void;
    onPrint: () => void;
    onDelete: () => void;
  } & DialogProps
): React.ReactElement {
  const classes = useStyles();
  const [isDeleteConfirmationDialogOpen, setDeleteConfirmationDialogOpen] =
    React.useState(false);
  const handleDeleteDialogClose = () => setDeleteConfirmationDialogOpen(false);
  const handleDelete = () => {
    setDeleteConfirmationDialogOpen(false);
    props.onDelete();
  };

  let fileDetails: React.ReactElement;
  if (props.canBePrinted) {
    fileDetails = (
      <FileDetailsWithAPI filename={props.filename} path={props.path} />
    );
  } else {
    fileDetails = (
      <Box
        display="flex"
        width={350}
        height={80}
        alignItems="center"
        justifyContent="center"
      >
        <Typography>This file cannot be printed.</Typography>
      </Box>
    );
  }

  return (
    <Dialog {...props}>
      <DialogTitle className={classes.dialogTitle} disableTypography>
        <Typography component="h2" variant="h6">
          {props.filename}
        </Typography>
        <IconButton
          className={classes.moreOptionsButton}
          onClick={() => setDeleteConfirmationDialogOpen(true)}
        >
          <DeleteForeverIcon />
        </IconButton>
        <Dialog
          open={isDeleteConfirmationDialogOpen}
          onClose={handleDeleteDialogClose}
        >
          <DialogContent>
            <DialogContentText>
              Are you sure you want to <b>permanently delete</b> the file{" "}
              <b>{props.filename}</b>?
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button color="primary" onClick={handleDeleteDialogClose} autoFocus>
              Cancel
            </Button>
            <Button color="primary" onClick={handleDelete}>
              Delete
            </Button>
          </DialogActions>
        </Dialog>
      </DialogTitle>
      <DialogContent style={{ padding: 0 }} dividers>
        {fileDetails}
      </DialogContent>
      <DialogActions>
        <Button onClick={props.onCancel} color="primary">
          Cancel
        </Button>
        <Button
          onClick={props.onPrint}
          color="primary"
          disabled={!props.canBePrinted}
        >
          Print
        </Button>
      </DialogActions>
    </Dialog>
  );
}
