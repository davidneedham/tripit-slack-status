import datetime
from icalendar import Calendar
from urllib.request import urlopen, Request
from urllib.parse import urlencode

# Define the variables
TRIPIT_ICAL_URL='enter-your-trip-ical-url'
SLACK_API_TOKEN='enter-your-slack-api-token'
TRIPIT_HOME='enter the city, state of your home'

# Read the calendar stream.
ical_reader = urlopen(TRIPIT_ICAL_URL)
ical = ical_reader.read()

# Setup data.
today = datetime.date.today()
current_location_start = today
current_location = TRIPIT_HOME
next_location = TRIPIT_HOME

# Parse the calendar stream.
cal = Calendar.from_ical(ical)
for event in cal.walk('vevent'):
    dtstart = event.get('dtstart').dt
    dtend = event.get('dtend').dt
    location = event.get('location')
    summary = event.get('summary')


    # Trips only have dates, not times.
    if isinstance(dtstart, datetime.date) and not isinstance(dtstart, datetime.datetime):
        # If the trip has ended, ignore it.
        if today > dtend:
            continue;

        # If we're in the middle of a trip, set it as current.
        if dtstart <= today and today < dtend:
            current_location = location
            current_summary = summary
            current_location_start = dtstart
            current_location_end = dtend
            next_location_start = dtend

        # If we're seeing a future event
        if dtstart > today:
            # If coming from home, this is the next trip.
            if current_location == TRIPIT_HOME:
                next_summary = summary
                next_location = location
                next_location_start = dtstart
            # If coming from another trip that ends after or when this starts, this is next trip.
            elif current_location_end and current_location_end >= dtstart:
                next_summary = summary
                next_location = location
                next_location_start = dtstart
            break;


# Pretty format the status info and account for no upcoming trips.
# If I'm traveling, say where I'm at and how long I'll be there for.
if current_location != TRIPIT_HOME:
    status = 'Traveling {c.month}/{c.day} -> {n.month}/{n.day} for {summary}'.format(c=current_location_start, cloc=current_location, n=current_location_end, summary=current_summary)
    emoji = ':airplane:' or ''
# If I'm not traveling, use my default WFH status.
else:
    status = 'Working from home'
    emoji = ':house:' or ''


# Setup the Slack API info.
slack_url = 'https://slack.com/api/users.profile.set'
slack_profile = '{"status_text":"' + status + '", "status_emoji": "' + emoji + '"}'
slack_token = SLACK_API_TOKEN

# Post the status to Slack.
post_data = {'token': slack_token, 'profile': slack_profile}
req = Request(slack_url, urlencode(post_data).encode())
resp = urlopen(req)
if resp.status == 200:
    print('Status updated: ' + status)
else:
    print(resp.read())
