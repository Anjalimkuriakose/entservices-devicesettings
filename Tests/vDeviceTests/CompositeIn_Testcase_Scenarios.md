# CompositeIn Testcase Scenarios

This document describes the CompositeIn testcases `TCID01` through `TCID20` implemented in this directory.
The response sections list expected pass criteria; they are not captured execution logs.

## TCID01_GetInputDevices

Scenario: Validate that `getInputDevices(COMPOSITE)` returns a non-empty list of well-formed devices with unique port IDs.

1. Call `getInputDevices` for `COMPOSITE`.
2. Validate that the call succeeds and returns a non-empty device list.
3. Validate that each device has an `id`, a string `locator`, and a boolean `connected` value.
4. Validate that all device IDs are unique.

Response:

```text
Expected: getInputDevices succeeds with at least one well-formed device.
Expected: All device IDs are unique.
TCID01_GetInputDevices Passed
```

## TCID02_StartStopInput

Scenario: Validate that starting and stopping composite port `0` emits the expected input-status events and that a repeated stop is handled.

1. Register for `onInputStatusChanged`.
2. Call `startInput` for composite port `0`.
3. Validate that the call succeeds and an event for port `0` with status `started` is received.
4. Wait one second.
5. Call `stopInput`.
6. Validate that the call succeeds and an event for port `0` with status `stopped` is received.
7. Call `stopInput` again and validate that the call succeeds.
8. Clean up the input and close the event listener.

Response:

```text
Expected: startInput succeeds and onInputStatusChanged reports started.
Expected: stopInput succeeds and onInputStatusChanged reports stopped.
Expected: A second stopInput succeeds.
TCID02_StartStopInput Passed
```

## TCID03_SetVideoRectangle

Scenario: Validate that full-screen and picture-in-picture video rectangles are accepted while composite input is active.

1. Start composite input on port `0`.
2. Set the full-screen rectangle `(0, 0, 1920, 1080)`.
3. Set a PIP rectangle `(960, 540, 960, 540)`.
4. Move the PIP rectangle to `(100, 100, 640, 360)`.
5. Restore the full-screen rectangle `(0, 0, 1920, 1080)`.
6. Clean up the input.

Response:

```text
Expected: startInput and all four setVideoRectangle calls succeed.
TCID03_SetVideoRectangle Passed
```

## TCID04_StartStopCycle

Scenario: Validate repeatability by completing five start/stop cycles on every enumerated composite port.

1. Enumerate composite ports; use port `0` if the list is unavailable.
2. For each port, perform five cycles of `startInput` followed by `stopInput`.
3. Clean up the input.
4. Re-enumerate the ports when available and validate that the port list is unchanged.

Response:

```text
Expected: Every startInput and stopInput call succeeds for all five cycles on each port.
Expected: The enumerated port list remains unchanged.
TCID04_StartStopCycle Passed
```

## TCID05_PortSwitching

Scenario: Validate direct switching among composite ports without an intervening stop, followed by one stop to release the active port.

1. Enumerate composite ports; use port `0` if the list is unavailable.
2. If fewer than two ports are available, repeat the same port to validate a same-port restart.
3. Call `startInput` for each port in enumeration order, then in reverse order, waiting 0.5 seconds between calls.
4. Call `stopInput` once after the sequence.
5. Clean up the input.

Response:

```text
Expected: Each startInput call succeeds during the forward and reverse sequences.
Expected: The final stopInput succeeds.
TCID05_PortSwitching Passed
```

## TCID06_InvalidPortId

Scenario: Validate that malformed, missing, and out-of-range composite `portId` values are rejected and do not prevent later valid input operations.

1. Call `startInput` with each of these port values: non-numeric `"abc"`, empty string, `-1`, out-of-range `10`, `99999999999`, `0.5`, `null`, and missing `portId`.
2. Call `startInput` with the `params` object missing.
3. Validate that each call receives a response and is rejected with an error.
4. Call `startInput(0)` followed by `stopInput` and validate that both succeed.
5. Clean up the input.

Response:

```text
Expected: Every invalid or missing portId case returns an error response.
Expected: A valid startInput/stopInput sequence succeeds afterwards.
TCID06_InvalidPortId Passed
```

## TCID07_InvalidTypeOfInput

Scenario: Validate response handling and input-type validation across `getInputDevices`, `startInput`, `stopInput`, and `setVideoRectangle`.

1. Test the rejected type values `"ABCD"`, `""`, `"COMPOSITE1"`, and numeric `123`.
2. Test the tolerated type values `"composite"`, `"Composite"`, and `" COMPOSITE"`.
3. For every value, call all four APIs and validate that each call receives a response.
4. For rejected values, validate that `getInputDevices` and `startInput` return errors.
5. Call `startInput` with `typeOfInput` omitted and validate that a response is received.
6. Validate that the plugin remains healthy, then clean up.

