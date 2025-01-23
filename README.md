# Prayer Times WhatsApp Notification Agent

This Python application automatically sends WhatsApp notifications for Islamic prayer times based on your current location.

## Features

- Automatically detects your current location
- Fetches accurate prayer times using the Aladhan API
- Sends WhatsApp notifications before each prayer time
- Updates prayer times daily
- Runs continuously in the background

## Prerequisites

- Python 3.7 or higher
- Twilio account for WhatsApp notifications
- Internet connection for location detection and API calls

## Local Setup

1. Clone this repository:

```bash
git clone <repository-url>
cd prayer-times-agent
```

2. Create and activate a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the template:

```bash
cp .env.example .env
```

5. Set up Twilio:

   - Create a Twilio account at https://www.twilio.com
   - Get your Account SID and Auth Token from the Twilio Console
   - Set up WhatsApp Sandbox in Twilio
   - Update the `.env` file with your Twilio credentials and WhatsApp number

6. Edit the `.env` file with your details:

```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
YOUR_WHATSAPP_NUMBER=your_whatsapp_number
```

## Cloud Deployment

### Option 1: Railway.app (Recommended)

1. Create an account on [Railway.app](https://railway.app)
2. Install Railway CLI:

```bash
# On macOS
brew install railway

# On Windows/Linux
npm i -g @railway/cli
```

3. Login to Railway:

```bash
railway login
```

4. Create a new project:

```bash
railway init
```

5. Deploy the application:

```bash
railway up
```

6. Set environment variables in Railway dashboard:
   - Go to your project settings
   - Add the same variables from `.env` file

### Option 2: Python Anywhere

1. Create an account on [PythonAnywhere](https://www.pythonanywhere.com)
2. Go to the "Files" tab and upload your project files
3. Go to the "Consoles" tab and start a new Bash console
4. Create a virtual environment and install requirements:

```bash
mkvirtualenv --python=/usr/bin/python3.9 prayer_agent
pip install -r requirements.txt
```

5. Set up environment variables in the "Files" tab
6. Create a new task in the "Tasks" tab to run your script

### Option 3: Heroku

1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login to Heroku:

```bash
heroku login
```

3. Create a new Heroku app:

```bash
heroku create prayer-times-agent
```

4. Deploy the application:

```bash
git push heroku main
```

5. Set environment variables:

```bash
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
heroku config:set TWILIO_PHONE_NUMBER=your_twilio_number
heroku config:set YOUR_WHATSAPP_NUMBER=your_number
```

6. Start the worker:

```bash
heroku ps:scale worker=1
```

## Usage

Make sure your virtual environment is activated, then run the agent:

```bash
python prayer_times_agent.py
```

The agent will:

1. Detect your location
2. Fetch prayer times
3. Schedule WhatsApp notifications
4. Run continuously, sending notifications at prayer times

## Notes

- The agent uses Method 2 (Islamic Society of North America) for prayer calculations
- Location is updated daily at midnight
- Prayer times are also updated daily
- The agent must be running continuously to send notifications
- To deactivate the virtual environment when done, simply type `deactivate`
- Make sure to set all environment variables in your cloud platform
- Monitor your cloud platform's logs for any issues
