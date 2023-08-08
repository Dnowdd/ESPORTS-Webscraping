from pathlib import Path
import requests
from bs4 import BeautifulSoup
from tkinter import *
import webbrowser
from datetime import datetime, timedelta
import os

atual_directory = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(os.path.join(atual_directory, "assets", "frame0"))

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

window.title("Esports Webscraping")
window.iconbitmap(os.path.join(atual_directory, "assets/resources/icon.ico"))
window.geometry("1600x865")
window.configure(bg = "#17192D")

url = 'https://maisesports.com.br/'
language_code = 'br'

response = requests.get(url)
pageSoup = BeautifulSoup(response.text, 'html.parser')

def change_cursor(event):
    canvas.config(cursor="hand2")

def restore_cursor(event):
    canvas.config(cursor="")

def convert_to_brasilia_time(date_string):
    if date_string != 0:
        if(language_code == 'br'):
            date_format = "%d/%m %H:%M"
            date = datetime.strptime(str(date_string), date_format)

            brasilia_offset = timedelta(hours=3)
            current_time = datetime.now()
            difference = current_time - date

            if date.hour < 3 and difference.days == 0:
                # Retroceder um dia
                date -= timedelta(days=1)

            brasilia_time = date - brasilia_offset

            brasilia_time_string = brasilia_time.strftime(date_format)
            return brasilia_time_string
        else:
            parts = date_string.split()
            data_parts = parts[0].split('/')
            new_data = f"{data_parts[1]}/{data_parts[0]} {parts[1]}"
            return new_data
    else:
        return ''

def nextMatchs(i, multi):
    lastMatchs = pageSoup.find_all('div', class_='sc-973586-1')
    lastMatchs = lastMatchs[1]
    lastMatchsHtml = lastMatchs.prettify()

    lastMatchsSoup = BeautifulSoup(lastMatchsHtml, 'html.parser')
    matchs = lastMatchsSoup.find_all('a', class_='sc-973586-7')

    def getMatchInfos(match):
        matchSoup = BeautifulSoup(match, 'html.parser')
        matchName = matchSoup.find('div', class_='sc-973586-13')
        matchTeams = matchSoup.find_all('div', class_='sc-973586-12')
        matchTeamsImage = matchSoup.find_all('img')

        matchTeamHomeImage = matchTeamsImage[2]['src']
        matchTeamAwayImage = matchTeamsImage[5]['src']

        if matchSoup.find('a', class_='jOmIEC'):
            game = 'League of Legends'
        elif matchSoup.find('a', class_='gDATmb'):
            game = 'Valorant'
        else:
            game = 'Undefined'

        if matchSoup.find('a', 'sc-973586-14'):
            live = 1
        else:
            live = 0

        if live == 0:
            matchDate = matchSoup.find('div', 'sc-973586-14').text.strip()
        else:
            matchDate = 0

        homeTeamName = matchTeams[0].text.strip().replace('LOUD', 'LLL').split('.')
        awayTeamName = matchTeams[1].text.strip().replace('LOUD', 'LLL').split('.')

        dados = {
            "game": game,
            "league": matchName.text.strip(),
            "hometeam": homeTeamName[0],
            "awayteam": awayTeamName[0],
            "live": live,
            "date": matchDate,
            "homeimage": 'https://maisesports.com.br'+matchTeamHomeImage+'/',
            "awayimage": 'https://maisesports.com.br'+matchTeamAwayImage+'/'
        }

        return dados

    return getMatchInfos(matchs[i].prettify())[multi]

def lastMatchs(i, multi):
    lastMatchs = pageSoup.find_all('div', class_='sc-973586-1')
    lastMatchs = lastMatchs[2]
    lastMatchsHtml = lastMatchs.prettify()

    lastMatchsSoup = BeautifulSoup(lastMatchsHtml, 'html.parser')
    matchs = lastMatchsSoup.find_all('a', class_='sc-973586-7')

    def getMatchInfos(match):
        matchSoup = BeautifulSoup(match, 'html.parser')
        matchName = matchSoup.find('div', class_='sc-973586-13')
        matchDate = matchSoup.find('div', class_='sc-973586-14')
        matchTeams = matchSoup.find_all('div', class_='sc-973586-12')
        matchScore = matchSoup.find_all('div', class_='sc-973586-21')
        matchTeamsImage = matchSoup.find_all('img')

        matchTeamHomeImage = matchTeamsImage[2]['src']
        matchTeamAwayImage = matchTeamsImage[5]['src']

        if matchSoup.find('a', class_='jOmIEC'):
            game = 'League of Legends'
        elif matchSoup.find('a', class_='gDATmb'):
            game = 'Valorant'
        else:
            game = 'Undefined'

        homeTeamName = matchTeams[0].text.strip().replace('LOUD', 'LLL').split('.')
        awayTeamName = matchTeams[1].text.strip().replace('LOUD', 'LLL').split('.')

        dados = {
            "game": game,
            "league": matchName.text.strip(),
            "date": matchDate.text.strip(),
            "hometeam": homeTeamName[0],
            "awayteam": awayTeamName[0],
            "homescore": matchScore[0].text.strip(),
            "awayscore": matchScore[1].text.strip(),
            "homeimage": 'https://maisesports.com.br'+matchTeamHomeImage+'/',
            "awayimage": 'https://maisesports.com.br'+matchTeamAwayImage+'/'
        }

        return dados

    return getMatchInfos(matchs[i].prettify())[multi]

def redirectGithub(event):
    webbrowser.open('https://github.com/dnowdd')

def redirectMaisesports(event):
    webbrowser.open('https://maisesports.com.br')

def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)

def sizeTeamName(str,mode):
    if mode == "last":
        if len(str) == 2:
            return 867
        else:
            return 837
    elif mode == "next":
        if len(str) == 2:
            return 1371
        else:
            return 1341
        
def verifyLive(live, color):
    if live == 1:
        return color
    else:
        return ""

def lastRefreshed_Phrase():
    if language_code == 'br':
        return 'Última vez atualizado em: '
    else:
        return 'Last updated: '

