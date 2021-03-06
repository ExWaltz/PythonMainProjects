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
    return _main(url)

def livestream(search_val):
    search_val = _url_check(search_val)
    url = f"{search_val}/videos?view=2&live_view=501"
    return _main(url)

def upcoming(search_val):
    search_val = _url_check(search_val)
    url = f"{search_val}/videos?view=2&live_view=502"
    return _main(url)

def _get_views(jsn_data):
    # if watcher is in single to triple digits
    if len(jsn_data) == 1:
        channel_vid_views = str(jsn_data[0].get('text')).split()[0]
        channel_vid_length = str(jsn_data[0].get('text')).split()[1]
    elif len(jsn_data) == 2:
        channel_vid_views = jsn_data[0].get('text')
        channel_vid_length = jsn_data[1].get('text')
    else:
        channel_vid_views = '0'
        channel_vid_length = "watching"
    return channel_vid_views, channel_vid_length 

def _getVids(parent_jsn):
    # Get Videos
    channel_vid = parent_jsn.get('videoId')
    channel_vid = f"https://www.youtube.com/watch?v={channel_vid}"
    channel_vid_thumb = parent_jsn.get('thumbnail').get('thumbnails')[-1].get('url')
    channel_vid_thumb = str(channel_vid_thumb)
    channel_vid_title = parent_jsn.get('title').get('runs')[0].get('text')
    channel_vid_type = parent_jsn.get('thumbnailOverlays')[0].get('thumbnailOverlayTimeStatusRenderer').get('style')

    # Check if Live Stream
    if parent_jsn.get('publishedTimeText') is None:

        # Get Live Stream Info
        try:

            if parent_jsn.get('thumbnailOverlays')[0].get('thumbnailOverlayTimeStatusRenderer').get('style') == 'LIVE':
                channel_vid_date = parent_jsn.get('thumbnailOverlays')[0].get('thumbnailOverlayTimeStatusRenderer').get('style')
                channel_vid_views, channel_vid_length = _get_views(parent_jsn.get('viewCountText').get('runs')) 

            elif parent_jsn.get('upcomingEventData'):
                channel_vid_date = parent_jsn.get('upcomingEventData').get('startTime')
                channel_vid_date = datetime.fromtimestamp(int(channel_vid_date))
                jpn_time = pytz.timezone('Japan')
                channel_vid_date = str(channel_vid_date.astimezone(jpn_time))
                channel_vid_views, channel_vid_length = _get_views(parent_jsn.get('viewCountText').get('runs')) 

        except Exception:

            # Youtube upload music videos is confusing
            channel_vid_date = "Unspecified"
            channel_vid_views = parent_jsn.get('viewCountText').get('simpleText')
            channel_vid_length = parent_jsn.get('lengthText').get('simpleText')

    else:

        # Get Video Info
        channel_vid_date = parent_jsn.get('publishedTimeText').get('simpleText')
        channel_vid_views = parent_jsn.get('viewCountText').get('simpleText')
        channel_vid_length = parent_jsn.get('thumbnailOverlays')[0].get('thumbnailOverlayTimeStatusRenderer').get('text').get('simpleText')
    return {channel_vid: [channel_vid_title, channel_vid_date, channel_vid_views, channel_vid_length, channel_vid_thumb, channel_vid_type]}


def _main(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    script_list = soup.find_all('script')

    # !Debuging
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

    # !Debuging
    # Save the json ready string to a file named
    # 'searchRaw.log'. You can use an online tool to
    # check if the string is ready to be parsed to json format
    #
    # open_file = open('searchRaw.log', 'w', encoding='utf-8')
    # open_file.write(str(real_script))
    # open_file.close()

    jsn = json.loads(real_script)

    # :The pain of nested json
    # :I suggest to use a tool to check the
    # :validity of the json key names in the 'searchRaw.log' file
    # We use get method, because it returns None type instead of an error
    #
    jsn_list = jsn['contents'].get('twoColumnBrowseResultsRenderer').get('tabs')[1].get('tabRenderer').get('content').get('sectionListRenderer').get('contents')[0].get('itemSectionRenderer').get('contents')[0].get("gridRenderer").get("items")

    results = {}

    for search_result in jsn_list:
        if search_result.get("gridVideoRenderer"):
            chnl_vid = _getVids(search_result.get("gridVideoRenderer"))
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
    print(upcom)
