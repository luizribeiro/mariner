import Button from "@material-ui/core/Button";
import CircularProgress from "@material-ui/core/CircularProgress";
import { createStyles, WithStyles, withStyles } from "@material-ui/core/styles";
import PublishIcon from "@material-ui/icons/Publish";
import nullthrows from "nullthrows";
import React from "react";
import { withAPI, WithAPIProps } from "../api";
import { getSupportedExtensions, setState } from "../utils";

const styles = () =>
  createStyles({
    input: {
      display: "none",
    },
  });

export interface UploadButtonProps extends WithStyles, WithAPIProps {
  onUploadFinished: () => void;
}

interface UploadButtonState {
  isUploading: boolean;
  uploadProgress: number;
}

class UploadButton extends React.Component<
  UploadButtonProps,
  UploadButtonState
> {
  state: UploadButtonState = { isUploading: false, uploadProgress: 0 };
  uploadButtonRef: React.RefObject<HTMLInputElement> =
    React.createRef<HTMLInputElement>();

  async _onUploadStart(): Promise<void> {
    const files = nullthrows(this.uploadButtonRef.current?.files);

    await setState(this, { isUploading: true, uploadProgress: 0 });
    await this.props.api.uploadFile(files[0], (event: ProgressEvent) => {
      this.setState({
        uploadProgress: (event.loaded / event.total) * 100,
      });
    });
    await setState(this, { isUploading: false, uploadProgress: 0 });

    await this.props.onUploadFinished();
  }

  render(): React.ReactElement {
    const { classes } = this.props;
    const { isUploading, uploadProgress } = this.state;

    return (
      <React.Fragment>
        <input
          ref={this.uploadButtonRef}
          accept={getSupportedExtensions()}
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
              isUploading ? (
                <CircularProgress
                  variant="determinate"
                  value={uploadProgress}
                  size={18}
                />
              ) : (
                <PublishIcon />
              )
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

export default withStyles(styles)(withAPI(UploadButton));