def click(event):
    global response
    global pageSoup
    response = requests.get(url)
    pageSoup = BeautifulSoup(response.text, 'html.parser')
    def refreshLast():
        #COORDENADAS DOS TEXTOS
        canvas.coords(last_awayteam3, (sizeTeamName(lastMatchs(3,'awayteam'), 'last')), canvas.coords(last_awayteam3)[1])
        canvas.coords(last_awayteam2, (sizeTeamName(lastMatchs(2,'awayteam'), 'last')), canvas.coords(last_awayteam2)[1])
        canvas.coords(last_awayteam1, (sizeTeamName(lastMatchs(1,'awayteam'), 'last')), canvas.coords(last_awayteam1)[1])
        canvas.coords(last_awayteam0, (sizeTeamName(lastMatchs(0,'awayteam'), 'last')), canvas.coords(last_awayteam0)[1])

        #MUDANÇAS DOS TEXTOS
        canvas.itemconfig(last_league3, text=(lastMatchs(3,'league')))
        canvas.itemconfig(last_league2, text=(lastMatchs(2,'league')))
        canvas.itemconfig(last_league1, text=(lastMatchs(1,'league')))
        canvas.itemconfig(last_league0, text=(lastMatchs(0,'league')))

        canvas.itemconfig(last_hometeam3, text=(lastMatchs(3,'hometeam')))
        canvas.itemconfig(last_hometeam2, text=(lastMatchs(2,'hometeam')))
        canvas.itemconfig(last_hometeam1, text=(lastMatchs(1,'hometeam')))
        canvas.itemconfig(last_hometeam0, text=(lastMatchs(0,'hometeam')))

        canvas.itemconfig(last_awayteam3, text=(lastMatchs(3,'awayteam')))
        canvas.itemconfig(last_awayteam2, text=(lastMatchs(2,'awayteam')))
        canvas.itemconfig(last_awayteam1, text=(lastMatchs(1,'awayteam')))
        canvas.itemconfig(last_awayteam0, text=(lastMatchs(0,'awayteam')))

        canvas.itemconfig(last_score3, text=(lastMatchs(3,'homescore'))+":"+(lastMatchs(3,'awayscore')))
        canvas.itemconfig(last_score2, text=(lastMatchs(2,'homescore'))+":"+(lastMatchs(2,'awayscore')))
        canvas.itemconfig(last_score1, text=(lastMatchs(1,'homescore'))+":"+(lastMatchs(1,'awayscore')))
        canvas.itemconfig(last_score0, text=(lastMatchs(0,'homescore'))+":"+(lastMatchs(0,'awayscore')))

        canvas.itemconfig(last_date3, text=(convert_to_brasilia_time(lastMatchs(3,'date'))))
        canvas.itemconfig(last_date2, text=(convert_to_brasilia_time(lastMatchs(2,'date'))))
        canvas.itemconfig(last_date1, text=(convert_to_brasilia_time(lastMatchs(1,'date'))))
        canvas.itemconfig(last_date0, text=(convert_to_brasilia_time(lastMatchs(0,'date'))))

        canvas.itemconfig(last_game3, text=(lastMatchs(3,'game')))
        canvas.itemconfig(last_game2, text=(lastMatchs(2,'game')))
        canvas.itemconfig(last_game1, text=(lastMatchs(1,'game')))
        canvas.itemconfig(last_game0, text=(lastMatchs(0,'game')))

        updateHomeIcon3 = requests.get(lastMatchs(3,'homeimage'))
        updateHomeIcon3 = updateHomeIcon3.content
        updateHomeIcon3 = PhotoImage(data=updateHomeIcon3)
        updateHomeIcon3 = updateHomeIcon3.subsample(2)
        homeTeam3.configure(image=updateHomeIcon3)
        homeTeam3.image = updateHomeIcon3
        #---------
        updateHomeIcon2 = requests.get(lastMatchs(2,'homeimage'))
        updateHomeIcon2 = updateHomeIcon2.content
        updateHomeIcon2 = PhotoImage(data=updateHomeIcon2)
        updateHomeIcon2 = updateHomeIcon2.subsample(2)
        homeTeam2.configure(image=updateHomeIcon2)
        homeTeam2.image = updateHomeIcon2
        #---------
        updateHomeIcon1 = requests.get(lastMatchs(1,'homeimage'))
        updateHomeIcon1 = updateHomeIcon1.content
        updateHomeIcon1 = PhotoImage(data=updateHomeIcon1)
        updateHomeIcon1 = updateHomeIcon1.subsample(2)
        homeTeam1.configure(image=updateHomeIcon1)
        homeTeam1.image = updateHomeIcon1
        #---------
        updateHomeIcon0 = requests.get(lastMatchs(0,'homeimage'))
        updateHomeIcon0 = updateHomeIcon0.content
        updateHomeIcon0 = PhotoImage(data=updateHomeIcon0)
        updateHomeIcon0 = updateHomeIcon0.subsample(2)
        homeTeam0.configure(image=updateHomeIcon0)
        homeTeam0.image = updateHomeIcon0
        

        updateAwayIcon3 = requests.get(lastMatchs(3,'awayimage'))
        updateAwayIcon3 = updateAwayIcon3.content
        updateAwayIcon3 = PhotoImage(data=updateAwayIcon3)
        updateAwayIcon3 = updateAwayIcon3.subsample(2)
        awayTeam3.configure(image=updateAwayIcon3)
        awayTeam3.image = updateAwayIcon3
        #---------
        updateAwayIcon2 = requests.get(lastMatchs(2,'awayimage'))
        updateAwayIcon2 = updateAwayIcon2.content
        updateAwayIcon2 = PhotoImage(data=updateAwayIcon2)
        updateAwayIcon2 = updateAwayIcon2.subsample(2)
        awayTeam2.configure(image=updateAwayIcon2)
        awayTeam2.image = updateAwayIcon2
        #---------
        updateAwayIcon1 = requests.get(lastMatchs(1,'awayimage'))
        updateAwayIcon1 = updateAwayIcon1.content
        updateAwayIcon1 = PhotoImage(data=updateAwayIcon1)
        updateAwayIcon1 = updateAwayIcon1.subsample(2)
        awayTeam1.configure(image=updateAwayIcon1)
        awayTeam1.image = updateAwayIcon1
        #---------
        updateAwayIcon0 = requests.get(lastMatchs(0,'awayimage'))
        updateAwayIcon0 = updateAwayIcon0.content
        updateAwayIcon0 = PhotoImage(data=updateAwayIcon0)
        updateAwayIcon0 = updateAwayIcon0.subsample(2)
        awayTeam0.configure(image=updateAwayIcon0)
        awayTeam0.image = updateAwayIcon0

    def refreshNext():
        #COORDENADAS DOS TEXTOS
        canvas.coords(next_awayteam3, (sizeTeamName(nextMatchs(3,'awayteam'), 'next')), canvas.coords(next_awayteam3)[1])
        canvas.coords(next_awayteam2, (sizeTeamName(nextMatchs(2,'awayteam'), 'next')), canvas.coords(next_awayteam2)[1])
        canvas.coords(next_awayteam1, (sizeTeamName(nextMatchs(1,'awayteam'), 'next')), canvas.coords(next_awayteam1)[1])
        canvas.coords(next_awayteam0, (sizeTeamName(nextMatchs(0,'awayteam'), 'next')), canvas.coords(next_awayteam0)[1])

        #MUDANÇAS DOS TEXTOS
        canvas.itemconfig(next_league3, text=(nextMatchs(3,'league')))
        canvas.itemconfig(next_league2, text=(nextMatchs(2,'league')))
        canvas.itemconfig(next_league1, text=(nextMatchs(1,'league')))
        canvas.itemconfig(next_league0, text=(nextMatchs(0,'league')))

        canvas.itemconfig(next_hometeam3, text=(nextMatchs(3,'hometeam')))
        canvas.itemconfig(next_hometeam2, text=(nextMatchs(2,'hometeam')))
        canvas.itemconfig(next_hometeam1, text=(nextMatchs(1,'hometeam')))
        canvas.itemconfig(next_hometeam0, text=(nextMatchs(0,'hometeam')))

        canvas.itemconfig(next_awayteam3, text=(nextMatchs(3,'awayteam')))
        canvas.itemconfig(next_awayteam2, text=(nextMatchs(2,'awayteam')))
        canvas.itemconfig(next_awayteam1, text=(nextMatchs(1,'awayteam')))
        canvas.itemconfig(next_awayteam0, text=(nextMatchs(0,'awayteam')))

        canvas.itemconfig(next_date3, text=(convert_to_brasilia_time(nextMatchs(3,'date'))))
        canvas.itemconfig(next_date2, text=(convert_to_brasilia_time(nextMatchs(2,'date'))))
        canvas.itemconfig(next_date1, text=(convert_to_brasilia_time(nextMatchs(1,'date'))))
        canvas.itemconfig(next_date0, text=(convert_to_brasilia_time(nextMatchs(0,'date'))))

        canvas.itemconfig(next_game3, text=(nextMatchs(3,'game')))
        canvas.itemconfig(next_game2, text=(nextMatchs(2,'game')))
        canvas.itemconfig(next_game1, text=(nextMatchs(1,'game')))
        canvas.itemconfig(next_game0, text=(nextMatchs(0,'game')))

        canvas.itemconfig(next_live_box3, fill=(verifyLive(nextMatchs(3,'live'), '#FF4242')))
        canvas.itemconfig(next_live_text3, fill=(verifyLive(nextMatchs(3,'live'), '#FFFFFF')))
        canvas.itemconfig(next_live_circle3, fill=(verifyLive(nextMatchs(3,'live'), '#FFFFFF')))

        canvas.itemconfig(next_live_box2, fill=(verifyLive(nextMatchs(2,'live'), '#FF4242')))
        canvas.itemconfig(next_live_text2, fill=(verifyLive(nextMatchs(2,'live'), '#FFFFFF')))
        canvas.itemconfig(next_live_circle2, fill=(verifyLive(nextMatchs(2,'live'), '#FFFFFF')))

        canvas.itemconfig(next_live_box1, fill=(verifyLive(nextMatchs(1,'live'), '#FF4242')))
        canvas.itemconfig(next_live_text1, fill=(verifyLive(nextMatchs(1,'live'), '#FFFFFF')))
        canvas.itemconfig(next_live_circle1, fill=(verifyLive(nextMatchs(1,'live'), '#FFFFFF')))

        canvas.itemconfig(next_live_box0, fill=(verifyLive(nextMatchs(0,'live'), '#FF4242')))
        canvas.itemconfig(next_live_text0, fill=(verifyLive(nextMatchs(0,'live'), '#FFFFFF')))
        canvas.itemconfig(next_live_circle0, fill=(verifyLive(nextMatchs(0,'live'), '#FFFFFF')))

        nextupdateHomeIcon3 = requests.get(nextMatchs(3,'homeimage'))
        nextupdateHomeIcon3 = nextupdateHomeIcon3.content
        nextupdateHomeIcon3 = PhotoImage(data=nextupdateHomeIcon3)
        nextupdateHomeIcon3 = nextupdateHomeIcon3.subsample(2)
        nexthomeTeam3.configure(image=nextupdateHomeIcon3)
        nexthomeTeam3.image = nextupdateHomeIcon3
        #---------
        nextupdateHomeIcon2 = requests.get(nextMatchs(2,'homeimage'))
        nextupdateHomeIcon2 = nextupdateHomeIcon2.content
        nextupdateHomeIcon2 = PhotoImage(data=nextupdateHomeIcon2)
        nextupdateHomeIcon2 = nextupdateHomeIcon2.subsample(2)
        nexthomeTeam2.configure(image=nextupdateHomeIcon2)
        nexthomeTeam2.image = nextupdateHomeIcon2
        #---------
        nextupdateHomeIcon1 = requests.get(nextMatchs(1,'homeimage'))
        nextupdateHomeIcon1 = nextupdateHomeIcon1.content
        nextupdateHomeIcon1 = PhotoImage(data=nextupdateHomeIcon1)
        nextupdateHomeIcon1 = nextupdateHomeIcon1.subsample(2)
        nexthomeTeam1.configure(image=nextupdateHomeIcon1)
        nexthomeTeam1.image = nextupdateHomeIcon1
        #---------
        nextupdateHomeIcon0 = requests.get(nextMatchs(0,'homeimage'))
        nextupdateHomeIcon0 = nextupdateHomeIcon0.content
        nextupdateHomeIcon0 = PhotoImage(data=nextupdateHomeIcon0)
        nextupdateHomeIcon0 = nextupdateHomeIcon0.subsample(2)
        nexthomeTeam0.configure(image=nextupdateHomeIcon0)
        nexthomeTeam0.image = nextupdateHomeIcon0
        

        nextupdateAwayIcon3 = requests.get(nextMatchs(3,'awayimage'))
        nextupdateAwayIcon3 = nextupdateAwayIcon3.content
        nextupdateAwayIcon3 = PhotoImage(data=nextupdateAwayIcon3)
        nextupdateAwayIcon3 = nextupdateAwayIcon3.subsample(2)
        nextawayTeam3.configure(image=nextupdateAwayIcon3)
        nextawayTeam3.image = nextupdateAwayIcon3
        #---------
        nextupdateAwayIcon2 = requests.get(nextMatchs(2,'awayimage'))
        nextupdateAwayIcon2 = nextupdateAwayIcon2.content
        nextupdateAwayIcon2 = PhotoImage(data=nextupdateAwayIcon2)
        nextupdateAwayIcon2 = nextupdateAwayIcon2.subsample(2)
        nextawayTeam2.configure(image=nextupdateAwayIcon2)
        nextawayTeam2.image = nextupdateAwayIcon2
        #---------
        nextupdateAwayIcon1 = requests.get(nextMatchs(1,'awayimage'))
        nextupdateAwayIcon1 = nextupdateAwayIcon1.content
        nextupdateAwayIcon1 = PhotoImage(data=nextupdateAwayIcon1)
        nextupdateAwayIcon1 = nextupdateAwayIcon1.subsample(2)
        nextawayTeam1.configure(image=nextupdateAwayIcon1)
        nextawayTeam1.image = nextupdateAwayIcon1
        #---------
        nextupdateAwayIcon0 = requests.get(nextMatchs(0,'awayimage'))
        nextupdateAwayIcon0 = nextupdateAwayIcon0.content
        nextupdateAwayIcon0 = PhotoImage(data=nextupdateAwayIcon0)
        nextupdateAwayIcon0 = nextupdateAwayIcon0.subsample(2)
        nextawayTeam0.configure(image=nextupdateAwayIcon0)
        nextawayTeam0.image = nextupdateAwayIcon0

    def lastRefresh():
        now = datetime.now()
        future_hours = now + timedelta(hours=3)
        formated_data = future_hours.strftime("%d/%m %H:%M")

        canvas.itemconfig(textAtualizado, fill='#b0b0b0')
        canvas.itemconfig(textAtualizado, text=lastRefreshed_Phrase()+''+convert_to_brasilia_time(formated_data))

    refreshLast()
    refreshNext()
    lastRefresh()

