# -*- coding: utf-8 -*-
import legs
# (구버전 실험) DAY 2 마지막에 숙소 도착 추가 — 현재 일정은 legs.py 가 기준입니다
legs.DAYS['d2'] = [
  ('breakfast2',   '08:30', 30, 50,'차량'),
  ('ecoland',      '09:50',160,  5,'차량'),
  ('gyorae_lunch', '13:00', 70, 35,'차량'),
  ('manjanggul',   '15:00', 80, 25,'차량'),
  ('delmoondo',    '17:00', 25,  5,'도보'),
  ('hamdeok',      '17:30', 50, 40,'차량'),
  ('ssangdungi',   '19:00', 90, 60,'차량'),
  ('stay_night2',  '20:20',  0,  0, None),
]
legs.SHORT['stay_night2']='숙소'
