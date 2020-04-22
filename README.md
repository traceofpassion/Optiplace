* Author: SHIRONMARO
* API_Used: Kakao Geocoding API based on keywords (Requires your own api_key)
* Description:
1. Subway_Station_Crawling.ipynb
- Crawled all the line and station names in Korea, and cleansed them into common expressions.

2. Optiplace.py
- centering(): a function which calculates a center coordinate of N-people
- distance(): a function which requests a set of latitude and longitude of N-people, and finds the nearest subway station to the center coordinate of N-people.
- optimize(): a function which returns and shows the optimal places, using `folium` module.

3. Optiplace.ipynb
- Inputs a list-format of N-people's location names as an object of Optiplace.optimize()
- Any Korean words would be possible, but official places like stations and landmarks will work the best.
- It the location name doesn't exist in KakaoMap System, the function would not work. Try other keywords.

4. Etc
- data: a folder where a station information table is located
- chromedriver.exe: selenium chrome driver

* On planning
- I'm planning to make a function to optimize the place based on the time interval from station A to station B.
- If someone has inquiries about the `optiplace' or have some good ideas to calculate time interval, please email to 'traceofpassion@gmail.com'.
