from bs4 import BeautifulSoup

with open('html/october.html') as oct, open('html/november.html') as nov, open('html/december.html') as dec:
    html = oct.read()

soup = BeautifulSoup(html, "html.parser")

titles = soup.find_all('span', attrs={"class" : "d2l-le-calendar-event-title"})
times = soup.find_all('span', attrs={"class" : "d2l-le-calendar-event-time"})

print(titles[0].contents[0])
print(times[0].contents[0])
# print(times)

school = zip([title.contents[0] for title in titles], [time.contents[0] for time in times])

for item in school: print(item)
