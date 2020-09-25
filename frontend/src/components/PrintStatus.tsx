import Box from "@material-ui/core/Box";
import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Grid from "@material-ui/core/Grid";
import LinearProgress from "@material-ui/core/LinearProgress";
import { createStyles, WithStyles, withStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import CheckIcon from "@material-ui/icons/Check";
import FolderIcon from "@material-ui/icons/Folder";
import PauseIcon from "@material-ui/icons/Pause";
import PlayArrowIcon from "@material-ui/icons/PlayArrow";
import StopIcon from "@material-ui/icons/Stop";
import axios, { AxiosResponse } from "axios";
import nullthrows from "nullthrows";
import React from "react";
import { Link } from "react-router-dom";
import { cancelPrint, pausePrint, resumePrint } from "../commands";

const styles = () =>
  createStyles({
    root: {
      minWidth: 100,
      maxWidth: 400,
    },
    title: {
      fontSize: 16,
      fontWeight: "bold",
      paddingBottom: 12,
    },
    playButton: {
      padding: 6,
    },
    playIcon: {
      height: 38,
      width: 38,
    },
    gridRoot: {
      flexGrow: 1,
      padding: 12,
      paddingTop: 20,
      paddingBottom: 20,
      textAlign: "center",
    },
  });

type PrinterState = "IDLE" | "STARTING_PRINT" | "PRINTING" | "PAUSED";

function toPrinterState(state: string): PrinterState {
  if (
    state !== "IDLE" &&
    state !== "STARTING_PRINT" &&
    state !== "PRINTING" &&
    state !== "PAUSED"
  ) {
    throw Error("Unknown printer state " + state);
  }
  return state;
}

export interface PrintStatusState {
  isLoading: boolean;
  data?: {
    state: PrinterState;
    selectedFile: string;
    progress: number;
    currentLayer?: number;
    layerCount?: number;
    printTimeSecs?: number;
  };
}

interface PrintStatusAPIResponse {
  state: string;
  selected_file: string;
  progress: number;
  current_layer?: number;
  layer_count?: number;
  print_time_secs?: number;
}

class PrintStatus extends React.Component<
  WithStyles<typeof styles>,
  PrintStatusState
> {
  state: PrintStatusState = {
    isLoading: true,
  };

  async componentDidMount(): Promise<void> {
    const response: AxiosResponse<PrintStatusAPIResponse> = await axios.get(
      "api/print_status"
    );
    this.setState({
      isLoading: false,
      data: {
        state: toPrinterState(response.data.state),
        progress: response.data.progress,
        selectedFile: response.data.selected_file,
        currentLayer: response.data.current_layer,
        layerCount: response.data.layer_count,
        printTimeSecs: response.data.print_time_secs,
      },
    });
  }

  _renderButtons(): React.ReactElement | null {
    const { state } = nullthrows(this.state.data);
    if (state === "IDLE") {
      return null;
    }

    return (
      <Grid
        container
        direction="row"
        justify="center"
        alignItems="center"
        spacing={3}
      >
        <Grid item>
          <Button
            variant="contained"
            color="primary"
            size="small"
            startIcon={<PlayArrowIcon />}
            onClick={async () => await resumePrint()}
            disabled={state !== "PAUSED"}
          >
            Resume
          </Button>
        </Grid>
        <Grid item>
          <Button
            variant="outlined"
            color="primary"
            size="small"
            startIcon={<PauseIcon />}
            onClick={async () => await pausePrint()}
            disabled={state === "PAUSED" || state === "STARTING_PRINT"}
          >
            Pause
          </Button>
        </Grid>
        <Grid item>
          <Button
            variant="outlined"
            color="primary"
            size="small"
            startIcon={<StopIcon />}
            onClick={async () => await cancelPrint()}
          >
            Stop
          </Button>
        </Grid>
      </Grid>
    );
  }

  render(): React.ReactElement | null {
    const { classes } = this.props;

    if (this.state.isLoading) {
      return null;
    }

    const {
      state,
      progress,
      selectedFile,
      layerCount,
      currentLayer,
    } = nullthrows(this.state.data);

    let content: React.ReactElement;
    if (state === "IDLE") {
      content = (
        <Box>
          <Typography variant="h5" gutterBottom>
            <Grid
              container
              direction="row"
              justify="center"
              alignItems="center"
              spacing={1}
            >
              <Grid item>
                <CheckIcon fontSize="large" />
              </Grid>
              <Grid item>Ready</Grid>
            </Grid>
          </Typography>
          <Grid
            container
            alignItems="flex-start"
            justify="flex-end"
            direction="row"
          >
            <Button
              variant="outlined"
              color="primary"
              size="small"
              startIcon={<FolderIcon />}
              component={Link}
              to="/files"
            >
              Files
            </Button>
          </Grid>
        </Box>
      );
    } else {
      content = (
        <React.Fragment>
          <Box display="flex">
            <Box width="100%">
              <Typography component="h6" variant="h6" color="textSecondary">
                {selectedFile}
              </Typography>
              <Box display="flex" alignItems="center">
                <Box width="100%" mr={1}>
                  <LinearProgress variant="determinate" value={progress} />
                </Box>
                <Box minWidth={35}>
                  <Typography variant="body2" color="textSecondary">
                    {`${Math.round(progress)}%`}
                  </Typography>
                </Box>
              </Box>
            </Box>
          </Box>

          <div className={classes.gridRoot}>
            <Grid container spacing={3}>
              <Grid item xs={6}>
                <Typography variant="h5" color="textPrimary" display="inline">
                  2h44&nbsp;
                </Typography>
                <Typography
                  variant="body1"
                  color="textSecondary"
                  display="inline"
                >
                  left
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="h5" color="textPrimary" display="inline">
                  {currentLayer}
                </Typography>
                <Typography variant="h6" color="textPrimary" display="inline">
                  /{layerCount}&nbsp;
                </Typography>
                <Typography
                  variant="body1"
                  color="textSecondary"
                  display="inline"
                >
                  layers
                </Typography>
              </Grid>
            </Grid>
          </div>

          {this._renderButtons()}
        </React.Fragment>
      );
    }

    return (
      <Card className={classes.root}>
        <CardContent>
          <Typography
            className={classes.title}
            color="textPrimary"
            gutterBottom
          >
            Elegoo Mars Pro
          </Typography>
          {content}
        </CardContent>
      </Card>
    );
  }
}

export default withStyles(styles)(PrintStatus);
