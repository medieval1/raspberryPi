#!/usr/bin/python

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from time import sleep
import twitter
from random import randint
import sys
import getopt
import signal

def sig_handler(signal, frame):
  lcd.clear()
  lcd.backlight(lcd.OFF)
  sys.exit()

def main (argv):

  twitUser = ''

  try:
    opts, args = getopt.getopt(argv, "hu:", ["user="])
  except getopt.GetoptError:
    print 'mytwit.py -u <twitterUser>'
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print 'mytwit.py -u <twitterUser>'
      sys.exit()
    elif opt in ("-u", "--user"):
      twitUser = arg
  
  if twitUser == '':
    print 'mytwit.py -u <twitterUser>'
    sys.exit(2)

  api = twitter.Api()

  lcd.clear()

  col = (lcd.RED , lcd.YELLOW, lcd.GREEN, lcd.TEAL, lcd.VIOLET, lcd.WHITE)

  status = api.GetUserTimeline(twitUser)

  twitUser = twitUser[:12] + ' '
  numTweets = len(status)

  for tweet in status:

    txt = tweet.text

    if txt != None and type(txt) == type(u"") and txt.find(u'\u2019') >= 0 : txt = txt.replace(u'\u2019', '\'')
    if txt != None and type(txt) == type(u"") and txt.find(u'\u201c') >= 0 : txt = txt.replace(u'\u201c', '\'')
    if txt != None and type(txt) == type(u"") and txt.find(u'\u201d') >= 0 : txt = txt.replace(u'\u201d', '\'')
    if txt != None and type(txt) == type(u"") and txt.find(u'\u2026') >= 0 : txt = txt.replace(u'\u2026', '\'')

    lcd.backlight(col[randint(0,5)])
    lcd.clear()

    lcd.message(twitUser + str(numTweets) + '\n' + txt[0:15])
    sleep(1)

    for x in range(0, len(txt)-15):
      if lcd.buttonPressed(lcd.SELECT):
        break
      lcd.clear()
      lcd.message(twitUser + str(numTweets) + '\n' + txt[x:x+15])
      sleep(.2)

    numTweets -= 1
    sleep(1)

  lcd.clear()
  lcd.backlight(lcd.OFF)

if __name__ == "__main__":

  lcd = Adafruit_CharLCDPlate()

  signal.signal(signal.SIGINT, sig_handler)
  main(sys.argv[1:])
