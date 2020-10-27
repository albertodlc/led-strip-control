import ledStrip
import sys

dc = ledStrip.DeviceControl("52:14:00:00:C6:A9")
dc.notifications()
dc.close_connection()
