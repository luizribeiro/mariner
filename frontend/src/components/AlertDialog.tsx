import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Typography,
} from "@material-ui/core";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import React from "react";

export interface AlertOptions {
  title: string;
  description: string;
  traceback?: string;
}

interface AlertDialogProps extends AlertOptions {
  open: boolean;
  onClose: () => void;
}

export const AlertDialog: React.FC<AlertDialogProps> = ({
  open,
  title,
  description,
  traceback,
  onClose,
}: AlertDialogProps) => {
  const details = traceback ? (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Typography variant="subtitle2">Details</Typography>
      </AccordionSummary>
      <AccordionDetails>
        <Box
          fontFamily="Monospace"
          whiteSpace="pre"
          overflow="scroll"
          border={1}
          borderRadius={4}
          borderColor="#ededed"
          padding={1}
          bgcolor="#fafafa"
        >
          {traceback}
        </Box>
      </AccordionDetails>
    </Accordion>
  ) : null;

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <DialogContentText>{description}</DialogContentText>
        {details}
      </DialogContent>
      <DialogActions>
        <Button color="primary" onClick={onClose} autoFocus>
          OK
        </Button>
      </DialogActions>
    </Dialog>
  );
};
