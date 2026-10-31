# Tuya Smart Litter Box Integration for Home Assistant (HACS)

A local Home Assistant integration for Tuya and Tonepie compatible self-cleaning smart cat litter boxes (Tonepie T1 Pro / Ti Pro / PetLux / generic Tuya models).

This integration communicates **100% locally** with the litter box using the local Tuya LAN protocol—no cloud connection or Tuya developer subscription required after initial pairing.

---

## 🌟 Features & Entities

### Binary Sensors
* **Waste Drawer Full** (`binary_sensor.smart_litter_box_waste_drawer_full`): Alerts when the waste drawer is full (DP 103).
* **Cat Occupancy** (`binary_sensor.smart_litter_box_cat_occupancy`): Real-time occupancy sensor when a cat enters the box (DP 104).

### Sensors
* **Last Cat Weight** (`sensor.smart_litter_box_last_cat_weight`): Cat weight recorded during last use (in kg or lbs).
* **Last Visit Duration** (`sensor.smart_litter_box_last_visit_duration`): Time spent in seconds during the last visit.
* **Visits Today** (`sensor.smart_litter_box_visits_today`): Total bathroom visits recorded today.
* **Litter Level** (`sensor.smart_litter_box_litter_level`): Current baseline litter level (%).
* **Cycle Status** (`sensor.smart_litter_box_cycle_status`): `idle`, `cleaning`, or `emptying`.
* **Fault Code** (`sensor.smart_litter_box_fault_code`): Hardware diagnostic bitfield (`0` = normal).

### Switches
* **Auto Clean** (`switch.smart_litter_box_auto_clean`): Toggle auto-cleaning cycle after cat visits.
* **Deodorizer** (`switch.smart_litter_box_deodorizer`): Toggle built-in ionic deodorizer.
* **Auto Deodorize** (`switch.smart_litter_box_auto_deodorize`): Toggle automatic deodorization schedule.
* **Child Lock** (`switch.smart_litter_box_child_lock`): Lock/unlock physical buttons on the device.
* **Safety Radar** (`switch.smart_litter_box_safety_radar`): Toggle infrared/radar anti-pinch safety sensor.
* **Smart Clean** (`switch.smart_litter_box_smart_clean`): Smart clean mode.

### Action Buttons
* **Clean Now** (`button.smart_litter_box_clean_now`): Triggers a manual sifting clean cycle.
* **Empty Drum** (`button.smart_litter_box_empty_drum`): Dumps remaining litter into the waste drawer.

---

## 📦 Installation via HACS

1. Open **Home Assistant**.
2. Go to **HACS** > **Integrations**.
3. Click the **three dots menu** in the top right corner and choose **Custom repositories**.
4. Paste the URL of this repository (or your GitHub repo URL), select category **Integration**, and click **Add**.
5. Find **Tuya Smart Litter Box** in HACS and click **Download**.
6. **Restart Home Assistant**.

---

## ⚙️ Configuration

1. In Home Assistant, go to **Settings** > **Devices & Services**.
2. Click **Add Integration** in the bottom right corner.
3. Search for **Tuya Smart Litter Box**.
4. Fill in your device details:
   - **Device ID**: Your Tuya device ID (e.g., `bf0123456789abcdef0123`)
   - **IP Address**: Local IP of the litter box (e.g., `192.168.1.100`)
   - **Local Key**: 16-character local encryption key (e.g., `abcdef0123456789`)
   - **Protocol Version**: Select `3.5` (or `3.3` / `3.4` depending on your device firmware)
5. Click **Submit**. Your litter box and all its entities will now appear in your Home Assistant dashboard!

> [!TIP]
> Ensure the **Tuya** or **Smart Life** app on your phone is **closed** when connecting, as Tuya devices only allow one local connection at a time.

