import json

from .EmailNotifier import send_email
from .IO import read, write
from .WebScraper import get_next_matches


"""
When the script is call it will:
    - Get the team to follow (Read in config.json)
    - Get information of upcoming events (Webscrapping from HLTV.org)
    - If there is new info, send an email to the given recipient
      If not, it will end here 

This script is designed to be used with cron job to stay inform about following matches of your favorite team
"""


def is_different(new_list, old_list):
    """Verify if there is any change or news in the upcoming events"""
    new_list_s = sorted(new_list, key=lambda k: k['time'])
    old_list_s = sorted(old_list, key=lambda k: k['time'])
    return new_list_s != old_list_s


def main():

    with open('config.json') as json_file:  # Get information about team and recipient mail
        config = json.load(json_file)

    new_info_matchs = get_next_matches(config['team'], config['number'])  # get a dictionary that containt infos of next matchs

    if not new_info_matchs:  # If there is no following match
        exit()

    previous_info_matchs = read()  # Read previous info we got

    if is_different(previous_info_matchs, new_info_matchs):  # if there is any change in the shedule
        send_email(config['mail'], new_info_matchs)  # Send well formated email
        write(new_info_matchs)  # write down new info


if __name__ == '__main__':
    main()