Response:

```text
Expected: No tested call hangs or crashes.
Expected: Unknown values are rejected by getInputDevices and startInput.
Expected: The plugin remains healthy after the invalid and tolerated values.
TCID07_InvalidTypeOfInput Passed
```

## TCID08_InvalidRectangle

Scenario: Validate rejection of malformed rectangle fields, response handling for unusual dimensions, and recovery with a valid rectangle.

1. Start composite input on port `0`.
2. Verify rejection of rectangles with missing `x`, missing `w`, all rectangle fields missing, string `x`, string `w`, null `h`, or boolean `y`.
3. Submit rectangles with negative coordinates, negative dimensions, zero dimensions, and floating-point values; validate that each call receives a response.
4. Set the valid rectangle `(0, 0, 1920, 1080)` and validate success.
5. Clean up the input.

Response:

```text
Expected: Each malformed required-field or wrong-type case returns an error.
Expected: Each negative, zero, or floating-point case receives a response.
Expected: The valid rectangle succeeds after the invalid cases.
TCID08_InvalidRectangle Passed
```

## TCID09_StopWithoutStart

Scenario: Validate that repeated `stopInput` calls with no active input are handled and do not prevent a subsequent start.

1. Clean up any active input.
2. Call `stopInput` three times while idle and validate that each call succeeds.
3. Call `startInput` for port `0` and validate success.
4. Clean up the input.

Response:

```text
Expected: All three idle stopInput calls and the subsequent startInput succeed.
TCID09_StopWithoutStart Passed
```

## TCID10_RectangleWithoutActiveInput

Scenario: Validate that `setVideoRectangle` receives a response before input starts and after it stops, without preventing normal active-input operation.

1. Clean up any active input.
2. Call `setVideoRectangle(0, 0, 1920, 1080)` before starting input and validate that a response is received.
3. Start port `0`, then call `stopInput`.
4. Call `setVideoRectangle(0, 0, 1920, 1080)` after the stop and validate that a response is received.
5. Start port `0` again and set the same rectangle while active; validate that both calls succeed.
6. Clean up the input.

Response:

```text
Expected: Rectangle calls outside the active-input state receive responses.
Expected: A subsequent startInput and active setVideoRectangle both succeed.
TCID10_RectangleWithoutActiveInput Passed
```

## TCID11_BoundaryRectangle

Scenario: Validate required small and full-frame rectangles, response handling for off-screen and integer-boundary values, and plugin health afterwards.

1. Start composite input on port `0`.
2. Validate success for rectangles `(0, 0, 1, 1)`, `(0, 0, 1920, 1080)`, and `(0, 0, 3840, 2160)`.
3. Submit the bottom-right `1x1`, partially off-screen, fully off-screen, `INT32_MAX`, and `INT32_MAX+1` rectangle cases; validate that each receives a response.
4. Restore `(0, 0, 1920, 1080)` and validate that the plugin remains healthy.
5. Clean up the input.

Response:

```text
Expected: The 1x1, 1080p, and 4K rectangles succeed.
Expected: Every remaining boundary case receives a response.
Expected: The valid restore rectangle succeeds and the plugin remains healthy.
TCID11_BoundaryRectangle Passed
```

## TCID12_DoubleStartSamePort

Scenario: Validate that starting the same port twice is answered and that one stop releases the port with a `stopped` event.

1. Register for `onInputStatusChanged`.
2. Start composite port `0` and validate success.
3. Start port `0` a second time and validate that the call receives a response.
4. Call `stopInput` and validate success.
5. Validate that an `onInputStatusChanged` event with status `stopped` is received.
6. Clean up the input and close the event listener.

Response:

```text
Expected: Both startInput calls receive responses.
Expected: stopInput succeeds and the stopped event is received.
TCID12_DoubleStartSamePort Passed
```

## TCID13_HdmiCompositeIsolation

Scenario: Validate that stopping HDMI input does not release active composite input and that HDMI enumeration remains unchanged.

1. Read and store the HDMI input-device list.
2. Start composite input on port `0`.
3. Call `stopInput` for HDMI while composite input is active.
4. Set a composite rectangle `(0, 0, 1280, 720)` and validate success.
5. Stop composite input.
6. Read the HDMI input-device list again and validate that it is unchanged.
7. Clean up the input.

Response:

```text
Expected: Composite remains usable after stopInput(HDMI).
Expected: HDMI enumeration matches the list captured before the test.
TCID13_HdmiCompositeIsolation Passed
```

## TCID14_RapidStartStopStress

Scenario: Validate plugin stability during 25 back-to-back composite start, rectangle, and stop iterations without delays.

1. Repeat 25 times: start port `0`, set `(0, 0, 1920, 1080)`, then stop input.
2. Validate that every API call succeeds.
3. Validate that the plugin remains healthy.
4. Clean up the input.

