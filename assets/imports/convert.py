import datetime

class Converter():
    def __init__(self):
        pass

    async def secondsToTimeText(self, secs):
        """``Returns a time with their text values between``
        
        ``Input``: int
        ``Output example``: 23 hours 54 minutes 23 seconds
        ``Usage example``: secs = await convert.secondsToTimeText(50)
        """
        seconds = secs % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        
        return f'{hour} hours, {minutes} minutes and {seconds} seconds'

    async def secondsToTimeDate(self, secs):
        """``Returns a time with semi colons between``

        ``Input``: int
        ``Output example``: 23:54:23
        ``Usage example``: secs = await convert.secondsToTimeText(50)
        """
        seconds = secs % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        
        return "%d:%02d:%02d" % (hour, minutes, seconds)