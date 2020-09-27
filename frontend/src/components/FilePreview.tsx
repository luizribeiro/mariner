import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from "@material-ui/core/styles";
import React from "react";

const useStyles = makeStyles({
  root: {
    background: "#5a5a5a",
    paddingTop: "calc(3 / 4 * 100%)",
    position: "relative",
  },
  image: {
    width: "100%",
    height: "100%",
    position: "absolute",
    top: 0,
    left: 0,
  },
  iconContainer: {
    width: "100%",
    height: "100%",
    position: "absolute",
    top: 0,
    left: 0,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
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
    <div className={classes.root}>
      <div className={classes.iconContainer}>
        <CircularProgress
          style={{ color: "#aaa", display: progressDisplay }}
          size={60}
        />
      </div>
      <img
        className={classes.image}
        src={src}
        onLoad={() => setProgressDisplay("none")}
      />
    </div>
  );
}
