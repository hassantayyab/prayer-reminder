import os
import time
import schedule
import requests
import geocoder
from datetime import datetime, timedelta
from dotenv import load_dotenv
from twilio.rest import Client
from dateutil import parser

# Load environment variables
load_dotenv()

# App version
APP_VERSION = "1.2.0"  # Enhanced notifications with beautiful formatting

class PrayerTimesAgent:
    def __init__(self):
        # Initialize Twilio client
        self.twilio_client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        self.twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        self.your_whatsapp_number = os.getenv('YOUR_WHATSAPP_NUMBER')
        
        # Prayer emojis mapping
        self.prayer_emojis = {
            'Fajr': '🌅',     # Sunrise for Fajr
            'Dhuhr': '☀️',    # Sun for Dhuhr
            'Asr': '🌤️',     # Sun behind cloud for Asr
            'Maghrib': '🌅',  # Sunset for Maghrib
            'Isha': '🌙'      # Crescent moon for Isha
        }
        
        # Get current location
        self.update_location()
        
    def send_startup_notification(self):
        """Send startup notification with app info"""
        startup_message = (
            f"🚀 Prayer Times Agent v{APP_VERSION} is now running!\n\n"
            f"📍 Location: {self.city}, {self.country}\n"
            f"⚙️ Features:\n"
            f"• 🕌 All prayer time notifications\n"
            f"• ⏰ 10-min advance alert for Asr\n"
            f"• ⏰ 10-min advance alert for Isha\n\n"
            f"🤲 May Allah accept our prayers\n"
            f"📱 Notifications are now active"
        )
        self.send_whatsapp_message(startup_message)
        
    def update_location(self):
        """Get current location using IP address"""
        g = geocoder.ip('me')
        if g.ok:
            self.latitude = g.lat
            self.longitude = g.lng
            self.city = g.city
            self.country = g.country
            print(f"Location updated: {self.city}, {self.country}")
        else:
            raise Exception("Could not get location")

    def get_prayer_times(self):
        """Fetch prayer times from API"""
        url = f"http://api.aladhan.com/v1/timings/{int(time.time())}?latitude={self.latitude}&longitude={self.longitude}&method=2"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['data']['timings']
        else:
            raise Exception("Failed to fetch prayer times")

    def send_whatsapp_message(self, message):
        """Send WhatsApp message using Twilio"""
        try:
            message = self.twilio_client.messages.create(
                body=message,
                from_=f"whatsapp:{self.twilio_phone_number}",
                to=f"whatsapp:{self.your_whatsapp_number}"
            )
            print(f"Message sent: {message.sid}")
        except Exception as e:
            print(f"Error sending message: {str(e)}")

    def get_time_minus_minutes(self, time_str, minutes):
        """Get time minus specified minutes"""
        prayer_time = parser.parse(f"{datetime.now().strftime('%Y-%m-%d')} {time_str}")
        return (prayer_time - timedelta(minutes=minutes)).strftime("%H:%M")

    def format_prayer_message(self, prayer_name, time_str, is_advance=False):
        """Format prayer notification message with beautiful styling"""
        emoji = self.prayer_emojis.get(prayer_name, '🕌')
        current_date = datetime.now().strftime("%d %B %Y")
        
        if is_advance:
            return (
                f"⏰ Prayer Reminder ⏰\n\n"
                f"Get ready for {prayer_name} prayer!\n"
                f"{emoji} Time: {time_str}\n"
                f"📅 {current_date}\n\n"
                f"🤲 10 minutes remaining to prepare"
            )
        else:
            return (
                f"🕌 Prayer Time 🕌\n\n"
                f"{emoji} {prayer_name} Prayer\n"
                f"⏰ Time: {time_str}\n"
                f"📅 {current_date}\n\n"
                f"🤲 May Allah accept our prayers"
            )

    def schedule_prayers(self):
        """Schedule prayer time notifications"""
        prayer_times = self.get_prayer_times()
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Prayer names mapping
        prayer_names = {
            'Fajr': 'Fajr',
            'Dhuhr': 'Dhuhr',
            'Asr': 'Asr',
            'Maghrib': 'Maghrib',
            'Isha': 'Isha'
        }

        # Schedule notifications for each prayer
        for prayer, name in prayer_names.items():
            prayer_time = parser.parse(f"{current_date} {prayer_times[prayer]}")
            
            # Schedule regular prayer notification
            if prayer_time > datetime.now():
                schedule.every().day.at(prayer_times[prayer]).do(
                    self.send_whatsapp_message,
                    self.format_prayer_message(name, prayer_times[prayer])
                )
                print(f"Scheduled {name} prayer notification for {prayer_times[prayer]}")
                
                # Schedule 10-minute advance notification for Asr and Isha
                if prayer in ['Asr', 'Isha']:
                    advance_time = self.get_time_minus_minutes(prayer_times[prayer], 10)
                    advance_time_obj = parser.parse(f"{current_date} {advance_time}")
                    
                    if advance_time_obj > datetime.now():
                        schedule.every().day.at(advance_time).do(
                            self.send_whatsapp_message,
                            self.format_prayer_message(name, prayer_times[prayer], is_advance=True)
                        )
                        print(f"Scheduled 10-minute advance notification for {name} prayer at {advance_time}")

    def run(self):
        """Run the prayer times agent"""
        print("Starting Prayer Times Agent...")
        
        # Send startup notification
        self.send_startup_notification()
        
        # Schedule daily location update and prayer scheduling
        schedule.every().day.at("00:01").do(self.update_location)
        schedule.every().day.at("00:02").do(self.schedule_prayers)
        
        # Initial run
        self.schedule_prayers()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(30)

if __name__ == "__main__":
    agent = PrayerTimesAgent()
    agent.run() 