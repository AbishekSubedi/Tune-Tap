import time
import board
from analogio import AnalogIn

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode as CC

# ===================== BLE SETUP =====================

ble = BLERadio()
hid = HIDService()
advertisement = ProvideServicesAdvertisement(hid)

# Consumer Control (media keys)
cc = ConsumerControl(hid.devices)

# ===================== SENSOR PINS ===================

fsr   = AnalogIn(board.A4)  # FSR (thumb pad)
ptr   = AnalogIn(board.A0)  # Pointer flex
mid   = AnalogIn(board.A1)  # Middle flex
ring  = AnalogIn(board.A2)  # Ring flex
pky   = AnalogIn(board.A3)  # Pinky flex

# ===================== THRESHOLDS ====================
# CircuitPython AnalogIn gives 0–65535

FSR_THR  = 50000  # FSR: pressed if value > 50000

# Flex sensors inverted:
# bending -> value decreases, unbent -> value increases
# So: BENT if value < threshold
PTR_THR  = 200   # pointer bent if value < 1000
MID_THR  = 54000  # middle  bent if value < 54000
RING_THR = 58000  # ring    bent if value < 60000
PKY_THR  = 55000  # pinky   bent if value < 55000

# ===================== DEBOUNCE CONFIG =================

DEBOUNCE_SAMPLES = 3  # consecutive active samples needed

fsr_cnt  = 0
ptr_cnt  = 0
mid_cnt  = 0
ring_cnt = 0
pky_cnt  = 0

fsr_state  = False
ptr_state  = False
mid_state  = False
ring_state = False
pky_state  = False

fsr_prev  = False
ptr_prev  = False
mid_prev  = False
ring_prev = False
pky_prev  = False


# ===================== MEDIA HELPERS ===================

def send_cc(code):
    """Safely send a Consumer Control key (handles disconnects)."""
    if not ble.connected:
        return
    try:
        cc.send(code)
    except OSError:
        # Happens if we send right when disconnecting – ignore
        pass

def send_play_pause():
    send_cc(CC.PLAY_PAUSE)

def send_next_track():
    send_cc(CC.SCAN_NEXT_TRACK)

def send_prev_track():
    send_cc(CC.SCAN_PREVIOUS_TRACK)

def send_vol_up():
    send_cc(CC.VOLUME_INCREMENT)

def send_vol_down():
    send_cc(CC.VOLUME_DECREMENT)


# ===================== DEBOUNCE HELPER =================

def debounce(raw_active, cnt, state):
    """
    Simple debounce:
    - If raw_active: increase counter up to DEBOUNCE_SAMPLES.
    - If not: reset counter.
    - State is True only when counter >= DEBOUNCE_SAMPLES.
    """
    if raw_active:
        if cnt < DEBOUNCE_SAMPLES:
            cnt += 1
    else:
        cnt = 0

    state = (cnt >= DEBOUNCE_SAMPLES)
    return cnt, state


# ===================== MAIN LOOP ======================

print("TuneTap Glove – CircuitPython Media Remote")
print("Advertising as BLE HID...")

while True:
    # Start advertising when not connected
    if not ble.connected:
        if not ble.advertising:
            ble.start_advertising(advertisement)
        # We still read sensors for debugging if you want, but no gestures
        time.sleep(0.05)
        continue

    # ---- READ RAW SENSORS ----
    fsr_val  = fsr.value
    ptr_val  = ptr.value
    mid_val  = mid.value
    ring_val = ring.value
    pky_val  = pky.value

    # ---- RAW THRESHOLD CHECKS ----
    fsr_raw_active  = (fsr_val  > FSR_THR)
    ptr_raw_bent    = (ptr_val  < PTR_THR)
    mid_raw_bent    = (mid_val  < MID_THR)
    ring_raw_bent   = (ring_val < RING_THR)
    pky_raw_bent    = (pky_val  < PKY_THR)

    # ---- DEBOUNCE EACH INPUT ----
    fsr_cnt,  fsr_state  = debounce(fsr_raw_active,  fsr_cnt,  fsr_state)
    ptr_cnt,  ptr_state  = debounce(ptr_raw_bent,    ptr_cnt,  ptr_state)
    mid_cnt,  mid_state  = debounce(mid_raw_bent,    mid_cnt,  mid_state)
    ring_cnt, ring_state = debounce(ring_raw_bent,   ring_cnt, ring_state)
    pky_cnt,  pky_state  = debounce(pky_raw_bent,    pky_cnt,  pky_state)

    # ---- RISING EDGE DETECTION ----
    fsr_rise  = fsr_state  and not fsr_prev
    ptr_rise  = ptr_state  and not ptr_prev
    mid_rise  = mid_state  and not mid_prev
    ring_rise = ring_state and not ring_prev
    pky_rise  = pky_state  and not pky_prev

    fsr_prev  = fsr_state
    ptr_prev  = ptr_state
    mid_prev  = mid_state
    ring_prev = ring_state
    pky_prev  = pky_state

    # ---- DEBUG PRINT ----
    print(
        "FSR: {} > {} => {} | PTR: {} < {} => {} | MID: {} < {} => {} | "
        "RING: {} < {} => {} | PKY: {} < {} => {} | connected: {}".format(
            fsr_val,  FSR_THR,  fsr_raw_active,
            ptr_val,  PTR_THR,  ptr_raw_bent,
            mid_val,  MID_THR,  mid_raw_bent,
            ring_val, RING_THR, ring_raw_bent,
            pky_val,  PKY_THR,  pky_raw_bent,
            ble.connected,
        )
    )

    # ===================== GESTURES ======================
    # FSR tap => PLAY / PAUSE
    if fsr_rise:
        print("FSR event → PLAY/PAUSE | value:", fsr_val)
        send_play_pause()

    # Pointer bent => PREVIOUS TRACK
    if ptr_rise:
        print(">> PREVIOUS TRACK (Pointer:", ptr_val, ")")
        send_prev_track()

    # Middle bent => NEXT TRACK
    if mid_rise:
        print(">> NEXT TRACK (Middle:", mid_val, ")")
        send_next_track()

    # Ring bent => VOLUME DOWN
    if ring_rise:
        print(">> VOL DOWN (Ring:", ring_val, ")")
        send_vol_down()

    # Pinky bent => VOLUME UP
    if pky_rise:
        print(">> VOL UP (Pinky:", pky_val, ")")
        send_vol_up()

    time.sleep(0.01)