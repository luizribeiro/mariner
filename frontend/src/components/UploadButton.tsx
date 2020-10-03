import Button from "@material-ui/core/Button";
import CircularProgress from "@material-ui/core/CircularProgress";
import { createStyles, WithStyles, withStyles } from "@material-ui/core/styles";
import PublishIcon from "@material-ui/icons/Publish";
import axios from "axios";
import nullthrows from "nullthrows";
import React from "react";
import { setState } from "../utils";

const styles = () =>
  createStyles({
    input: {
      display: "none",
    },
  });

export interface UploadButtonProps extends WithStyles {
  onUploadFinished: () => void;
}

interface UploadButtonState {
  isUploading: boolean;
}

class UploadButton extends React.Component<
  UploadButtonProps,
  UploadButtonState
> {
  state: UploadButtonState = { isUploading: false };
  uploadButtonRef: React.RefObject<HTMLInputElement> = React.createRef<
    HTMLInputElement
  >();

  async _onUploadStart(): Promise<void> {
    const files = nullthrows(this.uploadButtonRef.current?.files);
    const formData = new FormData();
    formData.append("file", files[0]);

    await setState(this, { isUploading: true });
    await axios.post("api/upload_file", formData);
    await setState(this, { isUploading: false });

    this.props.onUploadFinished();
  }

  render(): React.ReactElement {
    const { classes } = this.props;
    const { isUploading } = this.state;

    return (
      <React.Fragment>
        <input
          ref={this.uploadButtonRef}
          accept=".ctb"
          className={classes.input}
          id="upload-button"
          multiple
          type="file"
          onChange={async () => await this._onUploadStart()}
          disabled={isUploading}
        />
        <label htmlFor="upload-button">
          <Button
            startIcon={
              isUploading ? <CircularProgress size={18} /> : <PublishIcon />
            }
            variant="outlined"
            color="primary"
            component="span"
            disabled={isUploading}
          >
            Upload
          </Button>
        </label>
      </React.Fragment>
    );
  }
}

export default withStyles(styles)(UploadButton);
