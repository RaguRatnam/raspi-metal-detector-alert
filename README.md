Raspberry Pi Metal Detector with Telegram Alerts & Buzzer
This project uses a metal detector sensor with a Raspberry Pi to detect metal objects.
When metal is detected:
- A Telegram notification is sent instantly 📲
- A buzzer connected to the Pi sounds 🔊

Perfect for learning Raspberry Pi GPIO, real-time notifications, and IoT projects.
⚡ Features
•	Detects metal objects using a metal sensor (powered by 9V battery).
•	Sends Telegram alerts instantly.
•	Activates a buzzer alarm when metal is detected.
•	Runs automatically on boot.
•	Safe 3.3V GPIO protection via voltage divider.
🛠️ Hardware Required
•	Raspberry Pi (any model with GPIO, e.g., Pi 4B).
•	Metal Detector Sensor (3-wire type: Brown = VCC, Blue = GND, Black = OUT)(I used a 6-36v normally open).
•	9V Battery (to power the sensor).
•	Resistors: 10kΩ + 4.7kΩ (for voltage divider).
•	Buzzer (active buzzer, connected to GPIO17).
•	Jumper wires & breadboard.
⚡ Wiring Diagram
(Sensor Brown) ---------- (+9V Battery)
(Sensor Blue) ----------- (-9V Battery AND Raspberry Pi GND)
(Sensor Black) --+-- 10kΩ --+-- GPIO18 (Raspberry Pi)
                 |          |
                 |         4.7kΩ
                 |          |
                 +--------- GND (Raspberry Pi)

(Buzzer +) ---------------- GPIO17 (Raspberry Pi)
(Buzzer -) ---------------- GND (Raspberry Pi)

⚠️ Important: Always connect Raspberry Pi GND and sensor GND together.
📦 Software Setup
1. Clone the repository
git clone https://github.com/your-username/pi-metal-detector.git
cd pi-metal-detector
2. Create a virtual environment
python3 -m venv my_project_env
source my_project_env/bin/activate
3. Install dependencies
pip install python-telegram-bot RPi.GPIO
4. Configure Telegram Bot
- Create a bot via BotFather.
- Copy your BOT_TOKEN.
- Get your CHAT_ID by sending a message to your bot and checking:
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
- Update telegram_metal_detector.py with your token and chat ID.
▶️ Run the Program
python3 telegram_metal_detector.py
You should see:
🚀 Monitoring for metal detection...
🚗 Metal Detected! Sending Telegram alert and buzzing...
🔄 Auto-Start on Boot
1. Create a systemd service
sudo nano /etc/systemd/system/metal_detector.service
2. Paste:
[Unit]
Description=Raspberry Pi Metal Detector
After=multi-user.target

[Service]
ExecStart=/home/pi/my_project_env/bin/python3 /home/pi/telegram_metal_detector.py
WorkingDirectory=/home/pi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
3. Enable service
sudo systemctl daemon-reload
sudo systemctl enable metal_detector.service
sudo systemctl start metal_detector.service
Now it will run automatically on boot.

📝 License
MIT License. Free to use and modify.
