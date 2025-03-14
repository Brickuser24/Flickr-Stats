import requests
import asyncio
import aiohttp

#Flickr ID
#Use https://www.webfx.com/tools/idgettr/ if their flickr page has their name in the link instead of the id.
user_id = ""

#Flickr API Key
api_key = ""

url = f"https://www.flickr.com/photos/{user_id}/"
response = requests.get(url).text
f = response.find('followerCount')
followers = ""
for i in response[f + 15:f + 20]:
  if i.isdigit():
    followers += i
print(f"Followers: " + followers)

async def fetch_photos(user_id, current_page):
    url = "https://api.flickr.com/services/rest"
    querystring = {
        "per_page": "500",
        "page": f"{current_page}",
        "extras": "can_addmeta,can_comment,can_download,can_print,can_share,contact,content_type,count_comments,count_faves,count_views,date_taken,date_upload,description,icon_urls_deep,isfavorite,ispro,license,media,needs_interstitial,owner_name,owner_datecreate,path_alias,perm_print,realname,rotation,safety_level,secret_k,secret_h,url_sq,url_q,url_t,url_s,url_n,url_w,url_m,url_z,url_c,url_l,url_h,url_k,url_3k,url_4k,url_f,url_5k,url_6k,url_o,visibility,visibility_source,o_dims,publiceditability,system_moderation",
        "user_id": user_id,
        "method": "flickr.people.getPhotos",
        "api_key": api_key,
        "format": "json",
        "nojsoncallback": "1"
    }

    async with aiohttp.ClientSession() as session:
      async with session.get(url, params=querystring) as response:
          return await response.json()

async def main(user_id):
    current_page = 1
    faves = 0
    views = 0
    comments = 0
    while True:
        response = await fetch_photos(user_id, current_page)
        for photo in response['photos']['photo']:
            faves += int(photo["count_faves"])
            views += int(photo["count_views"])
            comments += int(photo["count_comments"])
        if response['photos']['pages'] == current_page:
            break
        current_page += 1
    print(f"Total Faves: {faves}")
    print(f"Total Views: {views}")
    print(f"Total Comments: {comments}")

asyncio.run(main(user_id))
