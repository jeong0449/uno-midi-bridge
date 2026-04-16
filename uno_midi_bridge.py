import serial
import mido
import time

PORT = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_75834353930351211140-if00'

# Open serial port
ser = serial.Serial(PORT, 31250, timeout=0.001)

# Wate for UNO reset stabilization
time.sleep(2)

# Create ALSA seq port
outport = mido.open_output('UNO-bridge', virtual=True)

running_status = None
data_bytes = []

def expected_data_len(status):
    if 0x80 <= status <= 0xBF:
        return 2
    if 0xC0 <= status <= 0xDF:
        return 1
    if 0xE0 <= status <= 0xEF:
        return 2
    return 0

while True:
    b = ser.read(1)
    if not b:
        continue

    byte = b[0]

    # --- REALTIME messages (can appear anywhere) ---
    if 0xF8 <= byte <= 0xFF:
        try:
            msg = mido.Message.from_bytes([byte])
            outport.send(msg)
        except:
            pass
        continue

    # --- SYSTEM messages (ignored) ---
    if 0xF0 <= byte <= 0xF7:
        running_status = None
        data_bytes = []
        continue

    # --- STATUS BYTE ---
    if byte & 0x80:
        running_status = byte
        data_bytes = []
        continue

    # --- DATA BYTE ---
    if running_status is None:
        continue

    data_bytes.append(byte)
    needed = expected_data_len(running_status)

    if needed and len(data_bytes) >= needed:
        raw = [running_status] + data_bytes[:needed]

        try:
            msg = mido.Message.from_bytes(raw)

            # NOTE OFF stabilization (velocity 0 fix)
            if msg.type == 'note_on' and msg.velocity == 0:
                msg = mido.Message('note_off',
                                   channel=msg.channel,
                                   note=msg.note,
                                   velocity=0)

            outport.send(msg)

        except Exception:
            pass

        data_bytes = data_bytes[needed:]
