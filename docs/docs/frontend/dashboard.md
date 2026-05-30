---
sidebar_position: 1
---
# Structure of frontend

Whole frontend is designed as this. navbar on the left with these options:

## Teams
This is disinged to be a list of teams as react element. 
Should contain:
1) Img located in /engine/img in center
2) Name of team
3) Points of teams
4) Drivers
5) Points
### Race mode
Designed table of teams if the race will end as it is rn

## Drivers
This is disinged to be a list of drivers as react element. 
Should contain:
1) Name
2) Position
3) Team
4) History of driver
5) Points
### Race mode
1) Pit stops
2) pneu
3) wear
4) avg position

## Track details

Should contain:
1) Conutry flag
2) Name of track
3) Pneu && Speed of track
4) Laps
5) DNF probalitiy during race count as this 100* count_cars* laps/dnf_probability

## POST forms
For this need to know <a href="http://localhost:3001/docs/api%20endpoints/post" target="_blank">Api endpoints</a>
Post forms should have structure like a form, but shouldn't look like 'em. 
### Sim lap
Need to handle init_race failure overflow of laps, automaticly do after race api and form should have multiple laps sim with option sim until ...
1) Lap number
2) DNF of sb
3) Start of rain
etc.

## Training
Used in init race, now is actully true for debug. SHould have big form, its own json that will be used in graphs
## Graphs
### Time laps
History of laps during race
### Sectors
Graph of avg time per sector
### Training
Graph of sector. Understeer and oversteer
### Standings during the time
During the race
### History of 
History of the circuit etc.