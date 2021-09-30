import json
import holidays
import datetime
with open('./manual_holidays.json') as f:
    man_holidays = json.load(f)

holiday_dates = [holiday[0].strftime("%x") for holiday in holidays.Canada(years=2021).items()]
holiday_names = [holiday[1] for holiday in holidays.Canada(years=2021).items()]

print(man_holidays)

holidays = {}
for key in man_holidays:
    year = man_holidays[key][0]
    month = man_holidays[key][1]
    day = man_holidays[key][2]
    holidays[dt.date(year, month, day)] = key
print(holidays)

for item in holidays:
    print(item)

holiday_dates += [holiday[0].strftime("%x") for holiday in holidays.items()]

print(holiday_dates)