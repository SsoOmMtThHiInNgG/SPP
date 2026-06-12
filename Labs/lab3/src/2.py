class AnalogClock:
    def __init__(self, hour_angle, minute_angle):
        self.hour_angle = hour_angle
        self.minute_angle = minute_angle

    def get_hour_angle(self):
        return self.hour_angle
    
    def get_minute_angle(self):
        return self.minute_angle


class ClockAdapter:
    def __init__(self, analog_clock):
        self.analog_clock = analog_clock

    def get_time(self):
        days = 0
        hour_angle = self.analog_clock.get_hour_angle()
        minute_angle = self.analog_clock.get_minute_angle()
        
        if hour_angle >= 360:
            days += hour_angle // 360
            hour_angle = hour_angle % 360
        elif hour_angle < 0:
            days -= (abs(hour_angle) // 360) + 1
            hour_angle = 360 - (abs(hour_angle) % 360)
            if hour_angle == 360:
                hour_angle = 0
        
        if minute_angle >= 360:
            minute_angle = minute_angle % 360
        elif minute_angle < 0:
            minute_angle = 360 - (abs(minute_angle) % 360)
            if minute_angle == 360:
                minute_angle = 0
        
        hours = int(hour_angle / 15)
        
        minutes = int(minute_angle / 6)
        if minutes == 60:
            minutes = 0
        
        if days > 0:
            return f"{days}д {hours:02d}:{minutes:02d}"
        elif days < 0:
            return f"{days}д {hours:02d}:{minutes:02d}"
        else:
            return f"{hours:02d}:{minutes:02d}"


hour_angle = int(input("Введите угол часовой стрелки: "))
minute_angle = int(input("Введите угол минутной стрелки: "))

clock = AnalogClock(hour_angle, minute_angle)
adapter = ClockAdapter(clock)

print("Время:", adapter.get_time())