Response:

```text
Expected: All 75 API calls succeed across 25 iterations.
Expected: The plugin remains healthy after the stress sequence.
TCID14_RapidStartStopStress Passed
```

## TCID15_PresentationWorkflow

Scenario: Validate the complete composite presentation workflow from enumeration through start, rectangle changes, stop, and re-enumeration.

1. Enumerate composite ports and validate that at least one port is available.
2. Start the first enumerated port.
3. Set full-screen `(0, 0, 1920, 1080)`, PIP `(1280, 720, 640, 360)`, moved PIP `(0, 0, 640, 360)`, then restore full-screen.
4. Stop input.
5. Call `setVideoRectangle(0, 0, 1920, 1080)` after stop and validate that a response is received.
6. Re-enumerate composite ports and validate that the port list is unchanged.
7. Clean up the input.

Response:

```text
Expected: All active presentation workflow calls succeed.
Expected: The rectangle-after-stop call receives a response and port enumeration is unchanged.
TCID15_PresentationWorkflow Passed
```

## TCID16_ConnectionStatusUpdate

Scenario: Validate that injected composite connect and disconnect changes are reported through `onDevicesChanged` and reflected by `getInputDevices(COMPOSITE)`.

1. Enumerate composite ports; use port `0` if the list is unavailable.
2. Register for `onDevicesChanged`.
3. For each port, inject connected and then disconnected status. Use the connection-status YAML for port `0` when connecting; use inline status updates otherwise.
4. For each injection, validate that `onDevicesChanged` reports the expected state.
5. Query `getInputDevices(COMPOSITE)` and validate that the port's `connected` state matches the injection.
6. Inject disconnected status for each port and close the event listener.

Response:

```text
Expected: Connect and disconnect events are received for every tested port.
Expected: getInputDevices reflects each injected connected state.
TCID16_ConnectionStatusUpdate Passed
```

## TCID17_SignalStatusTransitions

Scenario: Validate ordered `onSignalChanged` notifications for NO_SIGNAL, UNSTABLE, and STABLE composite signal states.

1. Register for `onSignalChanged`.
2. Start composite input on port `0`.
3. Inject connected status for port `0`.
4. Post `CompositeInput_Signal_NOSIGNAL_Status.yaml`, then validate the `noSignal` event.
5. Post `CompositeInput_Signal_UNSTABLE_Status.yaml`, then validate the `unstableSignal` event.
6. Post `CompositeInput_Signal_STABLE_Status.yaml`, then validate the `stableSignal` event.
7. Reset signal status to NO_SIGNAL, disconnect port `0`, clean up, and close the listener.

Response:

```text
Expected: onSignalChanged reports noSignal, unstableSignal, and stableSignal in order for port 0.
TCID17_SignalStatusTransitions Passed
```

## TCID18_VideoModeUpdate

Scenario: Validate that a YAML-injected NTSC 480i video mode produces a non-empty `currentVideoMode` string.

1. Start composite input on port `0`.
2. Inject connected status for port `0`.
3. Post `CompositeInput_VideoMode_Update.yaml`.
4. Wait one second.
5. Call `AVInput.currentVideoMode`.
6. Validate that the call succeeds and returns a non-empty string.
7. Disconnect port `0` and clean up the input.

Response:

```text
Expected: currentVideoMode succeeds and returns a non-empty string after video-mode injection.
TCID18_VideoModeUpdate Passed
```

## TCID19_DisconnectWhilePresenting

Scenario: Validate that disconnecting a source during presentation leaves the plugin responsive and permits stop, reconnect, and restart.

1. Inject connected status for composite port `0`.
2. Start input on port `0`.
3. Inject disconnected status while input is active.
4. Wait one second and validate that the plugin remains healthy.
5. Call `stopInput` and validate success.
6. Inject connected status again and validate that `startInput(0)` succeeds.
7. Disconnect the port and clean up the input.

Response:

```text
Expected: The plugin remains healthy after disconnect.
Expected: stopInput after disconnect and startInput after reconnect succeed.
TCID19_DisconnectWhilePresenting Passed
```

## TCID20_InvalidVComponentInjection

Scenario: Validate that malformed vComponent stimuli do not crash the plugin or prevent subsequent CompositeIn operations.

1. Inject connection status for out-of-range ports `99` and `-1`.
2. Inject the unknown signal state `BOGUS_STATE` for port `0`.
3. Inject an unknown vComponent command.
4. Wait one second and validate that the plugin remains healthy.
5. Call `startInput(0)` followed by `stopInput` and validate that both succeed.
6. Clean up the input.

Response:

```text
Expected: Invalid vComponent injections do not crash or hang the plugin.
Expected: The plugin remains healthy and a valid startInput/stopInput sequence succeeds.
TCID20_InvalidVComponentInjection Passed
```
