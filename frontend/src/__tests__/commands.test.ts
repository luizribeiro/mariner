import "@babel/polyfill";
import axios from "axios";
import MockAdapter from "axios-mock-adapter";
import {
  cancelPrint,
  pausePrint,
  rebootPrinter,
  resumePrint,
  startPrint,
} from "../commands";

const axiosMock = new MockAdapter(axios);

describe("commands.startPrint", () => {
  axiosMock.reset();

  test("it should send an API request", async () => {
    axiosMock
      .onPost("api/printer/command/start_print")
      .reply(200, { success: true });
    await startPrint("monster.ctb");
    expect(axiosMock.history.post.length).toBe(1);
    expect(axiosMock.history.post[0].params).toEqual({
      filename: "monster.ctb",
    });
  });
});

describe("commands.cancelPrint", () => {
  axiosMock.reset();

  test("it should send an API request", async () => {
    axiosMock
      .onPost("api/printer/command/cancel_print")
      .reply(200, { success: true });
    await cancelPrint();
  });
});

describe("commands.cancelPrint", () => {
  axiosMock.reset();

  test("it should send an API request", async () => {
    axiosMock
      .onPost("api/printer/command/cancel_print")
      .reply(200, { success: true });
    await cancelPrint();
  });
});

describe("commands.pausePrint", () => {
  axiosMock.reset();

  test("it should send an API request", async () => {
    axiosMock
      .onPost("api/printer/command/pause_print")
      .reply(200, { success: true });
    await pausePrint();
  });
});

describe("commands.resumePrint", () => {
  axiosMock.reset();

  test("it should send an API request", async () => {
    axiosMock
      .onPost("api/printer/command/resume_print")
      .reply(200, { success: true });
    await resumePrint();
  });
});

describe("commands.rebootPrinter", () => {
  axiosMock.reset();

  test("it should send an API request", async () => {
    axiosMock
      .onPost("api/printer/command/reboot")
      .reply(200, { success: true });
    await rebootPrinter();
  });
});
