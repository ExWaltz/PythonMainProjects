import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import pytz


def _url_check(url):
    if url.find('youtube.com/channel/') == -1 and url.find('youtube.com/c/') == -1:
        raise Exception('URL is not a channel')
    if url.endswith('/'):
        url = url[:-1]
    if not url.startswith('https://'):
        url = f"https://{url}"
    return url

def videos(search_val):
    search_val = _url_check(search_val)
    url = f"{search_val}/videos"
    return _main(url, "DEFAULT")

def livestream(search_val):
    search_val = _url_check(search_val)
    url = f"{search_val}/videos?view=2&live_view=501"
    return _main(url, "LIVE")

def upcoming(search_val):
    search_val = _url_check(search_val)
    url = f"{search_val}/videos?view=2&live_view=502"
    return _main(url, "UPCOMING")

def _get_views(vid_link):
    response = requests.get(vid_link).text
    soup = BeautifulSoup(response, 'lxml')
    script_list = soup.find_all('script')

    if str(vid_link).endswith('/'): vid_link = vid_link[:-1]
    vid_id = str(vid_link).split('/')[-1]

    for sc in script_list:
        if str(sc).find("responseContext") != -1:
            real_script = str(sc)   # Find the correct script that contains video informations
            break

    real_script = real_script[69:-10]   # Remove uncessary text and convert to json ready text
    with open("test.log", "w", encoding="utf-8") as debug_sc:
        debug_sc.write(str(real_script))
    jsn = json.loads(real_script)

    vid_title = jsn.get('videoDetails').get('title')
    vid_date = jsn.get('microformat').get('playerMicroformatRenderer').get('publishDate')
    vid_views = jsn.get('videoDetails').get('viewCount')
    vid_length = jsn.get('videoDetails').get('lengthSeconds')
    vid_thumb = jsn.get('videoDetails').get('thumbnail').get('thumbnails')[-1].get('url')
    vid_type = "DEFAULT"
    vid_owner = jsn.get('videoDetails').get('author')

    if jsn.get('videoDetails').get('isLive'):
        vid_type = "LIVE"
    elif jsn.get('videoDetails').get('isUpcoming'):
        vid_type = "UPCOMING"

    return {vid_link: [vid_title, vid_date, vid_views, vid_length, vid_thumb, vid_type, vid_owner]}


def _main(url, method="DEFAULT"):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    script_list = soup.find_all('script')

    # Debuging
    # The code below will help you 
    # check if the code block below is working. 
    #
    # debug_raw = open('html_raw.log', 'w', encoding='utf-8')
    # for sc in script_list:
    #     debug_raw.write(str(sc))
    #     debug_raw.write("\n\n\n")
    # debug_raw.close()

    for sc in script_list:
        if str(sc).find("responseContext") != -1:
            real_script = str(sc)   # Find the correct script that contains video informations
            break

    real_script = real_script[59:-10]   # Remove uncessary text and convert to json ready text

    # Debuging
    # Save the json ready string to a file named
    # 'searchRaw.log'. You can use an online tool to
    # check if the string is ready to be parsed to json format
    #
    # open_file = open('searchRaw.log', 'w', encoding='utf-8')
    # open_file.write(str(real_script))
    # open_file.close()

    jsn = json.loads(real_script)

    # The pain of nested json
    # I suggest to use a tool to check the
    # validity of the json key names in the 'searchRaw.log' file
    # We use get() method, because it returns None type instead of an error
    #
    jsn_list = jsn.get('contents').get('twoColumnBrowseResultsRenderer').get('tabs')[1].get('tabRenderer').get('content').get('sectionListRenderer').get('contents')[0].get('itemSectionRenderer').get('contents')[0].get("gridRenderer").get("items")
    chnl_avatar = jsn.get('header').get('c4TabbedHeaderRenderer').get('avatar').get('thumbnails')[-1].get('url')

    results = {}

    for search_result in jsn_list:
        if search_result.get("gridVideoRenderer"):
            vid_link = search_result.get("gridVideoRenderer").get('videoId')
            vid_link = f"https://www.youtube.com/watch?v={vid_link}"
            chnl_vid = _get_views(vid_link)
            chnl_val = next(iter(chnl_vid.values()))
            chnl_key = next(iter(chnl_vid.keys()))
            chnl_val.append(chnl_avatar)
            chnl_vid[chnl_key] = chnl_val
            if chnl_val[5] == method:
                results.update(chnl_vid)

    return results


if __name__ == '__main__':
    query = input("Search:\t") 
    upcom = upcoming(str(query))
    live = livestream(str(query))
    vid = videos(str(query))
    comp = {}
    if upcom:
        comp.update(upcom)
    if live:
        comp.update(live)
    if vid:
        comp.update(vid)
    print(comp)
