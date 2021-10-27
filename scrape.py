# Helper function to scrape HTML from my D2L calendar

# Iterate through each HTML of each month (html, month name. month length)
for item in [(html_oct, "October", 31), (html_nov, "November", 30), (html_dec, "December", 31)]:

    # Parse HTMLs
    month = BeautifulSoup(item[0], "html.parser")
    # Get the days of the specific month
    days = month.find_all('div', attrs={"class" : "d2l-le-calendar-month-day"})

    # Iterate through each day of the month
    resulting_month = {}
    index = 1  # to keep track if given day belongs to particular month

    for day in days:
        # Select only the days that pertain to that particular month
        date = re.search("\d+", day.contents[0]).group()
        if int(date) != index:
            continue
        else:
            # Select only the days that have assignments
            if len(day.contents) > 1:

                # Find the spans in the divs
                titles = day.find_all('span', attrs={"class" : "d2l-le-calendar-event-title"})
                times = day.find_all('span', attrs={"class" : "d2l-le-calendar-event-time"})

                # Extract assignment data out of the HTML
                school = {k: v for k, v in zip([title.contents[0] for title in titles], [time.contents[0] for time in times])}
                resulting_day = {}
                for key in school:
                    resulting_day[key] = school[key]

                # Assign the given date to these assignments
                resulting_month[date] = resulting_day

        # Increment index up to the length of the month
        if index <= item[2]:
            index += 1

    # Assign the given month to these days of assignments
    result[item[1]] = resulting_month

# Create json document
with open("json/due.json", "w") as f:
    json.dump({"October": result["October"], "November": result["November"], "December": result["December"]}, f, indent=4)
