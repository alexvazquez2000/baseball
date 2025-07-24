from datetime import date
from datetime import datetime
import calendar

class BaseCalendar:

    def __init__(self, instance_attribute):
        self.instance_attribute = instance_attribute

    @classmethod
    def calculate_age(cls, birth_date, target_date):
      years = target_date.year - birth_date.year
      months = target_date.month - birth_date.month
      days = target_date.day - birth_date.day

      # Adjust days
      if days < 0:
        # Get days in the previous month
        prev_month = target_date.month - 1 if target_date.month > 1 else 12
        prev_year = target_date.year if target_date.month > 1 else target_date.year - 1
        days_in_prev_month = calendar.monthrange(prev_year, prev_month)[1]
        days += days_in_prev_month
        months -= 1

      # Adjust months
      if months < 0:
        months += 12
        years -= 1

      return years, months, days

    @classmethod
    def baseball_age(cls, dob_date, season_date):
      #dob_date, season_date are strings with format yyyy-mm-dd.  ie "2025-05-01"
      # Parse the string
      dob_obj = datetime.strptime(dob_date, "%Y-%m-%d").date()
      season_obj = datetime.strptime(season_date, "%Y-%m-%d").date()
      ## Now it's a date object
      #print(season_obj)           # Output: 2025-05-01
      #print(type(season_obj))     # Output: <class 'datetime.date'>
      age_years, age_months, age_days = BaseCalendar.calculate_age(dob_obj, season_obj)
      return f"{age_years} years, {age_months} months, {age_days} days."

## Usage example
#birth = date(2000, 12, 31)
#target = date(2025, 5, 1)
#age_years, age_months, age_days = BCalendar.calculate_age(birth, target)
#print(f"Age: {age_years} years, {age_months} months, {age_days} days.")
## would print:
##     Age: 24 years, 4 months, 1 days.

#print(BaseCalendar.baseball_age("2000-05-01", "2025-05-01"))