def changeLanguage(language):
    def portuguese():
        one_phrase_portuguese = "Esse projeto foi desenvolvido por"
        three_phrase_portuguese = "Ele consiste em um sistema que"
        four_phrase_portuguese = "captura informações de esports"
        five_phrase_portuguese = "utilizando webscraping do site"
        seven_phrase_portuguese = "Dentre os jogos possíveis para"
        eight_phrase_portuguese = "informação estão: LoL, CS:GO,"
        nine_phrase_portuguese = "Valorant, CS 2, Free fire, entre"
        ten_phrase_portuguese = "outros."
        phrase_refresh = "ATUALIZAR"
        phrase_nextMatchs = "Partidas futuras"
        phrase_lastMatchs = "Partidas recentes"
        phrase_live = "AO VIVO"

        canvas.itemconfig(one_phrase, text=one_phrase_portuguese)
        canvas.itemconfig(three_phrase, text=three_phrase_portuguese)
        canvas.itemconfig(four_phrase, text=four_phrase_portuguese)
        canvas.itemconfig(five_phrase, text=five_phrase_portuguese)
        canvas.itemconfig(seven_phrase, text=seven_phrase_portuguese)
        canvas.itemconfig(eight_phrase, text=eight_phrase_portuguese)
        canvas.itemconfig(nine_phrase, text=nine_phrase_portuguese)
        canvas.itemconfig(ten_phrase, text=ten_phrase_portuguese)
        canvas.itemconfig(textAtualizar, text=phrase_refresh)
        canvas.itemconfig(nextMatches_phrase, text=phrase_nextMatchs)
        canvas.itemconfig(lastMatches_phrase, text=phrase_lastMatchs)
        canvas.itemconfig(next_live_text3, text=phrase_live)
        canvas.itemconfig(next_live_text2, text=phrase_live)
        canvas.itemconfig(next_live_text1, text=phrase_live)
        canvas.itemconfig(next_live_text0, text=phrase_live)
    def english():
        one_phrase_english = "This project was developed by"
        three_phrase_english = "It consists of a system that"
        four_phrase_english = "captures esports information"
        five_phrase_english = "using web scraping from the website"
        seven_phrase_english = "Among the possible games for"
        eight_phrase_english = "information are: Lol, CS:GO,"
        nine_phrase_english = "Valorant, CS 2, Free fire, among"
        ten_phrase_english = "others."
        phrase_refresh = "REFRESH"
        phrase_nextMatchs = "Future matches"
        phrase_lastMatchs = "Recent matches"
        phrase_live = "LIVE"

        canvas.itemconfig(one_phrase, text=one_phrase_english)
        canvas.itemconfig(three_phrase, text=three_phrase_english)
        canvas.itemconfig(four_phrase, text=four_phrase_english)
        canvas.itemconfig(five_phrase, text=five_phrase_english)
        canvas.itemconfig(seven_phrase, text=seven_phrase_english)
        canvas.itemconfig(eight_phrase, text=eight_phrase_english)
        canvas.itemconfig(nine_phrase, text=nine_phrase_english)
        canvas.itemconfig(ten_phrase, text=ten_phrase_english)
        canvas.itemconfig(textAtualizar, text=phrase_refresh)
        canvas.itemconfig(nextMatches_phrase, text=phrase_nextMatchs)
        canvas.itemconfig(lastMatches_phrase, text=phrase_lastMatchs)
        canvas.itemconfig(next_live_text3, text=phrase_live)
        canvas.itemconfig(next_live_text2, text=phrase_live)
        canvas.itemconfig(next_live_text1, text=phrase_live)
        canvas.itemconfig(next_live_text0, text=phrase_live)
    
    global language_code
    if language == 'english':
        english()
        language_code = 'us'
        click('')
    else:
        portuguese()
        language_code = 'br'
        click('')

