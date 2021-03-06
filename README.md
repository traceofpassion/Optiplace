
# Documentation

## Directory

``` 
  Optiplace   
  ├── data
  │   ├── subway_location_info.csv
  │   └── crawling
  │       ├── chromedriver.exe (ignored)
  │       └── Subway_Station_Crawling.py
  │
  ├── Optiplace.py
  │
  ├── Optiplace.ipynb
  │
  └── kakao_api.csv (ignored)
```

## Requirement

### Packages Required

  - selenium
  - beautifulsoup
  - requests
  - pandas
  - folium

## Description

### 1\. Subway\_Station\_Crawling.py

  - Crawl all the line and station names in S.Korea, and cleanse them
    into common expressions.

### 2\. Optiplace.py

  - centering(): a function which calculates a center coordinate of
    N-people
  - distance(): a function which requests a set of latitude and
    longitude of N-people, and finds the nearest subway station to the
    center coordinate of N-people.
  - optimize(): a function which returns and shows the optimal places,
    using *folium* module.

### 3\. Optiplace.ipynb

  - Input a list-format of N-people’s location names as an object of
    Optiplace.optimize()
  - Any Korean words would be possible, but official places such as
    stations and landmarks will work the best.
  - If the location’s name doesn’t exist in KakaoMap, it would not work.
    Try other keywords.

## Forward

  - On the plan to make an optimization based on the time interval from
    station to station.
  - Should you have inquiries, please email to
    <traceofpassion@gmail.com>
