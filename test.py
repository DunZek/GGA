schedule = {
    "Wednesday": [
        {
            "Class": "Introduction to Networking",
            "Start": "9:00 AM",
            "Where": "Microsoft Teams",
            "End": "10:50 AM"
        },
        {
            "Class": "Professional Communication and Presentation Skills",
            "Start": "12:00 PM",
            "Where": "Zoom",
            "End": "1:50 PM"
        },
        {
            "Class": "Computer Programming Essentials",
            "Start": "2:30 PM",
            "Where": "Microsoft Teams",
            "End": "4:20 PM"
        }
    ],
}

for Class in schedule["Wednesday"]:
    # print(Class)
    for info in Class:
        print(info)
        print()
