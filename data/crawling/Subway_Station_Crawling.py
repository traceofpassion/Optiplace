print('--------Crawling Started--------')

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

def SubwayInfoCrawling():

    # crawling option = headless
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    # Use chromedriver from selenium <https://www.selenium.dev/>
    # You can choose other driver if you wish.
    driver = webdriver.Chrome("./chromedriver.exe", options=options)
    driver.get('http://www.seoulmetro.co.kr/kr/cyberStation.do')

    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    mapinfo = soup.find('div', 'mapInfo')
    lines = mapinfo.find_all('li')

    output = pd.DataFrame()
    for i in range(len(lines)):
        st_line = lines[i].span.text
        st_list = lines[i].div.text.split(',')
        for j in range(len(st_list)):
            st_name = st_list[j].strip()
            unit = pd.DataFrame({'st_name':[st_name],
                                 'st_line':[st_line]})
            output = pd.concat([output,unit], axis=0)

    output = output.reset_index(drop=True)
    driver.close()
    return output


# Save crawled data as a dataframe object
st_info = SubwayInfoCrawling()
print(st_info['st_line'].unique())


# Substitute line name with formal expression
line_dict = {
    '분당':'분당선',
    '신분당':'신분당선',
    '경의중앙':'경의중앙선',
    '용인경전철':'에버라인',
    '우이신설경전철':'우이신설선',
    '김포':'김포골드라인'    
}
st_info['st_line'] = st_info['st_line'].replace(line_dict)


# Substitute station name with formal expression
st_info.loc[st_info['st_name']=='4·19민주묘지','st_name'] = '4.19민주묘지'
st_info.loc[st_info['st_name']=='사우(김포시청)','st_name'] = '사우'
st_info['st_name'] = st_info['st_name'].apply(lambda x: x if x[-1]=='역' else x + '역')


# My own Kakao Developer API Key. Use for Geocoding.
kakao_api_key = pd.read_csv('../../kakao_api.csv')


# Geocode
headers = {'Authorization':f"{kakao_api_key['rest_api'][0]}"}
def Geocoding(st_name, st_line):
    url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={st_name} {st_line}'
    response = requests.get(url, headers=headers)
    lat = response.json()['documents'][0]['y']
    lng = response.json()['documents'][0]['x']
    return [lat,lng]

st_info['coordinates'] = st_info.apply(lambda x: Geocoding(x['st_name'], x['st_line']), axis=1)
st_info['lat'] = st_info['coordinates'].apply(lambda x: x[0])
st_info['lng'] = st_info['coordinates'].apply(lambda x: x[1])
st_info = st_info.drop(columns='coordinates')


# Save as a csv file
st_info.to_csv('../subway_location_info.csv', index=False)
print('--------Crawling Finished--------')