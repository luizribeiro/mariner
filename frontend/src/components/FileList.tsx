import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import FolderIcon from "@material-ui/icons/Folder";
import LayersIcon from "@material-ui/icons/Layers";
import axios, { AxiosResponse } from "axios";
import nullthrows from "nullthrows";
import React from "react";
import { useHistory } from "react-router-dom";
import { startPrint } from "../commands";
import { renderTime } from "../utils";
import FileDetailsDialog from "./FileDetailsDialog";

interface DirectoryAPIResponse {
  dirname: string;
}

interface FileAPIResponse {
  filename: string;
  path: string;
  print_time_secs: number;
}

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

function FileListItem({ file }: { file: FileAPIResponse }): React.ReactElement {
  const [open, setOpen] = React.useState(false);
  const handleClickOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const printTime = renderTime(file.print_time_secs);
  const history = useHistory();
  return (
    <React.Fragment>
      <ListItem button key={file.filename} onClick={handleClickOpen}>
        <ListItemIcon>
          <LayersIcon />
        </ListItemIcon>
        <ListItemText primary={file.filename} secondary={printTime} />
      </ListItem>
      <FileDetailsDialog
        filename={file.filename}
        path={file.path}
        onCancel={handleClose}
        onClose={handleClose}
        onPrint={async () => {
          await startPrint(file.path);
          setOpen(false);
          history.push("/");
        }}
        open={open}
        scroll="paper"
      />
    </React.Fragment>
  );
}

interface FileListAPIResponse {
  directories: [DirectoryAPIResponse];
  files: [FileAPIResponse];
}

export interface FileListState {
  isLoading: boolean;
  path: string;
  data?: FileListAPIResponse;
}

export default class FileList extends React.Component<{}, FileListState> {
  state: FileListState = {
    isLoading: true,
    path: "",
  };

  async refresh(): Promise<void> {
    const response: AxiosResponse<FileListAPIResponse> = await axios.get(
      `api/list_files?path=${this.state.path}`
    );
    this.setState({
      isLoading: false,
      data: response.data,
    });
  }

  async componentDidMount(): Promise<void> {
    await this.refresh();
  }

  render(): React.ReactElement | null {
    if (this.state.isLoading) {
      return null;
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
      <FileListItem file={file} key={file.filename} />
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
      <Card>
        <CardContent>
          <List>
            {parentDirectoryItem}
            {directoryListItems}
            {fileListItems}
          </List>
        </CardContent>
      </Card>
    );
  }
}
