import Avatar from "@material-ui/core/Avatar";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import ListItemText from "@material-ui/core/ListItemText";
import LayersIcon from "@material-ui/icons/Layers";
import axios, { AxiosResponse } from "axios";
import nullthrows from "nullthrows";
import React from "react";
import { useHistory } from "react-router-dom";
import { startPrint } from "../commands";
import { renderTime } from "../utils";
import FileDetailsDialog from "./FileDetailsDialog";

interface FileAPIResponse {
  filename: string;
  print_time_secs: number;
}

function FileListItem({ file }: { file: FileAPIResponse }): React.ReactElement {
  const [open, setOpen] = React.useState(false);
  const handleClickOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const printTime = renderTime(file.print_time_secs);
  const history = useHistory();
  return (
    <ListItem button key={file.filename} onClick={handleClickOpen}>
      <ListItemAvatar>
        <Avatar>
          <LayersIcon />
        </Avatar>
      </ListItemAvatar>
      <ListItemText primary={file.filename} secondary={printTime} />
      <FileDetailsDialog
        filename={file.filename}
        onCancel={handleClose}
        onClose={handleClose}
        onPrint={async () => {
          await startPrint(file.filename);
          setOpen(false);
          history.push("/");
        }}
        open={open}
        scroll="paper"
      />
    </ListItem>
  );
}

interface FileListAPIResponse {
  files: [FileAPIResponse];
}

export interface FileListState {
  isLoading: boolean;
  data?: FileListAPIResponse;
}

export default class FileList extends React.Component<{}, FileListState> {
  state: FileListState = {
    isLoading: true,
  };

  async componentDidMount(): Promise<void> {
    const response: AxiosResponse<FileListAPIResponse> = await axios.get(
      "api/list_files"
    );
    this.setState({
      isLoading: false,
      data: response.data,
    });
  }

  render(): React.ReactElement | null {
    if (this.state.isLoading) {
      return null;
    }

    const { files } = nullthrows(this.state.data);
    const listItems = files.map((file) => (
      <FileListItem file={file} key={file.filename} />
    ));

    return (
      <Card>
        <CardContent>
          <List>{listItems}</List>
        </CardContent>
      </Card>
    );
  }
}
