import Box from "@material-ui/core/Box";
import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from "@material-ui/core/styles";
import React from "react";

const useStyles = makeStyles({
  root: {
    background: "#5a5a5a",
    width: 400,
    height: 300,
  },
});

export default function FilePreview({
  src,
}: {
  src: string;
}): React.ReactElement {
  const classes = useStyles();
  const [progressDisplay, setProgressDisplay] = React.useState("block");

  return (
    <Box
      display="flex"
      alignItems="center"
      justifyContent="center"
      className={classes.root}
    >
      <CircularProgress
        style={{ color: "#aaa", display: progressDisplay }}
        size={60}
      />
      <img src={src} onLoad={() => setProgressDisplay("none")} />
    </Box>
  );
}
