# HLTV Crawler

This project is a crawler to `hltv.org` using Scrapy to gather CS:GO matches data.

## Guide

To start crawling HLTV, just execute the following command:

```
$ scrapy crawl hltv
```

It will create an `items.json` file, with the following format:

```
[{
    "player_nick": "huNter-",
    "kills": "24",
    "assists": "4 ",
    "deaths": "17",
    "kast": "75.9%",
    "adr": "89.7",
    "rating": "1.29",
    "team_item": {
        "team_name": "G2",
        "score": "13",
        "match_item": {
            "map_name": "Dust2",
            "event": "IEM Katowice 2020",
            "date": "2020-03-01 16:00",
            "match_id" : 99483
        }
    }
}...]
```
