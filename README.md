# Tripit Slack Status Updater
---

I travel a lot. In fact I'm a nomad, so I'm always on a trip somewhere, since I have no home. This makes it hard for coworkers to track where I am. But thankfully, I use [Tripit](https://www.tripit.com) to manage all of my travels and, while their API is crap, they allow me to publish my travels as an iCal file (.ics). This script takes my current location and my next upcoming location and publishes them to my Slack status.

## Setup

Add the following variables to your `tripit-slack-status.py` starting at line 6:

| Var | Description |
| --- | --- |
| `TRIPIT_ICAL_URL` | **Required.** Your Tripit calendar is available from [your publishing settings](https://www.tripit.com/account/edit/section/publishing_options). Click the "Subscribe" link in the Calendar Feed section, then click the "Subscribe to calendar feed" option. |
| `SLACK_API_TOKEN` | **Required.** Generate a [Slack legacy token](https://api.slack.com/custom-integrations/legacy-tokens). Your token will begin with `xoxp-`. |
| `TRIPIT_HOME` | **Required.** Your home location. |

You may also want to change your default "at home" status on line 64, as well as the emoji, and the specific format of the statuses in this section.

Next, install the `icalendar` library:
`pip install -r requirements.txt`

Then run the script:
`python tripit-slack-status.py`

Ideally, you'll want to run the script on a schedule. Once daily is probably enough, since it only checks for Trips, not individual plans.
