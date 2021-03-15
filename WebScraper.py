from bs4 import BeautifulSoup
import requests


def get_html(url):
    """Get the html code a the page given by the url in a BeautifulSoup Object

    :param url: str which is a valid url
    :return: The html code of the page url
    """
    html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 '
                                                    'Firefox/10.0 '})  # Need a header to avoid response 503
    return BeautifulSoup(html.text, features="html.parser")


def get_info_matches(matches_url):
    """From each next matches url, return a list of dictionnary fill with information of upcoming event.

    :param matches_url: A list of url for each following matches
    :return: A list of dictionary with essential info
    (ex : [{'team1': ['Vitality'], 'team2': ['FaZe'], 'time': datetime.datetime(2021, ...), 'url': 'https...'}, {...}])
    """
    info_matches = []
    for match_url in matches_url:
        match_html = get_html(match_url)
        teams = match_html.findAll('div', {'class': 'teamName'})  # Find teams name
        time = int(match_html.find('div', {'class': 'time'})['data-unix'][:-3])  # Find time

        info_matches.append({'team1': teams[0].contents[0], 'team2': teams[1].contents[0], 'time': time, 'url': match_url})

    return info_matches


def get_next_matches(team_name, team_number):
    """Scrape HTLV.org to get usefull information about next matches

    :param team_name: A str of the team name
    :param team_number: A str of the unique number given by HLTV to every team
    :return: A list of dictionary fill with information of next matches
    """
    team_url = f'https://www.hltv.org/team/{team_number}/{team_name}#tab-matchesBox'  # Url of the team we want matches info

    html_page = get_html(team_url)

    next_matches_url = ["https://www.hltv.org" + match['href'] for match in html_page.findAll('a', {'class': 'matchpage-button'})]

    return get_info_matches(next_matches_url)
