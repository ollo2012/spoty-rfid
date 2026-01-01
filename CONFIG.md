## Raspotify Installation & Configuration Guide

This guide explains how to install and configure [Raspotify](https://github.com/dtcooper/raspotify) to use with the spoty-rfid project on a Raspberry Pi.

### Prerequisites
- Raspberry Pi running Raspberry Pi OS (or compatible Debian-based OS)
- Internet connection
- sudo privileges

---

### 1. Install Raspotify

Open a terminal and run:

```sh
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
```

This will install Raspotify as a system service.

---

### 2. Configure Raspotify

Edit the configuration file:

```sh
sudo nano /etc/raspotify/conf
```

Recommended settings:

- **DEVICE_NAME**: Set a unique name for your device (e.g., `spoty-rfid`)
- **BITRATE**: (optional) Set to `160` or `320` for higher quality
- **OPTIONS**: (optional) Add `--disable-discovery` if you want to hide the device from Spotify Connect

### As spotify is  

Example:
```
DEVICE_NAME="spoty-rfid"
BITRATE="160"
#OPTIONS="--disable-discovery"
```

Save and exit (Ctrl+O, Enter, Ctrl+X).

---

### 3. Restart Raspotify

```sh
sudo systemctl restart raspotify
```

---

### 4. Test Raspotify

1. Open Spotify on your phone or computer (same network).
2. Look for the device name you set (e.g., `spoty-rfid`) in the list of available devices.
3. Select it and play music.

---

### 5. Integrate with spoty-rfid

The spoty-rfid project uses Raspotify as the Spotify Connect backend. No further configuration is needed unless you want to customize advanced options.

---

### 6. Troubleshooting

- Check service status: `sudo systemctl status raspotify`
- View logs: `journalctl -u raspotify -e`
- Ensure your device and phone/computer are on the same network.

---

For more details, see the [Raspotify GitHub page](https://github.com/dtcooper/raspotify).



### Headless Setup

To run your Raspberry Pi without a monitor, keyboard, or mouse (headless):

**1. Enable Autologin:**
Configure your Raspberry Pi to automatically log in on boot using systemd override:

```sh
sudo mkdir -p /etc/systemd/system/getty@tty1.service.d
sudo nano /etc/systemd/system/getty@tty1.service.d/override.conf
```
Add the following content to `override.conf`:
```
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin pi --noclear %I $TERM
```
Replace `pi` with your username if different. Save and exit, then reboot to apply autologin.

**2. Headless WiFi Connection:**
For automatic WiFi connection without manual input, use a preconfigured `wpa_supplicant-wlan0.conf` file. Place this file in `/boot` before first boot, or configure `/etc/wpa_supplicant/wpa_supplicant.conf` with your network details.

After setting up your configuration file, enable the WiFi service for the interface:
```sh
sudo systemctl enable wpa_supplicant@wlan0.service
sudo systemctl start wpa_supplicant@wlan0.service
```
This ensures your Raspberry Pi connects to WiFi automatically on boot, even in headless mode.

**3. Unmanage WiFi Interface in NetworkManager:**
If using NetworkManager, prevent it from managing the WiFi interface (`wlan0`) to avoid conflicts:

Edit `/etc/NetworkManager/NetworkManager.conf` and add at the bottom:
```
[keyfile]
unmanaged-devices=interface-name:wlan0
```
This ensures NetworkManager does not interfere with your manual WiFi setup.



