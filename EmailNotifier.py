from datetime import datetime
import ezgmail


def format_date(matches):
    """Convert the date from int to datetime.Object"""
    matches_copies = []
    for m in matches:
        m_copy = m.copy()
        m_copy['time'] = datetime.fromtimestamp(m_copy['time'])
        matches_copies.append(m_copy)
    return matches_copies


def format_hour(time):
    """Return a str easier to read, of the time of the match"""
    return f'{time.hour}H{time.minute:02d}'


def format_day(date):
    """Return a str easier to read, of the date of the match"""
    return date.isoformat()[:10]


def format_email(matches):
    """Return the subject and email content with the information of upcoming events.
    We use html to format the mail (making hyperlink).

    :param matches: A list of dictionary fill with information of next matches
    :return: A well formatted email body and subject
    """
    matches = format_date(matches)

    body = "<br>".join([f'<a href="{m["url"]}">{m["team1"]} vs {m["team2"]} on {format_day(m["time"])}</a>' for m in matches])
    html = f"""
    <html>
    <head></head>
      <body>
        <h3>Upcoming matches for {matches[0]['team1']}</h3>
        <br>
        {body}
      </body>
    </html>
    """

    day_left = (matches[0]['time'] - datetime.today()).days
    delay = "is {}".format(f'Today at {format_hour(matches[0]["time"])}' if day_left <= 0 else "in {} Day{}".format(day_left, "" if day_left == 1 else "s"))
    subject = f"[HLTV] {matches[0]['team1']} vs {matches[0]['team2']} {delay}"
    return html, subject


def send_email(recipient, new_info_matches):
    """Send a email with ezgmail library (with a gmail account) with information of following matches

    :param recipient: A str with the recipient email address
    :param new_info_matches: A list of dict fill with information of upcoming matches
    """

    body, subject = format_email(new_info_matches)
    ezgmail.send(recipient, subject, body, mimeSubtype='html')
    print('mail send')

