import axios, { AxiosError, AxiosResponse } from "axios";
import React from "react";
import { Subtract } from "utility-types";
import { AlertFunction, useAlert } from "./components/AlertServiceProvider";

export interface CommandAPIResponse {
  success: boolean;
}

export interface PrintStatusAPIResponse {
  state: string;
  selected_file: string;
  progress: number;
  current_layer?: number;
  layer_count?: number;
  print_time_secs?: number;
  time_left_secs?: number;
}

export interface DirectoryAPIResponse {
  dirname: string;
}

export interface FileAPIResponse {
  filename: string;
  path: string;
  print_time_secs?: number;
  can_be_printed: boolean;
}

export interface FileListAPIResponse {
  directories: [DirectoryAPIResponse];
  files: [FileAPIResponse];
}

export interface FileDetailsAPIResponse {
  filename: string;
  path: string;
  bed_size_mm: [number, number, number];
  height_mm: number;
  layer_count: number;
  layer_height_mm: number;
  resolution: [number, number];
  print_time_secs: number;
}

function isAxiosError(error: Error): error is AxiosError {
  return (error as AxiosError).isAxiosError !== undefined;
}

export class API {
  _alertFn?: AlertFunction;

  async printStatus(): Promise<PrintStatusAPIResponse | undefined> {
    try {
      const response: AxiosResponse<PrintStatusAPIResponse> = await axios.get(
        "api/print_status"
      );
      return response.data;
    } catch (error) {
      this._handleError(error);
    }
  }

  async listFiles(path: string): Promise<FileListAPIResponse | undefined> {
    try {
      const response: AxiosResponse<FileListAPIResponse> = await axios.get(
        `api/list_files?path=${path}`
      );
      return response.data;
    } catch (error) {
      this._handleError(error);
    }
  }

  async fileDetails(path: string): Promise<FileDetailsAPIResponse | undefined> {
    try {
      const response: AxiosResponse<FileDetailsAPIResponse> = await axios.get(
        "api/file_details",
        { params: { filename: path } }
      );
      return response.data;
    } catch (error) {
      this._handleError(error);
    }
  }

  async uploadFile(
    file: File,
    progress: (event: ProgressEvent) => void
  ): Promise<CommandAPIResponse | undefined> {
    try {
      const formData = new FormData();
      formData.append("file", file);
      const response: AxiosResponse<CommandAPIResponse> = await axios.post(
        "api/upload_file",
        formData,
        { onUploadProgress: progress }
      );
      return response.data;
    } catch (error) {
      this._handleError(error);
    }
  }

  async startPrint(filename: string): Promise<CommandAPIResponse | undefined> {
    try {
      const response: AxiosResponse<CommandAPIResponse> = await axios.post(
        "api/printer/command/start_print",
        null,
        { params: { filename } }
      );
      return response.data;
    } catch (error) {
      this._handleError(error);
    }
  }

  async deleteFile(filename: string): Promise<CommandAPIResponse | undefined> {
    try {
      const response: AxiosResponse<CommandAPIResponse> = await axios.post(
        "api/delete_file",
        null,
        { params: { filename } }
      );
      return response.data;
    } catch (error) {
      this._handleError(error);
    }
  }

  async cancelPrint(): Promise<CommandAPIResponse | undefined> {
    try {
      const response: AxiosResponse<CommandAPIResponse> = await axios.post(
        "api/printer/command/cancel_print"
      );
      return response.data;
    } catch (error) {
      this._handleError(error);
    }
  }

  async pausePrint(): Promise<CommandAPIResponse | undefined> {
    try {
      const response: AxiosResponse<CommandAPIResponse> = await axios.post(
        "api/printer/command/pause_print"
      );
      return response.data;
    } catch (error) {
      this._handleError(error);
    }
  }

  async resumePrint(): Promise<CommandAPIResponse | undefined> {
    try {
      const response: AxiosResponse<CommandAPIResponse> = await axios.post(
        "api/printer/command/resume_print"
      );
      return response.data;
    } catch (error) {
      this._handleError(error);
    }
  }

  async rebootPrinter(): Promise<CommandAPIResponse | undefined> {
    try {
      const response: AxiosResponse<CommandAPIResponse> = await axios.post(
        "api/printer/command/reboot"
      );
      return response.data;
    } catch (error) {
      this._handleError(error);
    }
  }

  async _handleError(error: Error): Promise<void> {
    if (!this._alertFn) {
      throw error;
    }

    if (isAxiosError(error)) {
      if (error.response && error.response.data instanceof Object) {
        await this._alertFn({
          title: error.response.data.title,
          description: error.response.data.description,
          traceback: error.response.data.traceback,
        });
      } else if (error.response) {
        await this._alertFn({
          title: "Something went wrong",
          description: `The server replied with a ${error.response.status} HTTP status code.`,
        });
      } else {
        await this._alertFn({
          title: "Something went wrong",
          description: "Sorry, I don't know what happened.",
        });
      }
    } else {
      throw error;
    }
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
    api._alertFn = useAlert();
    return <Component {...(props as Props)} api={api} />;
  };
  return WithAPI;
};

export const useAPI = (): API => {
  const api = new API();
  api._alertFn = useAlert();
  return api;
};
