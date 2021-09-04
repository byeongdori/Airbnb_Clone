from django.utils import timezone
import calendar

class Day():
    def __init__(self, number, past):
        self.number = number
        self.past = past
    
    def __str__(self):
        return self.number

class Calendar(calendar.Calendar):

    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wen", "Thu", "Fri", "Sat")
        self.month_names = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_days(self):
        # 그 해, 그 달의 날짜와 요일을 튜플로 리턴
        # ex) (1, 4) -> 1일이 금요일
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []
        for week in weeks:
            for day, _ in week:
                # week tuple을 Unpacking 하는 과정, 첫번째 원소인 day만 뽑아냄
                now = timezone.now()
                today = now.day
                month = now.month
                past = False
                if month == self.month:
                    if day <= today:
                        past = True
                new_day = Day(day, past)
                days.append(new_day)
        return days 

    def get_month(self):
        return self.month_names[self.month - 1]
