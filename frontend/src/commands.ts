import axios, { AxiosResponse } from "axios";

interface CommandAPIResponse {
  success: boolean;
}

export async function startPrint(filename: string): Promise<void> {
  const _response: AxiosResponse<CommandAPIResponse> = await axios.post(
    "api/printer/command/start_print",
    null,
    { params: { filename } }
  );
}

export async function deleteFile(filename: string): Promise<void> {
  const _response: AxiosResponse<CommandAPIResponse> = await axios.post(
    "api/delete_file",
    null,
    { params: { filename } }
  );
}

export async function cancelPrint(): Promise<void> {
  const _response: AxiosResponse<CommandAPIResponse> = await axios.post(
    "api/printer/command/cancel_print"
  );
}

export async function pausePrint(): Promise<void> {
  const _response: AxiosResponse<CommandAPIResponse> = await axios.post(
    "api/printer/command/pause_print"
  );
}

export async function resumePrint(): Promise<void> {
  const _response: AxiosResponse<CommandAPIResponse> = await axios.post(
    "api/printer/command/resume_print"
  );
}

export async function rebootPrinter(): Promise<void> {
  const _response: AxiosResponse<CommandAPIResponse> = await axios.post(
    "api/printer/command/reboot"
  );
}
