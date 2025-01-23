import os
import time
import schedule
import requests
import geocoder
from datetime import datetime
from dotenv import load_dotenv
from twilio.rest import Client
from dateutil import parser

# Load environment variables
load_dotenv()

class PrayerTimesAgent:
    def __init__(self):
        # Initialize Twilio client
        self.twilio_client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        self.twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        self.your_whatsapp_number = os.getenv('YOUR_WHATSAPP_NUMBER')
        
        # Get current location
        self.update_location()
        
    def update_location(self):
        """Get current location using IP address"""
        g = geocoder.ip('me')
        if g.ok:
            self.latitude = g.lat
            self.longitude = g.lng
            print(f"Location updated: {g.city}, {g.country}")
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
            if prayer_time > datetime.now():
                schedule.every().day.at(prayer_times[prayer]).do(
                    self.send_whatsapp_message,
                    f"🕌 Time for {name} prayer!"
                )
                print(f"Scheduled {name} prayer notification for {prayer_times[prayer]}")

    def run(self):
        """Run the prayer times agent"""
        print("Starting Prayer Times Agent...")
        
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