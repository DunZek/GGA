import json, datetime, holidays

# Meta data
with open('json/meta.json') as f:
    meta = json.load(f)
    # For on_message
    ID_PC = meta["GGA"]["ID_PC"]
    ID_MB = meta["GGA"]["ID_MB"]
    ID = str(meta["GGA"]["ID"])

# Messages
with open('json/messages.json') as f:
    messages = json.load(f)

# Class Schedule
with open("json/schedule.json") as f:
    schedule = json.load(f)

# List of holidays
with open("json/manual_holidays.json") as f:
    man_holidays = json.load(f)
    new_holidays = {}
    for key in man_holidays:
        year = man_holidays[key][0]
        month = man_holidays[key][1]
        day = man_holidays[key][2]
        new_holidays[datetime.date(year, month, day)] = key
    weekdays = dict.keys(schedule)
    holiday_dates = [holiday[0].strftime("%x") for holiday in holidays.Canada(years=2021).items()]
    holiday_dates += [holiday[0].strftime("%x") for holiday in new_holidays.items()]
    holiday_names = [holiday[1] for holiday in holidays.Canada(years=2021).items()]
    holiday_names += [holiday[1] for holiday in new_holidays.items()]

# Flags
with open("json/flags.json") as f:
    flags = json.load(f)

# Other
current_month = datetime.datetime.now().strftime("%B")  # Returns full month name -> "January"
