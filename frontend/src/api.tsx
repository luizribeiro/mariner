import axios, { AxiosResponse } from "axios";
import React from "react";
import { Subtract } from "utility-types";

interface CommandAPIResponse {
  success: boolean;
}

export class API {
  async startPrint(filename: string): Promise<CommandAPIResponse> {
    const response: AxiosResponse<CommandAPIResponse> = await axios.post(
      "api/printer/command/start_print",
      null,
      { params: { filename } }
    );
    return response.data;
  }

  async deleteFile(filename: string): Promise<CommandAPIResponse> {
    const response: AxiosResponse<CommandAPIResponse> = await axios.post(
      "api/delete_file",
      null,
      { params: { filename } }
    );
    return response.data;
  }

  async cancelPrint(): Promise<CommandAPIResponse> {
    const response: AxiosResponse<CommandAPIResponse> = await axios.post(
      "api/printer/command/cancel_print"
    );
    return response.data;
  }

  async pausePrint(): Promise<CommandAPIResponse> {
    const response: AxiosResponse<CommandAPIResponse> = await axios.post(
      "api/printer/command/pause_print"
    );
    return response.data;
  }

  async resumePrint(): Promise<CommandAPIResponse> {
    const response: AxiosResponse<CommandAPIResponse> = await axios.post(
      "api/printer/command/resume_print"
    );
    return response.data;
  }

  async rebootPrinter(): Promise<CommandAPIResponse> {
    const response: AxiosResponse<CommandAPIResponse> = await axios.post(
      "api/printer/command/reboot"
    );
    return response.data;
  }
}

export interface WithAPIProps {
  api: API;
}

export const withAPI = <Props extends WithAPIProps>(
  Component: React.ComponentType<Props>
): ((props: Subtract<Props, WithAPIProps>) => React.ReactElement) => {
  const WithAPI = (
    props: Subtract<Props, WithAPIProps>
  ): React.ReactElement => {
    const api = new API();
    return <Component {...(props as Props)} api={api} />;
  };
  return WithAPI;
};

export const useAPI = (): API => new API();
