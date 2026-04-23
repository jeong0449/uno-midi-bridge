# uno-midi-bridge

**Created:** 2026-04-17

Bridge raw MIDI from Arduino UNO USB-serial to ALSA MIDI on Linux.

---

## 1. Overview

This project provides a simple and practical way to:

Receive raw MIDI bytes from an Arduino UNO (USB-serial)  
and convert them into usable ALSA MIDI streams

It includes:

- a raw MIDI dump tool
- a Python-based ALSA bridge
- a C-based ALSA bridge (recommended for real use)

---

## 2. Background

This project originated as part of a broader system:

### Fluid Ardule

[Fluid Ardule](https://github.com/jeong0449/FluidArdule) is a DIY sound module system built around:

- Raspberry Pi (synthesis engine, e.g., FluidSynth)
- Arduino-based controllers and MIDI engines

In that system, this Arduino UNO is referred to as:

**UNO-2**

[UNO-2](https://github.com/jeong0449/NanoArdule/tree/main/firmware/ardule_usb_midi_host) (a.k.a. Ardule USB MIDI Host) acts as:

- MIDI input engine
- USB/DIN MIDI bridge
- reliable front-end for software synthesis

UNO-2 functions as a subsystem within the Nano Ardule architecture, which is introduced just below.

---

### Nano Ardule

This project is also related to [Nano Ardule](https://github.com/jeong0449/NanoArdule):

- Arduino firmware for MIDI processing is implemented there
- The UNO firmware used in this project originates from that ecosystem

---

## 3. Hardware Concept

<img src="https://github.com/jeong0449/NanoArdule/blob/main/images/MIDI_router_20260416.png" width="800" align="left">

This diagram shows the role of UNO-2 as a MIDI router/bridge between USB MIDI devices,
DIN MIDI devices, and a Raspberry Pi-based synthesis system.

<br clear="left">

---

## 4. Components

### `uno_midi_serial_dump.py`

Purpose:
- Verify that raw MIDI bytes are actually arriving from UNO-2 over USB-serial

### `uno_midi_bridge.py`

Purpose:
- Convert raw MIDI into ALSA MIDI using Python

### `uno_midi_bridge_sp.c`

Purpose:
- High-performance bridge in C (recommended)

- Appears in `aconnect -l`
- Can be connected to FluidSynth
- Auto-recovers on reset or reconnect

For practical use, only the compiled binary from `uno_midi_bridge_sp.c` is required.

---

## 5. Installation

### Python

```bash
sudo apt update
sudo apt install python3-serial python3-mido python3-rtmidi
```

### C

```bash
sudo apt update
sudo apt install build-essential libasound2-dev libserialport-dev
```

Compile:

```bash
gcc -O2 -Wall -o uno_midi_bridge_sp uno_midi_bridge_sp.c -lasound -lserialport
```

---

## 6. Usage
### 6.1 Connect UNO-2 first

Before running any program, make sure **UNO-2 is connected first**, with a MIDI keyboard attached.

### 6.2 Verify the serial MIDI stream with Python

Start with the raw dump tool to confirm that MIDI bytes are actually arriving from UNO-2:

```bash
python3 uno_midi_serial_dump.py
```

When you play the keyboard, hexadecimal byte values starting with `0x` should appear on the screen.

Example:

```text
0x90 0x3c 0x7f 0x80 0x3c 0x00
```

If no output appears, check:

- USB connection
- Serial device path (`/dev/serial/by-id/...`)
- MIDI keyboard power/status

### 6.3 Run the Python bridge

```bash
python3 uno_midi_bridge.py
```

Use this when you want a quick Python-based ALSA MIDI bridge for testing.

### 6.4 Run the C bridge (recommended)

```bash
./uno_midi_bridge_sp
```

Use this for practical operation. The C version is more suitable for long-running sessions and real-time use.


---

## 7. Example (FluidSynth)

```bash
fluidsynth -a alsa -m alsa_seq /home/pi/sf2/FluidR3_GM.sf2
./uno_midi_bridge_sp
aconnect -l
aconnect 128:0 129:0
```

---

## 8. Recovery behavior

The C bridge automatically recovers when:

- UNO-2 is reset
- USB cable is unplugged and reconnected

---

## 9. Limitations

- SysEx not supported
- Single merged MIDI stream

---

## 10. Summary

A minimal but powerful bridge connecting Arduino MIDI to Linux audio.
