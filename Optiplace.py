import pandas as pd
import numpy as np
import math
import folium
import requests
from IPython.display import display
import getpass

df = pd.read_csv("./data/subway_location_info.csv")

# ## centering
# - N명의 좌표가 주어졌을 때, 중점 그룹을 찾아주는 함수입니다.
def centering(geocodes):
    
    points = []
    
    # 세 명 이상일때
    if len(geocodes) > 2:
        for i in range(len(geocodes)):
            for j in range(len(geocodes)):
                if i != j:
                    point = {'lat':(geocodes[i]['lat'] + geocodes[j]['lat'])/2,
                             'lng':(geocodes[i]['lng'] + geocodes[j]['lng'])/2}
                    points.append(point)                        
    
    # 두 명일 때
    elif len(geocodes) == 2:
        point = {'lat':(geocodes[0]['lat'] + geocodes[1]['lat'])/2,
                 'lng':(geocodes[0]['lng'] + geocodes[1]['lng'])/2}
        points.append(point)
    
    else:
        point = {'lat':geocodes[0]['lat'],
                 'lng':geocodes[0]['lng']}
        points.append(point)
    
    # 중복된 데이터 제거
    compare = set()
    output = []
    for point in points:
        unit = tuple(point.items())
        if unit not in compare:
            compare.add(unit)
            output.append(point)
            
    return output

# ## distance()
# - 중점 그룹과 서울에 있는 모든 역의 좌표와의 거리 평균을 계산해주는 함수입니다.

def distance(centers,lat,lng):
    distances = []
    for i in range(len(centers)):
        hor = (centers[i]['lat'] - lat)**2
        ver = (centers[i]['lng'] - lng)**2
        distances.append(math.sqrt(hor + ver))
    return np.mean(distances)


# ## optimize()
# - KakaoMaps를 통해 N명의 좌표를 불러오고, 중점 그룹에서 가까운 역을 거리 순으로 정렬하여 출력하는 함수입니다.

user_name = getpass.getuser()
kakao_api_key = pd.read_csv(f'C:/Users/{user_name}/Google Drive/Secret/kakao.csv')
headers = {'Authorization':f"{kakao_api_key['rest_api'][0]}"}

def Geocoding(keyword):
    url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={keyword}'
    response = requests.get(url, headers=headers)
    lat = response.json()['documents'][0]['y']
    lng = response.json()['documents'][0]['x']
    return [lat,lng]

def optimize(location):
    geocodes = []
    for k in range(len(location)):
        result_01 = Geocoding(location[k])
        result_02 = {'lat':float(result_01[0]),
                     'lng':float(result_01[1])}
        geocodes.append(result_02)  
        
    centers = centering(geocodes)
    df['distance'] = df.apply(lambda x: distance(centers=centers,
                                                 lat=x['lat'],
                                                 lng=x['lng']), axis=1)
    place = df.sort_values('distance', ascending=True).head(5).reset_index(drop=True)
    
    hotspot = [place['lat'].mean(),place['lng'].mean()]
    m = folium.Map(hotspot, zoom_start = 11)
    
    for i in range(len(geocodes)):
        candidate = [geocodes[i]['lat'],geocodes[i]['lng']]
        folium.Marker(
            location = candidate,
            icon = folium.Icon(color='blue')).add_to(m)        
    
    for i in range(len(place)):
        candidate = [place['lat'][i],place['lng'][i]]
        folium.Marker(
            location = candidate,
            popup = place['st_name'][i],
            icon = folium.Icon(color='red')).add_to(m)
    display(m)
    return(place)