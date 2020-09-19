import Box from "@material-ui/core/Box";
import IconButton from "@material-ui/core/IconButton";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import LinearProgress from "@material-ui/core/LinearProgress";
import Grid from "@material-ui/core/Grid";
import PlayArrowIcon from "@material-ui/icons/PlayArrow";
import React from "react";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles({
  root: {
    minWidth: 100,
    maxWidth: 400,
  },
  title: {
    fontSize: 16,
    fontWeight: "bold",
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
    paddingBottom: 12,
    textAlign: "center",
  },
});

export default function PrintStatus(props: {
  progress: number;
}): React.ReactElement {
  const classes = useStyles();
  const { progress } = props;

  return (
    <Card className={classes.root}>
      <CardContent>
        <Typography className={classes.title} color="textPrimary" gutterBottom>
          Elegoo Mars Pro
        </Typography>
        <Box display="flex">
          <Box paddingRight={1}>
            <IconButton className={classes.playButton} aria-label="play/pause">
              <PlayArrowIcon className={classes.playIcon} />
            </IconButton>
          </Box>
          <Box width="100%">
            <Typography component="h6" variant="h6" color="textSecondary">
              lattice.ctb
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
              <Typography variant="h4" color="textPrimary" display="inline">
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
              <Typography variant="h4" color="textPrimary" display="inline">
                53
              </Typography>
              <Typography variant="h5" color="textPrimary" display="inline">
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
