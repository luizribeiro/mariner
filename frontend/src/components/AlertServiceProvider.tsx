import React from "react";
import { AlertDialog, AlertOptions } from "./AlertDialog";

const AlertServiceContext = React.createContext<
  (options: AlertOptions) => Promise<void>
>(Promise.resolve);

export const useAlert = (): ((options: AlertOptions) => Promise<void>) =>
  React.useContext(AlertServiceContext);

export const AlertServiceProvider = ({
  children,
}: {
  children: React.ReactNode;
}): React.ReactElement => {
  const [alertState, setAlertState] = React.useState<AlertOptions | null>(null);

  const awaitingPromiseRef = React.useRef<{
    resolve: () => void;
  }>();

  const openAlert = (options: AlertOptions) => {
    setAlertState(options);
    return new Promise<void>((resolve) => {
      awaitingPromiseRef.current = { resolve };
    });
  };

  const handleClose = () => {
    if (awaitingPromiseRef.current) {
      awaitingPromiseRef.current.resolve();
    }
    setAlertState(null);
  };

  return (
    <React.Fragment>
      <AlertServiceContext.Provider value={openAlert}>
        {children}
      </AlertServiceContext.Provider>
      <AlertDialog
        open={Boolean(alertState)}
        onClose={handleClose}
        title={alertState?.title || ""}
        description={alertState?.description || ""}
        traceback={alertState?.traceback}
      />
    </React.Fragment>
  );
};
