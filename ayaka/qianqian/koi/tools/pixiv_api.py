import gppt
import pixivpy3 as pixiv
from nonebot_adapter_gocq import Bot
import koi.tools.init_data as data
from typing import Optional,Union
import random
'''
返回示例：（json_result.illusts[0]),原结果返回一个包含众多以下集合结构的集合
{'id': 92757347, 'title': 'ドット絵271「山田杏奈②」僕の心のヤバイやつ', 'type': 'illust', 'image_urls': {'square_medium': 'https://i.pximg.net/c/360x360_70/img-master/img/2021/09/15/04/58/49/92757347_p0_square1200.jpg', 'medium': 'https://i.pximg.net/c/540x540_70/img-master/img/2021/09/15/04/58/49/92757347_p0_master1200.jpg', 'large': 'https://i.pximg.net/c/600x1200_90/img-master/img/2021/09/15/04/58/49/92757347_p0_master1200.jpg'}, 'caption': '', 'restrict': 0, 'user': {'id': 5257800, 'name': 'フクD', 'account': 'fuku_84', 'profile_image_urls': {'medium': 'https://i.pximg.net/user-profile/img/2019/07/12/04/12/37/15995784_c6643779d0c8edbcba922c4bb2e0ef4f_170.png'}, 'is_followed': False}, 'tags': [{'name': 'ドット絵', 'translated_name': 'pixel art'}, {'name': '水着', 'translated_name': 'swimsuit'}, {'name': '山田杏奈', 'translated_name': 'Anna Yamada'}, {'name': '僕の心のヤバイやつ', 'translated_name': 'The Dangers in My Heart'}], 'tools': ['EDGE'], 'create_date': '2021-09-15T04:58:49+09:00', 'page_count': 1, 'width': 512, 'height': 576, 'sanity_level': 2, 'x_restrict': 0, 'series': None, 'meta_single_page': {'original_image_url': 'https://i.pximg.net/img-original/img/2021/09/15/04/58/49/92757347_p0.png'}, 'meta_pages': [], 'total_view': 12, 'total_bookmarks': 0, 'is_bookmarked': False, 'visible': True, 'is_muted': False}

'''
proxies={
    'http':'http://127.0.0.1:10080',
    'https':'http://127.0.0.1:10080'
}
#保存refresh_token至独立文件
def restore_pixtoken(token):
    d_path=data.get_init_path()
    with open(f'{d_path}pixtoken.txt','w') as store:
        store.write(token)
        store.close()
    return True

#从独立文件获取refresh_token
def get_pixtoken():
    d_path=data.get_init_path()
    with open(f'{d_path}pixtoken.txt','r') as store:
        token=store.read()
        store.close()
    return token


async def pix_get_refresh_token(bot :Bot):
    g=gppt.GetPixivToken()
    #注意修改selenium中request请求的proxies参数以设置代理
    res=g.login(user='2911544726@qq.com',pass_='wang20010325')
    bot.config.pix_token=res['refresh_token']
    restore_pixtoken(res['refresh_token'])
    #注意在nonebot config中增加一项 pix_token

async def get_apiobject(bot : Bot):
    api = pixiv.AppPixivAPI(proxies=proxies)
    try:
        api.auth(refresh_token=bot.config.pix_token)
    except:
        try:
            api.auth(refresh_token=get_pixtoken())
        except:
            await pix_get_refresh_token(bot)
            api.auth(refresh_token=bot.config.pix_token)
    return api

#返回一个路径，对应下载的符合要求的图片
async def pix_search_from_tag(bot :Bot,tag) -> (bool,str):
    api= await get_apiobject(bot)
    path = data.get_cache_path() + 'pixiv_cache'
    try:
        json_result = api.search_illust(tag, search_target='partial_match_for_tags',sort='popular_desc')
        illust = json_result.illusts[random.randint(0,len(json_result.illusts)-1)]
        file_path=api.download(illust.image_urls['large'],'',path)
        pid=illust.id
        #修改了原方法中的返回值为path
        #!!!注意，缓存文件夹中需有"pixiv_cache"
        return (True,file_path,pid)
    except:
        return (False,'没有在pixiv上找到有对应标签的图片')

async def get_ranking_illust(bot: Bot,mode : str,date : Optional[str] = None,number = 10)->(bool,Union[list,str]):
    # mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
    # date: '2016-08-01'
    # mode(r18榜单需登录): [day_r18, day_male_r18, day_female_r18, week_r18, week_r18g]
    api= await get_apiobject(bot)
    path = data.get_cache_path() + 'pixiv_cache'
    filepath=[]
    try:
        json_result=api.illust_ranking(mode=mode,date=date)
        for illusts in json_result.illusts:
            number-=1
            filepath.append(api.download(illusts.image_urls['large'],'',path))
            if number==0:
                break
        return (True,filepath)
    except:
        return (False,'没有在pixiv上找到排行榜内容')




'''
#获取图片pixiv_tag和原图url
def get_pixiv_tag_url(pixiv_id,page):
    try:
        if proxy_on:
            api = AppPixivAPI()
            api.set_accept_language('zh-cn')
            api.auth(refresh_token=refresh_token)
            json_result = api.illust_detail(pixiv_id)
            if not json_result.illust.title:
                return '','',0,''
            page_count = json_result.illust.page_count
            illust = json_result.illust.tags
            r18 = 0
            pixiv_tag = ''
            pixiv_tag_t = ''
            pixiv_img_url =''
            if illust[0]['name'] == 'R-18':
                r18 = 1
            for i in illust:
                pixiv_tag = pixiv_tag.strip()+ " "+ str(i['name']).strip('R-18')
                pixiv_tag_t = pixiv_tag_t.strip() + " "+ str(i['translated_name']).strip('None') #拼接字符串 处理带引号sql
            pixiv_tag = pixiv_tag.strip()
            pixiv_tag_t = pixiv_tag_t.strip()
            if page_count == 1:
                pixiv_img_url=json_result.illust.meta_single_page['original_image_url']
            else:
                pixiv_img_url=json_result.illust.meta_pages[int(page)]['image_urls']['original']
            return pixiv_tag,pixiv_tag_t,r18,pixiv_img_url
        else:
            return '','',0,''
    except Exception as e:
        return '','',0,''
'''