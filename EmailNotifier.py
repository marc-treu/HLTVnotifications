import copy
from datetime import datetime
import ezgmail


def format_date(matches):
    matches_copie = []  # matches.copy()
    for m in matches:
        m_copy = m.copy()
        m_copy['time'] = datetime.fromtimestamp(m_copy['time'])
        # m['time'] = datetime.fromtimestamp(m['time'])
        matches_copie.append(m_copy)
    return matches_copie  # [datetime.fromtimestamp(copy.deepcopy(m)['time']) for m in matches]


def format_hour(time):
    return f'{time.hour}H{time.minute:02d}'


def format_day(date):
    return date.isoformat()[:10]


def format_email(matches):
    """

    :param body: A list of dictionary fill with info of next matches
    :return: A well formatted
    """

    matches = format_date(matches)

    body = "<br>".join([f'<a href="{m["url"]}">{m["team1"]} vs {m["team2"]} on {format_day(m["time"])}</a>' for m in matches])
    html = f"""
    <html>
    <head></head>
      <body>pass
        {body}
      </body>
    </html>
    """

    day_left = (matches[0]['time'] - datetime.today()).days
    delay = "is {}".format(f'Today at {format_hour(matches[0]["time"])}' if day_left <= 0 else "in {} Day{}".format(day_left, "" if day_left == 1 else "s"))
    subject = f"[HLTV] {matches[0]['team1']} vs {matches[0]['team2']} {delay}"
    return html, subject


def send_email(recipient, new_info_matchs):
    """

    :param recipient:
    :param new_info_matchs:
    :return:
    """

    body, subject = format_email(new_info_matchs)
    ezgmail.send(recipient, subject, body, mimeSubtype='html')
    print('mail send')

