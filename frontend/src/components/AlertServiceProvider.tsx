import React from "react";
import { Subtract } from "utility-types";
import { AlertDialog, AlertOptions } from "./AlertDialog";

const AlertServiceContext = React.createContext<
  (options: AlertOptions) => Promise<void>
>(Promise.resolve);

export type AlertFunction = (options: AlertOptions) => Promise<void>;

export const useAlert = (): AlertFunction =>
  React.useContext(AlertServiceContext);

export interface WithAlertProps {
  alertDialog: AlertFunction;
}

export const withAlert = <Props extends WithAlertProps>(
  Component: React.ComponentType<Props>
): ((props: Subtract<Props, WithAlertProps>) => React.ReactElement) => {
  const WithAlert = (
    props: Subtract<Props, WithAlertProps>
  ): React.ReactElement => {
    const alertDialog = useAlert();
    return <Component {...(props as Props)} alertDialog={alertDialog} />;
  };
  return WithAlert;
};

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
