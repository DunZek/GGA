# Scrapes HTML from my D2L calendar
# Should be regularly updated. Automated? No. Manually because I don't think I can do it automatically
from bs4 import BeautifulSoup
import re

with open('html/october.html') as oct, open('html/november.html') as nov, open('html/december.html') as dec:
    html_oct = oct.read()
    html_nov = nov.read()
    html_dec = dec.read()

# Iterate through each HTML of each month
for html in [html_oct]:
    # Parse HTMLs
    soup = BeautifulSoup(html, "html.parser")
    # Get the days of the specific month
    days = soup.find_all('div', attrs={"class" : "d2l-le-calendar-month-day"})
    # print(days[0])
    # Iterate through each day of the month
    for day in days:
        # Select only the days that have assignments
        if type(day.contents) == list and len(day.contents) > 1:
            print('CONTENT --- ', re.search("\d", day.contents[0]))
            # # Parse div element
            # soup = BeautifulSoup(day)
            #
            # titles = soup.find_all('span', attrs={"class" : "d2l-le-calendar-event-title"})
            # times = soup.find_all('span', attrs={"class" : "d2l-le-calendar-event-time"})
            #
            # print(titles[0])
            # print(times[0])
            # # print(times)
            #
            # school = zip([title.contents[0] for title in titles], [time.contents[0] for time in times])

            # for item in school: print(item)

    # # Create json document
    # with open("json/due.json") as f:
    #     f.dump({"October": object, "November": object, "December": })
