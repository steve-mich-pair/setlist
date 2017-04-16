#!/usr/bin/env python

import datetime
import random

def read_songs_from_file(file_name):
  with open(file_name, 'r') as f:
    return [song_name.strip() for song_name in f.read().split('\n') if song_name]

def write_songs_to_file(songs, file_name):
  with open(file_name, 'w') as f:
    f.write('\n'.join(songs))

def all_songs():
  return set(read_songs_from_file('songs.csv'))

seven_days = datetime.timedelta(days=7)

def short_date(date):
  return date.strftime("%m-%d-%y")

def setlist_from(date):
  try:
    return set(read_songs_from_file(short_date(date) + '.csv'))
  except:
    return set([])

def generate_songlist():
  today = datetime.datetime.today()
  next_sunday = datetime.timedelta(days=6 - today.weekday()) + today
  last_sunday = next_sunday - seven_days
  two_sundays_away = next_sunday + seven_days
  two_sundays_ago = last_sunday - seven_days

  print "Which sunday is this setlist for?"
  print "(1)", short_date(next_sunday)
  print "(2)", short_date(two_sundays_away)
  which_sunday = input()

  last_sunday_setlist = setlist_from(last_sunday)
  two_sundays_ago_setlist = setlist_from(two_sundays_ago)
  next_sunday_setlist = setlist_from(next_sunday)

  recently_played_songs = [
    last_sunday_setlist | two_sundays_ago_setlist,
    next_sunday_setlist | last_sunday_setlist
  ][which_sunday-1]

  setlist_date = [next_sunday, two_sundays_away][which_sunday-1]

  not_recently_played_songs = all_songs() - recently_played_songs

  print "How many songs in this setlist?"
  song_count = input()

  setlist = set(random.sample(not_recently_played_songs, min(song_count, len(not_recently_played_songs))))
  setlist = setlist | set(random.sample(recently_played_songs, min(song_count - len(setlist), len(recently_played_songs))))

  write_songs_to_file(setlist, short_date(setlist_date) + '.csv')
  print '\n'.join(setlist)

print len(all_songs()), "songs found in songs.csv"

print ""
print "What would you like to do?"
print "(1) Generate a songlist"
print "(2) Quit"

answer = input()

if answer == 1:
  generate_songlist()
elif answer == 2:
  exit()
