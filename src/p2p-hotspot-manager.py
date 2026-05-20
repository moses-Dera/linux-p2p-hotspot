#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import time
import re

def run_cmd(cmd, sudo_pass=None):
    if sudo_pass:
        cmd = f"echo '{sudo_pass}' | sudo -S " + cmd
    try:
        out = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError as e:
        out = e.output.strip()
        
    lines = [line.strip() for line in out.split('\n') if line.strip() and not line.startswith("[sudo]")]
    if not lines:
        return ""
    return lines[-1]

def run_sudo_script(script_content, sudo_pass):
    import tempfile, os
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as f:
        f.write(script_content)
    res = run_cmd(f"bash {path}", sudo_pass)
    os.remove(path)
    return res

class HotspotManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("P2P Hotspot Manager")
        self.root.geometry("450x750")
        self.sudo_pass = None
        
        tk.Label(root, text="Hotspot Name (SSID):").pack(pady=5)
        self.ssid_var = tk.StringVar(value="MyCustomHotspot")
        tk.Entry(root, textvariable=self.ssid_var, width=30).pack()
        
        tk.Label(root, text="Password (min 8 chars):").pack(pady=5)
        self.psk_var = tk.StringVar(value="password123")
        tk.Entry(root, textvariable=self.psk_var, width=30).pack()
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Start Hotspot", command=self.start_hotspot, bg="green", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Stop Hotspot", command=self.stop_hotspot, bg="red", fg="white").grid(row=0, column=1, padx=5)
        
        self.status_var = tk.StringVar(value="Status: Stopped")
        tk.Label(root, textvariable=self.status_var, fg="blue").pack(pady=5)
        
        self.qr_label = tk.Label(root)
        self.qr_label.pack(pady=5)
        
        tk.Label(root, text="Connected Devices:").pack(pady=5)
        self.devices_frame = tk.Frame(root)
        self.devices_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Button(root, text="Refresh Devices", command=self.refresh_devices).pack(pady=5)
        
    def log(self, msg):
        self.status_var.set(f"Status: {msg}")
        self.root.update()

    def start_hotspot(self):
        ssid = self.ssid_var.get()
        psk = self.psk_var.get()
        if len(psk) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters.")
            return
            
        if not self.sudo_pass:
            self.sudo_pass = simpledialog.askstring("Password", "Enter your Ubuntu (sudo) password:", show='*')
            if not self.sudo_pass:
                return
                
        self.log("Configuring network (Please hold still for Howdy...)")
        script = f"""
set -e
wpa_cli -i wlo1 p2p_group_remove wlo1 || true
for i in {{0..10}}; do wpa_cli -i wlo1 p2p_group_remove p2p-wlo1-$i || true; done
killall dnsmasq || true
net_id=$(wpa_cli -i wlo1 add_network)
wpa_cli -i wlo1 set_network $net_id ssid '"{ssid}"'
wpa_cli -i wlo1 set_network $net_id psk '"{psk}"'
wpa_cli -i wlo1 set_network $net_id mode 3
wpa_cli -i wlo1 set_network $net_id disabled 2
res=$(wpa_cli -i wlo1 p2p_group_add persistent=$net_id)
if [[ "$res" != *"OK"* ]]; then
    echo "P2P_FAIL_$res"
    exit 1
fi
sleep 3
P2P_IFACE=$(ip link | grep -o 'p2p-wlo1-[0-9]*' | head -n 1)
if [ -z "$P2P_IFACE" ]; then
    echo "NO_IFACE"
    exit 1
fi
ifconfig $P2P_IFACE 192.168.42.1 netmask 255.255.255.0 up || true
iw dev wlo1 set power_save off || true
sysctl -w net.ipv4.ip_forward=1 || true
iptables -I INPUT -i $P2P_IFACE -j ACCEPT || true
iptables -t nat -A POSTROUTING -o wlo1 -j MASQUERADE || true
iptables -A FORWARD -i wlo1 -o $P2P_IFACE -m state --state RELATED,ESTABLISHED -j ACCEPT || true
iptables -A FORWARD -i $P2P_IFACE -o wlo1 -j ACCEPT || true
dnsmasq -a 192.168.42.1 -z -i $P2P_IFACE --dhcp-range=192.168.42.10,192.168.42.100,12h --dhcp-leasefile=/tmp/hotspot.leases || true
echo "ALL_OK"
"""
        res = run_sudo_script(script, self.sudo_pass)
        if "ALL_OK" not in res:
            messagebox.showerror("Error", f"Failed to start Hotspot. Output: {res}")
            return
            
        qr_path = "/tmp/hotspot_qr.png"
        run_cmd(f'qrencode -o {qr_path} -s 5 "WIFI:T:WPA;S:{ssid};P:{psk};;"')
        try:
            self.qr_img = tk.PhotoImage(file=qr_path)
            self.qr_label.config(image=self.qr_img)
        except Exception:
            pass
            
        self.log("Running! Connected devices will appear below.")
        self.refresh_devices()

    def stop_hotspot(self):
        if not self.sudo_pass:
            self.sudo_pass = simpledialog.askstring("Password", "Enter your Ubuntu (sudo) password:", show='*')
            if not self.sudo_pass:
                return
        self.log("Stopping Hotspot...")
        script = """
for i in {0..10}; do wpa_cli -i wlo1 p2p_group_remove p2p-wlo1-$i || true; done
killall dnsmasq || true
iw dev wlo1 set power_save on || true
iptables -D INPUT -i p2p-wlo1-0 -j ACCEPT || true
iptables -D INPUT -i p2p-wlo1-1 -j ACCEPT || true
iptables -D INPUT -i p2p-wlo1-2 -j ACCEPT || true
iptables -t nat -D POSTROUTING -o wlo1 -j MASQUERADE || true
echo "STOPPED"
"""
        run_sudo_script(script, self.sudo_pass)
        self.qr_label.config(image="")
        self.log("Stopped.")
        self.refresh_devices()

    def block_user(self, mac):
        if not self.sudo_pass:
            self.sudo_pass = simpledialog.askstring("Password", "Enter your Ubuntu (sudo) password:", show='*')
            if not self.sudo_pass:
                return
        run_cmd(f"iptables -I FORWARD -m mac --mac-source {mac} -j DROP", self.sudo_pass)
        self.log(f"Blocked MAC: {mac}")
        messagebox.showinfo("Blocked", f"Device {mac} has been blocked from accessing the internet.")

    def refresh_devices(self):
        for widget in self.devices_frame.winfo_children():
            widget.destroy()
            
        P2P_IFACE = run_cmd("ip link | grep -o 'p2p-wlo1-[0-9]*' | head -n 1")
        if not P2P_IFACE:
            tk.Label(self.devices_frame, text="Hotspot not running.").pack()
            return
            
        out = run_cmd("cat /tmp/hotspot.leases 2>/dev/null || echo ''")
        devices = []
        for line in out.split('\n'):
            parts = line.strip().split()
            if len(parts) >= 4:
                mac = parts[1]
                ip = parts[2]
                name = parts[3]
                if name == "*":
                    name = "Phone/PC"
                devices.append({'ip': ip, 'mac': mac, 'name': name})
        
        if not devices:
            tk.Label(self.devices_frame, text="No devices found. (Ensure they are fully connected)").pack()
            return
            
        for dev in devices:
            f = tk.Frame(self.devices_frame, bd=1, relief="solid")
            f.pack(fill=tk.X, pady=2)
            tk.Label(f, text=f"{dev['name']} ({dev['ip']})\nMAC: {dev['mac']}").pack(side=tk.LEFT, padx=5)
            tk.Button(f, text="Block", bg="red", fg="white", 
                      command=lambda m=dev['mac']: self.block_user(m)).pack(side=tk.RIGHT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = HotspotManagerApp(root)
    root.mainloop()
