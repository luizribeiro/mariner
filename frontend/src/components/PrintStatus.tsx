import Box from "@material-ui/core/Box";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Grid from "@material-ui/core/Grid";
import IconButton from "@material-ui/core/IconButton";
import LinearProgress from "@material-ui/core/LinearProgress";
import { createStyles, WithStyles, withStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import PauseIcon from "@material-ui/icons/Pause";
import PlayArrowIcon from "@material-ui/icons/PlayArrow";
import axios, { AxiosResponse } from "axios";
import nullthrows from "nullthrows";
import React from "react";
import { cancelPrint } from "../commands";

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
      padding: 24,
      paddingBottom: 6,
      textAlign: "center",
    },
  });

export interface PrintStatusState {
  isLoading: boolean;
  data?: {
    isPrinting: boolean;
    selectedFile: string;
    progress: number;
  };
}

interface PrintStatusAPIResponse {
  selected_file: string;
  is_printing: boolean;
  progress: number;
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
        isPrinting: response.data.is_printing,
        progress: response.data.progress,
        selectedFile: response.data.selected_file,
      },
    });
  }

  _renderButton(): React.ReactElement {
    const { classes } = this.props;
    const { isPrinting } = nullthrows(this.state.data);

    const icon = isPrinting ? (
      <PauseIcon className={classes.playIcon} />
    ) : (
      <PlayArrowIcon className={classes.playIcon} />
    );

    return (
      <IconButton
        className={classes.playButton}
        aria-label="play/pause"
        onClick={async () => (isPrinting ? cancelPrint() : null)}
      >
        {icon}
      </IconButton>
    );
  }

  render(): React.ReactElement | null {
    const { classes } = this.props;

    if (this.state.isLoading) {
      return null;
    }

    const { progress, selectedFile } = nullthrows(this.state.data);

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
          <Box display="flex">
            <Box paddingRight={1}>{this._renderButton()}</Box>
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
                  53
                </Typography>
                <Typography variant="h6" color="textPrimary" display="inline">
                  /79&nbsp;
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
        </CardContent>
      </Card>
    );
  }
}

export default withStyles(styles)(PrintStatus);
