import Box from "@material-ui/core/Box";
import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import LinearProgress, {
  LinearProgressProps,
} from "@material-ui/core/LinearProgress";
import Grid from "@material-ui/core/Grid";
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
  gridRoot: {
    flexGrow: 1,
    padding: 24,
    paddingBottom: 12,
    textAlign: "center",
  },
});

export default function PrintStatus(progress: number) {
  const classes = useStyles();

  return (
    <Card className={classes.root}>
      <CardContent>
        <Typography className={classes.title} color="textPrimary" gutterBottom>
          Elegoo Mars Pro
        </Typography>
        <Typography component="h6" variant="h6" color="textSecondary">
          lattice.ctb
        </Typography>
        <Box display="flex" alignItems="center">
          <Box width="100%" mr={1}>
            <LinearProgress variant="determinate" value={20} />
          </Box>
          <Box minWidth={35}>
            <Typography variant="body2" color="textSecondary">
              {`${Math.round(20)}%`}
            </Typography>
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