canvas = Canvas(
    window,
    bg = "#17192D",
    height = 865,
    width = 1600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

# BG
canvas.create_rectangle(
    0.0,
    0.0,
    1600.0,
    1031.6666259765625,
    fill="#2B2E4A",
    outline="")

# BG OVERLAY
canvas.create_oval(1350, 1350, -3050, -2950, outline="", fill="#17192D")

# PARTIDAS FUTURAS
round_rectangle(1056.1484375, 228.3333282470703, 1507.1925048828125, 781.6666412353516, radius=45, fill="#53354A")

# PARTIDAS PASSADAS
round_rectangle(558.7006835937501, 228.3333282470703, 1009.7447509765626, 781.6666412353516, radius=45, fill="#53354A")

titulo = canvas.create_text(
    93.00000000000011,
    83.0,
    anchor="nw",
    text="ESPORTS WebScraping",
    fill="#E84545",
    font=("RobotoRoman Black", 103 * -1, 'bold')
)

last_league3 = canvas.create_text(
    600.0000000000001,
    671.0,
    anchor="nw",
    text=(lastMatchs(3,'league')),
    fill="#A73131",
    font=("RobotoRoman ExtraBold", 28 * -1, 'bold')
)

last_game3 = canvas.create_text(
    600.4641113281251,
    662.0,
    anchor="nw",
    text=(lastMatchs(3,'game')),
    fill="#FF9393",
    font=("Roboto", 12 * -1)
)

last_hometeam3 = canvas.create_text(
    655.4641113281251,
    709.0,
    anchor="nw",
    text=(lastMatchs(3,'hometeam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

last_score3 = canvas.create_text(
    765.4641113281251,
    714.0,
    anchor="nw",
    text=(lastMatchs(3,'homescore')+":"+(lastMatchs(3,'awayscore'))),
    fill="#E53636",
    font=("RobotoRoman Light", 28 * -1)
)

last_awayteam3 = canvas.create_text(
    sizeTeamName(lastMatchs(3,'awayteam'), 'last'),
    709.0,
    anchor="nw",
    text=(lastMatchs(3,'awayteam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

# HOME TEAM IMAGE 3
homeIcon3 = requests.get(lastMatchs(3,'homeimage'))
homeIcon3 = homeIcon3.content
homeIcon3 = PhotoImage(data=homeIcon3)
homeIcon3 = homeIcon3.subsample(2)
homeTeam3 = Label(window, image=homeIcon3, bg="#53354A")
homeTeam3.place(x = 605, y = 713)

# AWAY TEAM IMAGE 3
awayIcon3 = requests.get(lastMatchs(3,'awayimage'))
awayIcon3 = awayIcon3.content
awayIcon3 = PhotoImage(data=awayIcon3)
awayIcon3 = awayIcon3.subsample(2)
awayTeam3 = Label(window, image=awayIcon3, bg="#53354A")
awayTeam3.place(x = 933.4641113281251, y = 713)

last_date3 = canvas.create_text(
    880.9978027343751,
    676.0,
    anchor="nw",
    text=(convert_to_brasilia_time(lastMatchs(3,'date'))),
    fill="#9D8181",
    font=("RobotoRoman Regular", 17 * -1)
)

canvas.create_rectangle(
    582.8306274414064,
    646.6666870117188,
    985.6148681640626,
    646.6666870117188,
    fill="#000000",
    outline="")

last_league2 = canvas.create_text(
    600.0000000000001,
    545.0,
    anchor="nw",
    text=(lastMatchs(2,'league')),
    fill="#A73131",
    font=("RobotoRoman ExtraBold", 28 * -1, 'bold')
)

last_game2 = canvas.create_text(
    600.4641113281251,
    536.0,
    anchor="nw",
    text=(lastMatchs(2,'game')),
    fill="#FF9393",
    font=("RobotoRoman Thin", 12 * -1)
)

last_hometeam2 = canvas.create_text(
    655.4641113281251,
    583.0,
    anchor="nw",
    text=(lastMatchs(2,'hometeam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

last_score2 = canvas.create_text(
    765.4641113281251,
    588.0,
    anchor="nw",
    text=(lastMatchs(2,'homescore')+":"+(lastMatchs(2,'awayscore'))),
    fill="#E53636",
    font=("RobotoRoman Light", 28 * -1)
)

last_awayteam2 = canvas.create_text(
    sizeTeamName(lastMatchs(2,'awayteam'), 'last'),
    583.0,
    anchor="nw",
    text=(lastMatchs(2,'awayteam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

# HOME TEAM IMAGE 2
homeIcon2 = requests.get(lastMatchs(2,'homeimage'))
homeIcon2 = homeIcon2.content
homeIcon2 = PhotoImage(data=homeIcon2)
homeIcon2 = homeIcon2.subsample(2)
homeTeam2 = Label(window, image=homeIcon2, bg="#53354A")
homeTeam2.place(x = 605, y = 587)

# AWAY TEAM IMAGE 2
awayIcon2 = requests.get(lastMatchs(2,'awayimage'))
awayIcon2 = awayIcon2.content
awayIcon2 = PhotoImage(data=awayIcon2)
awayIcon2 = awayIcon2.subsample(2)
awayTeam2 = Label(window, image=awayIcon2, bg="#53354A")
awayTeam2.place(x = 933.4641113281251, y = 587)


last_date2 = canvas.create_text(
    880.9978027343751,
    550.0,
    anchor="nw",
    text=(convert_to_brasilia_time(lastMatchs(2,'date'))),
    fill="#9D8181",
    font=("RobotoRoman Regular", 17 * -1)
)

canvas.create_rectangle(
    582.8306274414064,
    520.0,
    985.6148681640626,
    520.0,
    fill="#000000",
    outline="")

last_league1 = canvas.create_text(
    600.0000000000001,
    418.0,
    anchor="nw",
    text=(lastMatchs(1,'league')),
    fill="#A73131",
    font=("RobotoRoman ExtraBold", 28 * -1, 'bold')
)

last_game1 = canvas.create_text(
    600.4641113281251,
    409.0,
    anchor="nw",
    text=(lastMatchs(1,'game')),
    fill="#FF9393",
    font=("RobotoRoman Thin", 12 * -1)
)

last_hometeam1 = canvas.create_text(
    655.4641113281251,
    456.0,
    anchor="nw",
    text=(lastMatchs(1,'hometeam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

last_score1 = canvas.create_text(
    765.4641113281251,
    461.0,
    anchor="nw",
    text=(lastMatchs(1,'homescore')+":"+(lastMatchs(1,'awayscore'))),
    fill="#E53636",
    font=("RobotoRoman Light", 28 * -1)
)

last_awayteam1 = canvas.create_text(
    sizeTeamName(lastMatchs(1,'awayteam'), 'last'),
    456.0,
    anchor="nw",
    text=(lastMatchs(1,'awayteam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

# HOME TEAM IMAGE 1
homeIcon1 = requests.get(lastMatchs(1,'homeimage'))
homeIcon1 = homeIcon1.content
homeIcon1 = PhotoImage(data=homeIcon1)
homeIcon1 = homeIcon1.subsample(2)
homeTeam1 = Label(window, image=homeIcon1, bg="#53354A")
homeTeam1.place(x = 605, y = 460)

# AWAY TEAM IMAGE 1
awayIcon1 = requests.get(lastMatchs(1,'awayimage'))
awayIcon1 = awayIcon1.content
awayIcon1 = PhotoImage(data=awayIcon1)
awayIcon1 = awayIcon1.subsample(2)
awayTeam1 = Label(window, image=awayIcon1, bg="#53354A")
awayTeam1.place(x = 933.4641113281251, y = 460)



last_date1 = canvas.create_text(
    880.9978027343751,
    423.0,
    anchor="nw",
    text=(convert_to_brasilia_time(lastMatchs(1,'date'))),
    fill="#9D8181",
    font=("RobotoRoman Regular", 17 * -1)
)

canvas.create_rectangle(
    582.8306274414064,
    393.3333435058594,
    985.6148681640626,
    393.3333435058594,
    fill="#000000",
    outline="")

last_league0 = canvas.create_text(
    599.5359497070314,
    291.6666564941406,
    anchor="nw",
    text=(lastMatchs(0,'league')),
    fill="#A73131",
    font=("RobotoRoman ExtraBold", 28 * -1, 'bold')
)

last_game0 = canvas.create_text(
    600.0000000000001,
    282.0,
    anchor="nw",
    text=(lastMatchs(0,'game')),
    fill="#FF9393",
    font=("RobotoRoman Thin", 12 * -1)
)

last_hometeam0 = canvas.create_text(
    655.0000000000001,
    329.0,
    anchor="nw",
    text=(lastMatchs(0,'hometeam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

last_score0 = canvas.create_text(
    765.0000000000001,
    334.0,
    anchor="nw",
    text=(lastMatchs(0,'homescore')+":"+(lastMatchs(0,'awayscore'))),
    fill="#E53636",
    font=("RobotoRoman Light", 28 * -1)
)

last_awayteam0 = canvas.create_text(
    sizeTeamName(lastMatchs(0,'awayteam'), 'last'),
    329.0,
    anchor="nw",
    text=(lastMatchs(0,'awayteam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

# HOME TEAM IMAGE 0
homeIcon0 = requests.get(lastMatchs(0,'homeimage'))
homeIcon0 = homeIcon0.content
homeIcon0 = PhotoImage(data=homeIcon0)
homeIcon0 = homeIcon0.subsample(2)
homeTeam0 = Label(window, image=homeIcon0, bg="#53354A")
homeTeam0.place(x = 605, y = 333)


# AWAY TEAM IMAGE 0
awayIcon0 = requests.get(lastMatchs(0,'awayimage'))
awayIcon0 = awayIcon0.content
awayIcon0 = PhotoImage(data=awayIcon0)
awayIcon0 = awayIcon0.subsample(2)
awayTeam0 = Label(window, image=awayIcon0, bg="#53354A")
awayTeam0.place(x = 933.4641113281251, y = 333)




last_date0 = canvas.create_text(
    880.5336914062501,
    296.0,
    anchor="nw",
    text=(convert_to_brasilia_time(lastMatchs(0,'date'))),
    fill="#9D8181",
    font=("RobotoRoman Regular", 17 * -1)
)

lastMatches_phrase = canvas.create_text(
    600.0000000000001,
    240.0,
    anchor="nw",
    text="Partidas recentes",
    fill="#FFFFFF",
    font=("RobotoRoman Black", 31 * -1, 'bold')
)

next_league3 = canvas.create_text(
    1098.0,
    671.0,
    anchor="nw",
    text=(nextMatchs(3,'league')),
    fill="#A73131",
    font=("RobotoRoman ExtraBold", 28 * -1, 'bold')
)

next_game3 = canvas.create_text(
    1098.0,
    662.0,
    anchor="nw",
    text=(nextMatchs(3,'game')),
    fill="#FF9393",
    font=("RobotoRoman Thin", 12 * -1)
)

next_hometeam3 = canvas.create_text(
    1153.0,
    709.0,
    anchor="nw",
    text=(nextMatchs(3,'hometeam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

next_score3 = canvas.create_text(
    1263.0,
    714.0,
    anchor="nw",
    text="vs.",
    fill="#E53636",
    font=("RobotoRoman Light", 28 * -1)
)

next_awayteam3 = canvas.create_text(
    sizeTeamName(nextMatchs(3,'awayteam'), 'next'),
    709.0,
    anchor="nw",
    text=(nextMatchs(3,'awayteam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

# HOME TEAM IMAGE 3 NEXT
nexthomeIcon3 = requests.get(nextMatchs(3,'homeimage'))
nexthomeIcon3 = nexthomeIcon3.content
nexthomeIcon3 = PhotoImage(data=nexthomeIcon3)
nexthomeIcon3 = nexthomeIcon3.subsample(2)
nexthomeTeam3 = Label(window, image=nexthomeIcon3, bg="#53354A")
nexthomeTeam3.place(x = 1103, y = 713)

# AWAY TEAM IMAGE 3 NEXT
nextawayIcon3 = requests.get(nextMatchs(3,'awayimage'))
nextawayIcon3 = nextawayIcon3.content
nextawayIcon3 = PhotoImage(data=nextawayIcon3)
nextawayIcon3 = nextawayIcon3.subsample(2)
nextawayTeam3 = Label(window, image=nextawayIcon3, bg="#53354A")
nextawayTeam3.place(x = 1431, y = 713)

next_date3 = canvas.create_text(
    1379.0,
    676.0,
    anchor="nw",
    text=(convert_to_brasilia_time(nextMatchs(3,'date'))),
    fill="#9D8181",
    font=("RobotoRoman Regular", 17 * -1)
)
# CAIXA DE AO VIVO
next_live_box3 = round_rectangle(1329, 676, 1470, 703, radius=20, fill=(verifyLive(nextMatchs(3,'live'), '#FF4242')))
next_live_text3 = canvas.create_text(
    1381.0,
    680.0,
    anchor="nw",
    text="AO VIVO",
    fill=(verifyLive(nextMatchs(3,'live'), '#FFFFFF')),
    font=("RobotoRoman Regular", 16 * -1, 'bold')
)
# CÍCULO DO AO VIVO
next_live_circle3 = canvas.create_oval(1358, 681, 1375, 698, outline="", fill=(verifyLive(nextMatchs(3,'live'), '#FFFFFF')))




canvas.create_rectangle(
    1081.0,
    646.6666870117188,
    1483.7841796875,
    646.6666870117188,
    fill="#000000",
    outline="")

next_league2 = canvas.create_text(
    1098.0,
    545.0,
    anchor="nw",
    text=(nextMatchs(2,'league')),
    fill="#A73131",
    font=("RobotoRoman ExtraBold", 28 * -1, 'bold')
)

next_game2 = canvas.create_text(
    1098.0,
    536.0,
    anchor="nw",
    text=(nextMatchs(2,'game')),
    fill="#FF9393",
    font=("RobotoRoman Thin", 12 * -1)
)

next_hometeam2 = canvas.create_text(
    1153.0,
    583.0,
    anchor="nw",
    text=(nextMatchs(2,'hometeam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

next_score2 = canvas.create_text(
    1263.0,
    588.0,
    anchor="nw",
    text="vs.",
    fill="#E53636",
    font=("RobotoRoman Light", 28 * -1)
)

next_awayteam2 = canvas.create_text(
    sizeTeamName(nextMatchs(2,'awayteam'), 'next'),
    583.0,
    anchor="nw",
    text=(nextMatchs(2,'awayteam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

# HOME TEAM IMAGE 2 NEXT
nexthomeIcon2 = requests.get(nextMatchs(2,'homeimage'))
nexthomeIcon2 = nexthomeIcon2.content
nexthomeIcon2 = PhotoImage(data=nexthomeIcon2)
nexthomeIcon2 = nexthomeIcon2.subsample(2)
nexthomeTeam2 = Label(window, image=nexthomeIcon2, bg="#53354A")
nexthomeTeam2.place(x = 1103, y = 587)

# AWAY TEAM IMAGE 2 NEXT
nextawayIcon2 = requests.get(nextMatchs(2,'awayimage'))
nextawayIcon2 = nextawayIcon2.content
nextawayIcon2 = PhotoImage(data=nextawayIcon2)
nextawayIcon2 = nextawayIcon2.subsample(2)
nextawayTeam2 = Label(window, image=nextawayIcon2, bg="#53354A")
nextawayTeam2.place(x = 1431, y = 587)


next_date2 = canvas.create_text(
    1379.0,
    550.0,
    anchor="nw",
    text=(convert_to_brasilia_time(nextMatchs(2,'date'))),
    fill="#9D8181",
    font=("RobotoRoman Regular", 17 * -1)
)
# CAIXA DE AO VIVO
next_live_box2 = round_rectangle(1329, 550, 1470, 577, radius=20, fill=(verifyLive(nextMatchs(2,'live'), '#FF4242')))
next_live_text2 = canvas.create_text(
    1381.0,
    554.0,
    anchor="nw",
    text="AO VIVO",
    fill=(verifyLive(nextMatchs(2,'live'), '#FFFFFF')),
    font=("RobotoRoman Regular", 16 * -1, 'bold')
)
# CÍCULO DO AO VIVO
next_live_circle2 = canvas.create_oval(1358, 555, 1375, 572, outline="", fill=(verifyLive(nextMatchs(2,'live'), '#FFFFFF')))





canvas.create_rectangle(
    1081.0,
    520.0,
    1483.7841796875,
    520.0,
    fill="#000000",
    outline="")

next_league1 = canvas.create_text(
    1098.0,
    418.0,
    anchor="nw",
    text=(nextMatchs(1,'league')),
    fill="#A73131",
    font=("RobotoRoman ExtraBold", 28 * -1, 'bold')
)

next_game1 = canvas.create_text(
    1098.0,
    409.0,
    anchor="nw",
    text=(nextMatchs(1,'game')),
    fill="#FF9393",
    font=("RobotoRoman Thin", 12 * -1)
)

next_hometeam1 = canvas.create_text(
    1153.0,
    456.0,
    anchor="nw",
    text=(nextMatchs(1,'hometeam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

next_score1 = canvas.create_text(
    1263.0,
    461.0,
    anchor="nw",
    text="vs.",
    fill="#E53636",
    font=("RobotoRoman Light", 28 * -1)
)

next_awayteam1 = canvas.create_text(
    sizeTeamName(nextMatchs(1,'awayteam'), 'next'),
    456.0,
    anchor="nw",
    text=(nextMatchs(1,'awayteam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

# HOME TEAM IMAGE 1 NEXT
nexthomeIcon1 = requests.get(nextMatchs(1,'homeimage'))
nexthomeIcon1 = nexthomeIcon1.content
nexthomeIcon1 = PhotoImage(data=nexthomeIcon1)
nexthomeIcon1 = nexthomeIcon1.subsample(2)
nexthomeTeam1 = Label(window, image=nexthomeIcon1, bg="#53354A")
nexthomeTeam1.place(x = 1103, y = 460)

# AWAY TEAM IMAGE 1 NEXT
nextawayIcon1 = requests.get(nextMatchs(1,'awayimage'))
nextawayIcon1 = nextawayIcon1.content
nextawayIcon1 = PhotoImage(data=nextawayIcon1)
nextawayIcon1 = nextawayIcon1.subsample(2)
nextawayTeam1 = Label(window, image=nextawayIcon1, bg="#53354A")
nextawayTeam1.place(x = 1431, y = 460)


next_date1 = canvas.create_text(
    1379.0,
    423.0,
    anchor="nw",
    text=(convert_to_brasilia_time(nextMatchs(1,'date'))),
    fill="#9D8181",
    font=("RobotoRoman Regular", 17 * -1)
)
# CAIXA DE AO VIVO
next_live_box1 = round_rectangle(1329, 423, 1470, 450, radius=20, fill=(verifyLive(nextMatchs(1,'live'), '#FF4242')))
next_live_text1 = canvas.create_text(
    1381.0,
    427.0,
    anchor="nw",
    text="AO VIVO",
    fill=(verifyLive(nextMatchs(1,'live'), '#FFFFFF')),
    font=("RobotoRoman Regular", 16 * -1, 'bold')
)
# CÍCULO DO AO VIVO
next_live_circle1 = canvas.create_oval(1358, 428, 1375, 445, outline="", fill=(verifyLive(nextMatchs(1,'live'), '#FFFFFF')))



canvas.create_rectangle(
    1081.0,
    393.3333435058594,
    1483.7841796875,
    393.3333435058594,
    fill="#000000",
    outline="")

next_league0 = canvas.create_text(
    1098.0,
    291.6666564941406,
    anchor="nw",
    text=(nextMatchs(0,'league')),
    fill="#A73131",
    font=("RobotoRoman ExtraBold", 28 * -1, 'bold')
)

next_game0 = canvas.create_text(
    1098.0,
    282.0,
    anchor="nw",
    text=(nextMatchs(0,'game')),
    fill="#FF9393",
    font=("RobotoRoman Thin", 12 * -1)
)

next_hometeam0 = canvas.create_text(
    1153.0,
    329.0,
    anchor="nw",
    text=(nextMatchs(0,'hometeam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

next_score0 = canvas.create_text(
    1263.0,
    334.0,
    anchor="nw",
    text="vs.",
    fill="#E53636",
    font=("RobotoRoman Light", 28 * -1)
)

next_awayteam0 = canvas.create_text(
    sizeTeamName(nextMatchs(0,'awayteam'), 'next'),
    329.0,
    anchor="nw",
    text=(nextMatchs(0,'awayteam')),
    fill="#FF9696",
    font=("RobotoRoman ExtraBold", 37 * -1, 'bold')
)

# HOME TEAM IMAGE 0 NEXT
nexthomeIcon0 = requests.get(nextMatchs(0,'homeimage'))
nexthomeIcon0 = nexthomeIcon0.content
nexthomeIcon0 = PhotoImage(data=nexthomeIcon0)
nexthomeIcon0 = nexthomeIcon0.subsample(2)
nexthomeTeam0 = Label(window, image=nexthomeIcon0, bg="#53354A")
nexthomeTeam0.place(x = 1103, y = 333)

# AWAY TEAM IMAGE 0 NEXT
nextawayIcon0 = requests.get(nextMatchs(0,'awayimage'))
nextawayIcon0 = nextawayIcon0.content
nextawayIcon0 = PhotoImage(data=nextawayIcon0)
nextawayIcon0 = nextawayIcon0.subsample(2)
nextawayTeam0 = Label(window, image=nextawayIcon0, bg="#53354A")
nextawayTeam0.place(x = 1431, y = 333)


nextMatches_phrase = canvas.create_text(
    1098.0,
    240.0,
    anchor="nw",
    text="Partidas futuras",
    fill="#FFFFFF",
    font=("RobotoRoman Black", 31 * -1, 'bold')
)





next_date0 = canvas.create_text(
    1379.0,
    293.0,
    anchor="nw",
    text=(convert_to_brasilia_time(nextMatchs(0,'date'))),
    fill="#9D8181",
    font=("RobotoRoman Regular", 17 * -1)
)
# CAIXA DE AO VIVO
next_live_box0 = round_rectangle(1329, 293, 1470, 320, radius=20, fill=(verifyLive(nextMatchs(0,'live'), '#FF4242')))
next_live_text0 = canvas.create_text(
    1381.0,
    297.0,
    anchor="nw",
    text="AO VIVO",
    fill=(verifyLive(nextMatchs(0,'live'), '#FFFFFF')),
    font=("RobotoRoman Regular", 16 * -1, 'bold')
)
# CÍCULO DO AO VIVO
next_live_circle0 = canvas.create_oval(1358, 298, 1375, 315, outline="", fill=(verifyLive(nextMatchs(0,'live'), '#FFFFFF')))





# BOTÃO ATUALIZAR
round_rectangle(92.80742645263683, 683.3333129882812, 514.1531295776368, 781.6666259765625, radius=35, fill="#53354A")

# ICON ATUALIZAR
refreshIcon = PhotoImage(file=os.path.join(atual_directory, "assets/resources/refresh.png"))
label_imagem = Label(window, image=refreshIcon, bg="#53354A").place(x = 160, y = 706)

textAtualizar = canvas.create_text(
    221.0000000000001,
    709.0,
    anchor="nw",
    text="ATUALIZAR",
    fill="#FFFFFF",
    font=("RobotoRoman Black", 37 * -1, 'bold')
)

atualizarHitbox = round_rectangle(92.80742645263683, 683.3333129882812, 514.1531295776368, 781.6666259765625, radius=35, fill="")
canvas.tag_bind(atualizarHitbox, '<ButtonPress-1>', click)
canvas.tag_bind(atualizarHitbox, "<Enter>", change_cursor)
canvas.tag_bind(atualizarHitbox, "<Leave>", restore_cursor)

textAtualizado = canvas.create_text(
    92,
    666,
    anchor="nw",
    text=lastRefreshed_Phrase(),
    fill="",
    font=("Roboto", 12 * -1, 'italic')
)


# ICON LINK
linkIcon = PhotoImage(file=os.path.join(atual_directory, "assets/resources/link.png"))
label_imagem = Label(window, image=linkIcon, bg="#17192D").place(x = 93, y = 545)
canvas.create_text(
    148,
    555,
    anchor="nw",
    text="github.com/dnowdd",
    fill="#6A2346",
    font=("RobotoRoman Bold", 24 * -1)
)
githubHitbox = canvas.create_rectangle(
    148,
    555,
    380,
    585,
    fill="",
    outline=""
)
canvas.tag_bind(githubHitbox, '<ButtonPress-1>', redirectGithub)
canvas.tag_bind(githubHitbox, "<Enter>", change_cursor)
canvas.tag_bind(githubHitbox, "<Leave>", restore_cursor)

canvas.create_text(
    92.80742645263683,
    260.0,
    anchor="nw",
    text="David Aquino.",
    fill="#903749",
    font=("Roboto", 28 * -1, 'bold')
)

one_phrase = canvas.create_text(
    92.80742645263683,
    230.0,
    anchor="nw",
    text="Esse projeto foi desenvolvido por",
    fill="#903749",
    font=("Roboto", 28 * -1)
)

canvas.create_text(
    92.80742645263683,
    380.0,
    anchor="nw",
    text="https://maisesports.com.br.",
    fill="#903749",
    font=("Roboto", 28 * -1, 'bold')
)
maisesportsHitbox = canvas.create_rectangle(
    92,
    380,
    500,
    410,
    fill="",
    outline=""
)
canvas.tag_bind(maisesportsHitbox, '<ButtonPress-1>', redirectMaisesports)
canvas.tag_bind(maisesportsHitbox, "<Enter>", change_cursor)
canvas.tag_bind(maisesportsHitbox, "<Leave>", restore_cursor)

five_phrase = canvas.create_text(
    92.80742645263683,
    350.0,
    anchor="nw",
    text="utilizando webscraping do site",
    fill="#903749",
    font=("Roboto", 28 * -1)
)

four_phrase = canvas.create_text(
    92.80742645263683,
    320.0,
    anchor="nw",
    text="captura informações de esports",
    fill="#903749",
    font=("Roboto", 28 * -1)
)

three_phrase = canvas.create_text(
    92.80742645263683,
    290.0,
    anchor="nw",
    text="Ele consiste em um sistema que",
    fill="#903749",
    font=("Roboto", 28 * -1)
)

ten_phrase = canvas.create_text(
    92.80742645263683,
    500.0,
    anchor="nw",
    text="outros.",
    fill="#903749",
    font=("Roboto", 28 * -1)
)

nine_phrase = canvas.create_text(
    92.80742645263683,
    470.0,
    anchor="nw",
    text="Valorant, CS 2, Free fire, entre",
    fill="#903749",
    font=("Roboto", 28 * -1)
)

eight_phrase = canvas.create_text(
    92.80742645263683,
    440.0,
    anchor="nw",
    text="informação estão: LoL, CS:GO,",
    fill="#903749",
    font=("Roboto", 28 * -1)
)

seven_phrase = canvas.create_text(
    92.80742645263683,
    410.0,
    anchor="nw",
    text="Dentre os jogos possíveis para",
    fill="#903749",
    font=("Roboto", 28 * -1)
)


# ICON LINK
brazilImage = PhotoImage(file=os.path.join(atual_directory, "assets/resources/brazil.png"))
brazilImage = brazilImage.subsample(10)
brazilItem = canvas.create_image(1528.8, 10, image=brazilImage, anchor="nw")
brazilHitbox = canvas.create_rectangle(
    1528.8,
    10,
    1580,
    61.2,
    fill="",
    outline=""
)

def changeLanguagePortuguese(event):
    changeLanguage('portuguese')
    
canvas.tag_bind(brazilHitbox, '<ButtonPress-1>', changeLanguagePortuguese)
canvas.tag_bind(brazilHitbox, "<Enter>", change_cursor)
canvas.tag_bind(brazilHitbox, "<Leave>", restore_cursor)

usaImage = PhotoImage(file=os.path.join(atual_directory, "assets/resources/usa.png"))
usaImage = usaImage.subsample(10)
usaItem = canvas.create_image(1457.6, 10, image=usaImage, anchor="nw")
usaHitbox = canvas.create_rectangle(
    1457.6,
    10,
    1508.2,
    61.2,
    fill="",
    outline=""
)

def changeLanguageEnglish(event):
    changeLanguage('english')
    
canvas.tag_bind(usaHitbox, '<ButtonPress-1>', changeLanguageEnglish)
canvas.tag_bind(usaHitbox, "<Enter>", change_cursor)
canvas.tag_bind(usaHitbox, "<Leave>", restore_cursor)

window.resizable(False, False)
window.mainloop()