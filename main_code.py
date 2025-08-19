"""
Metal Detection Alert System for Raspberry Pi
Detects metal objects using a sensor and sends Telegram alerts with buzzer feedback.
"""

# ======================
# SECTION 1: IMPORTS
# ======================

import RPi.GPIO as GPIO  # For GPIO pin control on Raspberry Pi
import time              # For timing and delays
import asyncio           # For asynchronous operations
from telegram import Bot # For Telegram bot communication

# ======================
# SECTION 2: CONFIGURATION
# ======================

# GPIO Pin Configuration (BCM numbering)
METAL_SENSOR_PIN = 26   # GPIO26 connected to metal sensor's output
BUZZER_PIN = 17         # GPIO17 connected to buzzer's control pin

# Telegram Bot Configuration
BOT_TOKEN = "YOUR_BOT_TOKEN"  # Replace with your bot token from @BotFather
CHAT_ID = "YOUR_CHAT_ID"      # Replace with your chat ID (use @userinfobot to find)

# System Behavior
DETECTION_COOLDOWN = 5  # Minimum seconds between consecutive alerts

# ======================
# SECTION 3: INITIALIZATION
# ======================

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)  # Use Broadcom SOC channel numbering
GPIO.setup(METAL_SENSOR_PIN, GPIO.IN)   # Metal sensor as input
GPIO.setup(BUZZER_PIN, GPIO.OUT)        # Buzzer as output

# Initialize Telegram bot
bot = Bot(token=BOT_TOKEN)

# Track last detection time for cooldown
last_detection_time = 0

# ======================
# SECTION 4: CORE FUNCTIONS
# ======================

async def send_alert():
    """
    Send Telegram alert notification safely with error handling.
    
    Note:
    - Uses async/await for non-blocking network calls
    - Includes try-catch to prevent crashes from network issues
    """
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text="🚨 Metal detected in the car!",
            parse_mode="Markdown"
        )
        print("📢 Telegram alert sent successfully")
    except Exception as e:
        print(f"⚠️ Failed to send Telegram alert: {e}")

def trigger_buzzer(duration=1):
    """
    Activate buzzer for specified duration.
    
    Args:
        duration (float): Seconds to keep buzzer on
    """
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

# ======================
# SECTION 5: MAIN LOOP
# ======================

async def main():
    """
    Primary monitoring loop with detection logic and cooldown management.
    """
    global last_detection_time
    
    print("🚀 Metal detection system activated")
    print(f"📡 Monitoring GPIO {METAL_SENSOR_PIN} for metal objects")
    print(f"🔔 Buzzer configured on GPIO {BUZZER_PIN}")
    print(f"⏳ Alert cooldown: {DETECTION_COOLDOWN} seconds")
    
    try:
        while True:
            # Read sensor (LOW = metal detected, HIGH = no metal)
            if GPIO.input(METAL_SENSOR_PIN) == GPIO.LOW:
                current_time = time.time()
                
                # Check if cooldown period has passed
                if current_time - last_detection_time > DETECTION_COOLDOWN:
                    print("🔍 Metal detected! Triggering alert sequence...")
                    
                    # Alert sequence
                    trigger_buzzer(1)          # 1 second buzzer
                    await send_alert()         # Send Telegram notification
                    
                    # Update last detection time
                    last_detection_time = current_time
                else:
                    cooldown_left = DETECTION_COOLDOWN - (current_time - last_detection_time)
                    print(f"⏱️ Metal detected but in cooldown ({cooldown_left:.1f}s remaining)")
            else:
                print("✅ Area clear (no metal detected)", end='\r')
            
            # Non-blocking sleep to allow other tasks
            await asyncio.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n🛑 Received keyboard interrupt")
    finally:
        # Cleanup resources
        GPIO.cleanup()
        print("♻️ GPIO cleanup completed")
        print("🔴 System shutdown")

# ======================
# SECTION 6: ENTRY POINT
# ======================

if __name__ == "__main__":
    # Start the async event loop
    asyncio.run(main())
