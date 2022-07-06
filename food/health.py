"""Helper functions to calculate diff MCI ."""

from datetime import date


class Health:
    """Heath helper Class."""

    # calc_age(date(year, month, day))
    @classmethod
    def calc_age(cls, born):
        """Calculate age."""
        today = date.today()
        try:
            birthday = born.replace(year=today.year)

            # raised when birthday date is Feb 29
            # and the current year is not a leap year
        except ValueError:
            birthday = born.replace(year=today.year,
                                    month=born.month + 1,
                                    day=1)

        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    @classmethod
    def imc(cls, weight, height):
        if weight > 0 and height > 0:
            print("Well you did not fail us")
            return round((weight / pow(height, 2)), 2)
        else:
            print("You did fail us.")
            return 0

    @classmethod
    def img(cls, gender, age, imc):
        if imc == 0 or age == 0:
            return 0
        else:
            if gender == 0:  # woman
                return round((1.2 * imc) + (0.23 * age) - (10.8 * 1) - (5.4), 2)
            elif gender == 1:  # man
                return round((1.2 * imc) + (0.23 * age) - (10.8 * 0) - (5.4), 2)

    @classmethod
    def mb_woman(cls, weight, height, age):
        """Calculate woman MB."""
        if weight > 0.0 and height > 0.0 and age > 0:
            print(" Not failed woman")
            return round(abs((10 * weight) + (6.25 * height) - (5 * age) - 161), 2)
        else:
            return 0

    @classmethod
    def mb_man(cls, weight, height, age):
        """Calculate man MB."""
        if weight > 0 and height > 0 and age > 0:
            print("Not failed men")
            return round(abs((10 * weight) + (6.25 * height) - (5 * age) + 5), 2)
        else:
            return 0

    @classmethod
    def ideal_weight_man(cls, height):
        """Calculate man ideal weight."""
        if height == 0:
            return 0
        return round(abs((height - 100) - ((height - 150) / 4)), 2)

    @classmethod
    def ideal_weight_woman(cls, height):
        """Calculate woman ideal weight."""
        if height == 0:
            return 0
        return round(abs((height - 100) - ((height - 150) / 2)), 2)

    @classmethod
    def tef_man(cls, mb_man):
        """
        Man TEA
        """
        return round(abs(mb_man * 0.1), 2)
   
    @classmethod
    def tef_woman(cls, mb_woman):
        """
        Woman TEA
        """
        return round(abs(mb_woman * 0.1), 2)

    @classmethod
    def activity_level(cls, activity, user_gender):
        if user_gender == "male":
            if activity == "sedentary":
                return 0
            elif activity == "light activity":
                return 0.14

            elif activity == "moderate activity":
                return 0.27
            else:
                return 0.54

        elif user_gender == "female":
            if activity == "sedentary":
                return 0
            elif activity == "light activity":
                return 0.12

            elif activity == "moderate activity":
                return 0.27
            else:
                return 0.45