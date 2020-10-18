import Box from "@material-ui/core/Box";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardHeader from "@material-ui/core/CardHeader";
import CircularProgress from "@material-ui/core/CircularProgress";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import { createStyles, WithStyles, withStyles } from "@material-ui/core/styles";
import FolderIcon from "@material-ui/icons/Folder";
import InsertDriveFileIcon from "@material-ui/icons/InsertDriveFile";
import LayersIcon from "@material-ui/icons/Layers";
import nullthrows from "nullthrows";
import React from "react";
import { useHistory } from "react-router-dom";
import {
  DirectoryAPIResponse,
  FileAPIResponse,
  FileListAPIResponse,
  useAPI,
  withAPI,
  WithAPIProps,
} from "../api";
import { renderTime, sleep } from "../utils";
import FileDetailsDialog from "./FileDetailsDialog";
import UploadButton from "./UploadButton";

function DirectoryListItem({
  directory,
  onSelect,
}: {
  directory: DirectoryAPIResponse;
  onSelect: (dirname: string) => void;
}): React.ReactElement {
  return (
    <React.Fragment>
      <ListItem
        button
        key={directory.dirname}
        onClick={() => onSelect(directory.dirname)}
      >
        <ListItemIcon>
          <FolderIcon />
        </ListItemIcon>
        <ListItemText primary={directory.dirname} />
      </ListItem>
    </React.Fragment>
  );
}

function FileListItem({
  file,
  onDelete,
}: {
  file: FileAPIResponse;
  onDelete: () => void;
}): React.ReactElement {
  const [open, setOpen] = React.useState(false);
  const handleClickOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const printTime = file.print_time_secs
    ? renderTime(file.print_time_secs)
    : null;
  const history = useHistory();
  const api = useAPI();
  return (
    <React.Fragment>
      <ListItem button key={file.filename} onClick={handleClickOpen}>
        <ListItemIcon>
          {file.can_be_printed ? <LayersIcon /> : <InsertDriveFileIcon />}
        </ListItemIcon>
        <ListItemText primary={file.filename} secondary={printTime} />
      </ListItem>
      <FileDetailsDialog
        filename={file.filename}
        canBePrinted={file.can_be_printed}
        path={file.path}
        onCancel={handleClose}
        onClose={handleClose}
        onPrint={async () => {
          await api.startPrint(file.path);
          setOpen(false);
          history.push("/");
        }}
        onDelete={async () => {
          await api.deleteFile(file.path);
          setOpen(false);
          await onDelete();
        }}
        open={open}
        scroll="paper"
      />
    </React.Fragment>
  );
}

export interface FileListState {
  isLoading: boolean;
  path: string;
  data?: FileListAPIResponse;
}

const styles = () =>
  createStyles({
    loadingContainer: {
      flexGrow: 1,
      padding: 18,
      textAlign: "center",
    },
  });

class FileList extends React.Component<
  WithStyles & WithAPIProps,
  FileListState
> {
  state: FileListState = {
    isLoading: true,
    path: "",
  };

  async refresh(): Promise<void> {
    // FIXME: this is kind of nasty, it's just here because FileList sometimes
    // fails to render on storybook, which makes the storyshot tests for this
    // component fail when they run
    await sleep(0);
    const response = await this.props.api.listFiles(this.state.path);
    if (response) {
      this.setState({
        isLoading: false,
        data: response,
      });
    }
  }

  async componentDidMount(): Promise<void> {
    await this.refresh();
  }

  _renderContent(): React.ReactElement {
    if (this.state.isLoading) {
      return (
        <Box className={this.props.classes.loadingContainer}>
          <CircularProgress />
        </Box>
      );
    }

    const { directories, files } = nullthrows(this.state.data);
    const directoryListItems = directories.map((directory) => (
      <DirectoryListItem
        directory={directory}
        key={directory.dirname}
        onSelect={(dirname) =>
          this.setState(
            (state, _props) => ({
              isLoading: true,
              path: `${state.path}${dirname}/`,
              data: undefined,
            }),
            async () => await this.refresh()
          )
        }
      />
    ));
    const fileListItems = files.map((file) => (
      <FileListItem
        file={file}
        key={file.filename}
        onDelete={async () => await this.refresh()}
      />
    ));

    const parentDirectoryItem =
      this.state.path !== "" ? (
        <DirectoryListItem
          directory={{ dirname: ".." }}
          key=".."
          onSelect={(_) =>
            this.setState(
              (state, _props) => ({
                isLoading: true,
                path: state.path.replace(/[^/]+\/$/, ""),
                data: undefined,
              }),
              async () => await this.refresh()
            )
          }
        />
      ) : null;

    return (
      <List>
        {parentDirectoryItem}
        {directoryListItems}
        {fileListItems}
      </List>
    );
  }

  render(): React.ReactElement {
    return (
      <Card>
        <CardHeader
          title="Files"
          subheader={`/${this.state.path}`}
          action={
            <UploadButton onUploadFinished={async () => await this.refresh()} />
          }
        />
        <CardContent>{this._renderContent()}</CardContent>
      </Card>
    );
  }
}

export default withStyles(styles)(withAPI(FileList));
