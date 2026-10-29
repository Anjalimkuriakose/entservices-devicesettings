AVInput (COMPOSITE IN) L3 vDevice Test Suite
============================================

JSON-RPC functional suite for org.rdk.AVInput with typeOfInput=COMPOSITE,
built on the same framework as the HDMI AVInput vDevice suite
(SuiteManager + utils + Curl builders + Testcases/TCIDxx + YAML injection).

RUN
---
cd Tests/vDeviceTests
python3 SuiteManager.py compositein            # all testcases
python3 SuiteManager.py -t compositein         # with timing
python3 SuiteManager.py compositein --test TCID02_StartStopInput

Lifecycle: org.rdk.DeviceSettings and org.rdk.AVInput are activated ONCE before
all testcases and deactivated ONCE after (reverse order). Disable with
AUTO_ACTIVATE_PLUGINS=0. Before each testcase Init_CompositeIn_Populate
verifies getInputDevices(COMPOSITE) and issues a best-effort stopInput.

Env: TARGET_HOST, JSONRPC_PORT, WPEFRAMEWORK_JSONRPC_URL,
     COMPOSITEIN_VCOMPONENT_PORT / COMPOSITEIN_VCOMPONENT_API_URL,
     COMPOSITEIN_CMD_BASE, AVINPUT_EVENT_TIMEOUT.

APIS COVERED (portId is a string, e.g. "0")
  getInputDevices / startInput / stopInput / setVideoRectangle

TESTCASES
---------
POSITIVE
 TCID01_GetInputDevices          list shape: id/locator/connected, unique ids
 TCID02_StartStopInput           start/stop + onInputStatusChanged, idempotent stop
 TCID03_SetVideoRectangle        full-screen, PIP, moved PIP, restore
 TCID04_StartStopCycle           5 cycles on every port
 TCID05_PortSwitching            switch ports without stop (scenario)
 TCID15_PresentationWorkflow     enumerate->start->rects->stop->re-enumerate
NEGATIVE
 TCID06_InvalidPortId            abc / "" / -1 / 10 / huge / 0.5 / null / missing
 TCID07_InvalidTypeOfInput       ABCD / "" / wrong case / number on all 4 APIs
 TCID08_InvalidRectangle         missing / wrong-type / negative / zero / float
 TCID09_StopWithoutStart         repeated idle stopInput
 TCID10_RectangleWithoutActiveInput  rectangle before start / after stop
EDGE-TO-EDGE
 TCID11_BoundaryRectangle        1x1, 4K, off-screen, INT32_MAX(+1)
 TCID12_DoubleStartSamePort      start twice, single stop releases
 TCID13_HdmiCompositeIsolation   HDMI vs COMPOSITE independence
 TCID14_RapidStartStopStress     25 back-to-back start/rect/stop loops
YAML / vCOMPONENT DRIVEN (vcomponent_configurations/commands)
 TCID16_ConnectionStatusUpdate   hot-plug -> onDevicesChanged + getInputDevices
 TCID17_SignalStatusTransitions  noSignal -> unstable -> stable (onSignalChanged)
 TCID18_VideoModeUpdate          video mode injection -> currentVideoMode
 TCID19_DisconnectWhilePresenting unplug during presentation, recover on replug
 TCID20_InvalidVComponentInjection bad port/state/command; plugin survives

ASSUMPTIONS TO VERIFY ON YOUR VCOMPONENT
- The composite vComponent accepts the top-level key "compositeinput" with
  commands connection_status {port, connected}, signal_status {port, state:
  NO_SIGNAL|UNSTABLE|LOCKED} and video_mode_update. These mirror the HDMI
  "hdmiinput" schema; rename in CompositeIn_Helpers.post_composite and the
  YAML files if your vComponent differs.
- "Must be rejected" checks (TCID06/07/08) expect a JSON-RPC error or
  success:false; relax them if the target plugin is lenient.
