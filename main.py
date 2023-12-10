from pyncm.apis.login import LoginViaAnonymousAccount
from colorama import init, Fore
from utils import randstr
import random
import pyncm.apis
import platform
import requests
import time
import os
import sys
import json
import easygui
import win32api
import processlib
import traceback
import bar

version = "1.3"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0 PLiveMSC/' + version,
}

os.makedirs("PLiveMSCdl", exist_ok=True)

if platform.system() == "Windows":
    win32api.SetConsoleTitle(f"PLiveMSC {version} by @Stevesuk0")

# This version of LiveMSC was written by SteveUbuntu using python3 and is 100% compatible with Windows 7 and newer./
# The original version of LiveMSC is written in Java, by [Kkforkd], under the GNU v3 open source license.

# All source code and binary executables of this program will be uploaded to github.com and Kkforkd's QQ group[781112998].
# 沟石代码勿喷。 

# -==============================-
# pyncm ----- Play, Download and Search music (Netease Music[music.163.com]).
# platform -- Get system info.
# requests -- Send http request.
# time ------ WAITWAITWAITWAITWAIT
# os -------- Basic System api.
# json ------ Encode, Decode the json file to save program configs.
# easygui --- pop-up window
# -==============================- 


def line():
    print("================================")

def exit():
    input(f"按 Enter 结束 {Fore.MAGENTA}LiveMSC{Fore.RESET}。")
    if launch_mode == 0:
        os.remove("temp.mp3")
    sys.exit()

init(autoreset=True) # Fix Windows conhost not displaying colored text correctly.


print(f"{Fore.MAGENTA}LiveMSC {Fore.RESET}(LiveSongs) {version} @Stevesuk0")
print(f"Running on {Fore.BLUE}{platform.system()}{Fore.YELLOW} {platform.version()} {Fore.RESET}\n")
print(f"基于 Python {platform.python_version()} 与 PyNCM SDK 构建。")

response = requests.get("https://git.stevesuk.eu.org/https://raw.githubusercontent.com/Stevesuk0/PLiveMSC/master/version")
if response.text == version:
    print(f"您当前的 {Fore.MAGENTA}LiveMSC{Fore.RESET} 是最新版本。")
    print(f"最新版本：{Fore.GREEN}{response.text}{Fore.RESET}")
    print(f"当前版本：{Fore.GREEN}{version}{Fore.RESET}")
else:
    print(f"您当前的 {Fore.MAGENTA}LiveMSC{Fore.RESET} 不是最新版本。")
    print(f"最新版本：{Fore.GREEN}{response.text}{Fore.RESET}")
    print(f"当前版本：{Fore.YELLOW}{version}{Fore.RESET}")

shinput = easygui.choicebox(title="PLiveMSC Launch Menu", msg="选择一项进行启动", choices=["正常启动", "以 歌曲下载 模式启动", "以 配置修改 模式启动", "打开歌曲文件夹"], preselect=0)

if shinput == "正常启动":
    launch_mode = 0
elif shinput == "以 歌曲下载 模式启动":
    print("\n以" + Fore.GREEN + "歌曲下载" + Fore.RESET + "模式启动。")
    launch_mode = 1
elif shinput == "以 配置修改 模式启动":
    print("\n以" + Fore.GREEN + "配置模式" + Fore.RESET + "模式启动。")
    launch_mode = 2
elif shinput == "打开歌曲文件夹":
    os.system("start %CD%\\PLiveMSCdl\\")
    exit()
else:
    exit()

latest_user = ""
latest_message = ""
latest_timeline = ""

def recv_danmaku():
    try:
        global latest_message, latest_user, latest_timeline, roomid, return_danmaku
        # Get danmaku
        response = requests.get(url="https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid=" + roomid, headers=headers)
        danmaku = response.json()["data"]["room"][-1]
        if latest_timeline != danmaku["timeline"]:
            latest_user = danmaku["nickname"]
            latest_message = danmaku["text"]
            latest_timeline = danmaku["timeline"]
            print("[" + Fore.GREEN + danmaku["timeline"] + Fore.RESET + "] " + Fore.BLUE + latest_user + Fore.RESET + ": \a" + Fore.YELLOW + latest_message + Fore.RESET)
            return True
    except IndexError: # If the danmaku doesn't exist the parsing will directly trigger an Index Error.
        print(Fore.RED + "直播间无弹幕或直播间不存在；解决方式：尝试往直播间发送弹幕。" + Fore.RESET)
        return False 

def login():
    while True:
        try:
            time.sleep(1)
            userid = randstr(random.randint(5, 12))
            account = LoginViaAnonymousAccount(userid) # Login to Netease Music.
            break
        except AssertionError:
            print(f"{Fore.RED}无法使用访客身份 {Fore.RESET}[{Fore.BLUE}{userid}{Fore.RESET}]{Fore.RED} 登录，正在重试。{Fore.RESET}")
    if str(account["content"]["code"]) == "200":
        print(Fore.GREEN + "登录成功！" + Fore.RESET + "使用访客身份 [" + Fore.BLUE + userid + Fore.RESET + "] 登录。" + Fore.RESET, end="")

def callmpg123():
    os.popen("lib\mpg123.exe -q temp.mp3") # call mpg123 to play music.

def play(msc):
    print("正在搜索:", Fore.BLUE + msc + Fore.RESET)
    # Search for music and pick the first one to play
    # song title
    if "id:" == msc[0:3]:
        try:
            url = pyncm.apis.track.GetTrackAudio(msc[3:])
            if url["data"][0]["url"] is None:
                print(Fore.RED + "歌曲已下架或需要 VIP。", Fore.RESET)
                return 0
            else:
                print("\n正在下载音频文件。。。") 
                bar.get((url["data"][0]["url"]), "./temp.mp3", "下载中")
                    
                with open("./PLiveMSCdl/id_" + msc[3:] + ".mp3", "wb") as fa:
                    fa.write(content)
                print(f"开始播放 ID 歌曲。：{Fore.BLUE}{msc[3:]}{Fore.RESET}\n", end="")
                return 0
        except IndexError:
            print(Fore.RED + "无法下载。", Fore.RESET)  
    tracks = pyncm.apis.cloudsearch.GetSearchResult(msc)
    if not tracks["code"] == 200:
        return 2
    if skip_vip is True:
        if tracks["result"]["songCount"] == 0:
            return 3
        for a in range(len(tracks["result"]["songs"])):
            try:
                print(Fore.BLUE + tracks["result"]["songs"][a]["name"] + " (" + Fore.RED + str(tracks["result"]["songs"][a]["id"]) + Fore.RESET + ")", end=" - ")
            except KeyError:
                return 0

            for i in tracks["result"]["songs"][a]["ar"]: # artist
                print(Fore.YELLOW + i["name"] + Fore.RESET, "(" + Fore.RED + str(i["id"]) + Fore.RESET + ")", end=" ")
            
            # Get the audio info, using the ids from the search.
            url = pyncm.apis.track.GetTrackAudio(tracks["result"]["songs"][a]["id"])
            try:
                if url["data"][0]["url"] is None:
                    print(Fore.RED + "歌曲已下架或需要 VIP。", Fore.RESET)
                else:
                    artist = ""

                    for s in tracks["result"]["songs"][a]["ar"]: # artist
                        #print(Fore.YELLOW + i["name"] + Fore.RESET, "(" + Fore.RED + str(i["id"]) + Fore.RESET + ")", end=" ")
                        artist = artist + s["name"] + ", "
        
                    artist = artist[0:-2]
                    content = requests.get((url["data"][0]["url"])).content
                    print("\n正在下载音频文件。。。") 
                    bar.get(url["data"][0]["url"], "./temp.mp3", "下载中")
                    bar.ins(url["data"][0]["url"], "./PLiveMSCdl/" + tracks["result"]["songs"][0]["name"] + " - " + artist + ".mp3")

                    print("开始播放：", end="")
                    print(Fore.BLUE + tracks["result"]["songs"][a]["name"] + Fore.RESET, end=" - ")
                    print(Fore.YELLOW + artist + Fore.RESET)
                    
                    
                    break
            except IndexError:
                print(Fore.RED + "无法下载。", Fore.RESET)
    else:
        try:
            print(Fore.BLUE + tracks["result"]["songs"][0]["name"] + " (" + Fore.RED + str(tracks["result"]["songs"][0]["id"]) + Fore.RESET + ")", end=" - ")
        except KeyError:
            return 0
        for i in tracks["result"]["songs"][0]["ar"]: # artist
            print(Fore.YELLOW + i["name"] + Fore.RESET, "(" + Fore.RED + str(i["id"]) + Fore.RESET + ")", end=" ")
        # Get the audio info, using the ids from the search.
        url = pyncm.apis.track.GetTrackAudio(tracks["result"]["songs"][0]["id"])
        try:
            if url["data"][0]["url"] is None:
                print(Fore.RED + "歌曲已下架或需要 VIP。", Fore.RESET)
            else:
                artist = ""
                for s in tracks["result"]["songs"][0]["ar"]: # artist
                    #print(Fore.YELLOW + i["name"] + Fore.RESET, "(" + Fore.RED + str(i["id"]) + Fore.RESET + ")", end=" ")
                    artist = artist + s["name"] + ", "
                artist = artist[0:-2]
                print("\n正在下载音频文件。。。") 
                bar.get(url["data"][0]["url"], "./temp.mp3", "下载中")
                bar.ins(url["data"][0]["url"], "./PLiveMSCdl/" + tracks["result"]["songs"][0]["name"] + " - " + artist + ".mp3")

                print("开始播放：", end="")
                print(Fore.BLUE + tracks["result"]["songs"][0]["name"] + Fore.RESET, end=" - ")
                print(Fore.YELLOW + artist + Fore.RESET)
                
        except IndexError:
            print(Fore.RED + "无法下载。", Fore.RESET)
        
        

return_danmaku = ""
latest_message = ""


#print(test)
def check_config():
    global roomid, skip_vip
    try:
        if not os.path.isfile("user.json"):
            print("检测到是第一次运行。")
            try:
                if easygui.ynbox(msg="检测到你是第一次运行 LiveMSC。\n如果您能接受并理解此分支版本可能有未知的 Bug 以及问题，并且我遇到问题后会及时跟开发者反馈，可点击确认开始使用。", title="PLiveMSC " + version, choices=["确认", "退出"]):
                    pass
                else:
                    exit()
            except TypeError:
                exit()
            print("正在初始化配置...")
            while True: # The user exits the loop by entering the correct roomid.
                try:
                    roomid = int(easygui.enterbox("请输入你的直播间房间号。", title="PLiveMSC " + version))  
                
                except ValueError:
                    easygui.msgbox("房间号只能是数字！\n\n如果你不知道你的直播间号，请将此链接复制到浏览器中打开。\nhttps://link.bilibili.com/p/center/index#/my-room/start-live", "LiveMSC v0.1 Alpha")
                except TypeError:
                    exit()
                with open("user.json", "w") as f:
                    f.write(json.dumps({
                    "roomid": roomid,
                    "skip_vip": False,
                }))
                print("请重新启动" + Fore.MAGENTA + " LiveMSC " + Fore.RESET + "。")
                exit()
        
        else: # Load config.
            with open("user.json") as f:
                config = json.loads(f.read())
                roomid = str(config["roomid"])
                skip_vip = config["skip_vip"]
            
            print("房间号: " + Fore.MAGENTA + roomid + Fore.RESET)
            if skip_vip is True:
                print("跳过 VIP 歌曲: " + Fore.MAGENTA + "开启" + Fore.RESET)
            else:
                print("跳过 VIP 歌曲: " + Fore.MAGENTA + "关闭" + Fore.RESET)
            line()
    except json.decoder.JSONDecodeError: # If can't decode the config
        print(Fore.RED + "读取 Json 配置文件出现错误。" + Fore.RESET)
        print("请重新启动" + Fore.MAGENTA + " LiveMSC " + Fore.RESET + "以重新生成配置文件。")
        os.remove("user.json")
        exit()
    #tracks = pyncm.apis.track.GetTrackAudio(song_ids = (496869422), bitrate = 320000, encodeType = "aac")
    
def dl(msc):
    os.makedirs("PLiveMSCdl", exist_ok=True)
    print(Fore.RESET + "正在搜索:", Fore.BLUE + msc + Fore.RESET)
    tracks = pyncm.apis.cloudsearch.GetSearchResult(msc) 

    try:
        for b in range(len(tracks["result"]["songs"])-1):
            print(Fore.GREEN + str(b) + Fore.RESET + ". " + Fore.BLUE + tracks["result"]["songs"][b]["name"] + Fore.RESET + " (" + Fore.RED + str(tracks["result"]["songs"][b]["id"]) + Fore.RESET + ")", end=" - ")
            a = ""
            for i in tracks["result"]["songs"][b]["ar"]: # artist
                print(Fore.YELLOW + i["name"] + Fore.RESET, "(" + Fore.RED + str(i["id"]) + Fore.RESET + ")", end=" ")
                a = a + i["name"] + ", "
            print()
    except Exception as f:
        print(f)
    
    print("\n选择一个你需要下载的，然后按下 Enter 开始下载。")
    while True:
        try:
            shinput = int(input(">"))
            break
        except KeyboardInterrupt:
            exit()
        except:
            print("非正确的数字，请重新输入。")
    # Get the audio info, using the ids from the search.
    url = pyncm.apis.track.GetTrackAudio(tracks["result"]["songs"][shinput]["id"])
    #print(url["data"][0]["url"])
    if not url["data"][0]["url"] is None: # If the song does not require "vip" to be downloaded
        a = ""
        for i in tracks["result"]["songs"][shinput]["ar"]: # artist
            a = a + i["name"] + ", "
        a = a[0:-2]
        print("\n正在下载音频文件。。。")    
        bar.get((pyncm.apis.track.GetTrackAudio(tracks["result"]["songs"][shinput]["id"])["data"][0]["url"]), "./PLiveMSCdl/" + tracks["result"]["songs"][shinput]["name"] + " - " + a + ".mp3", "下载中")
        print("下载成功:", os.getcwd().replace("\\", "/") + "/PLiveMSCdl/" + tracks["result"]["songs"][shinput]["name"] + " - " + a + ".mp3")
        
    else:
        print(Fore.RED + "歌曲已下架或需要 VIP。", Fore.RESET)



print("\n正在登录到网易云音乐...")
try:
    login()
except requests.exceptions.ProxyError:
    print(Fore.RED + "ProxyError" + Fore.RESET + ": 检查你的" + Fore.BLUE + "系统代理"+ Fore.RESET + "处于关闭状态。")
    exit()
if launch_mode == 0:
    print(Fore.BLUE + "开始弹幕接收和歌曲解析。", Fore.RESET)
    line()
else:
    print("\n")
    line()

def showlist():
    global musiclist
    
    if len(musiclist) == 0:
        print(Fore.RED + "当前列表为空。" + Fore.RESET)
    for i in range(len(musiclist)):
        print("当前搜索列表")
        print(Fore.BLUE + str(i+1) + Fore.RESET + ". " + Fore.YELLOW + musiclist[i] + Fore.RESET)

timeline = ""
musiclist = []
try:
    if launch_mode == 0:
        try:
            print("正在检查配置文件...")
            check_config()
            while True:
                time.sleep(1)
                if recv_danmaku() is False:
                    pass
                else:
                    if timeline != latest_timeline:
                        timeline = latest_timeline
                        if "点歌" in latest_message:
                            print("用户", Fore.BLUE + latest_user + Fore.RESET, "触发了点歌:", Fore.YELLOW + latest_message.split("点歌")[-1][1:].strip("\r") + Fore.RESET, "，已加入到点歌列表。")
                            musiclist.append(latest_message.split("点歌")[-1][1:].strip("\r"))
                            line()
                            showlist()
                            line()
                if len(musiclist) >= 1:
                    if processlib.search("mpg123.exe") is False:
                        ret = play(musiclist[0])
                        if ret == 3:
                            print(Fore.RED + "没有搜索到该歌曲，已从列表撤销。" + Fore.RESET)
                            del musiclist[0]
                            line()
                            showlist()
                            line()
                        elif ret == 2:
                            print(Fore.RED + "搜索出现异常。" + Fore.RESET)
                        else:
                            callmpg123()
                            del musiclist[0]
                            line()
                            showlist()
                            line()
                    
        except KeyboardInterrupt:
            sys.exit()
    elif launch_mode == 1:
        while True:
            print("输入歌曲名下载。")
            try:
                dl(input(">" + Fore.BLUE))
            except Exception as f:
                dl(input(">" + Fore.BLUE))
            except KeyboardInterrupt:
                exit()
                pass
    elif launch_mode == 2:
        try:
            with open("user.json") as f:
                config = json.loads(f.read())
        except FileNotFoundError:
            easygui.msgbox("请先正常启动 PLiveMSC 生成配置文件。", "PLiveMSC Configuration Menu", ok_button="确认")
            exit()
        skip_vip = config["skip_vip"]
        roomid = config["roomid"]
        while True:
            try:
                print(config)
                if skip_vip is True:
                    shinput = easygui.choicebox(title="PLiveMSC Configuration Menu", msg="双击一个项目来改变设置。", choices=["■ 自动跳过 VIP 歌曲", "○ 应用并退出", "○ 修改直播间号"])
                    if shinput == "■ 自动跳过 VIP 歌曲":
                        skip_vip = False
                else:
                    shinput = easygui.choicebox(title="PLiveMSC Configuration Menu", msg="双击一个项目来改变设置。", choices=["□ 自动跳过 VIP 歌曲", "○ 应用并退出", "○ 修改直播间号"])
                    if shinput == "□ 自动跳过 VIP 歌曲":
                        skip_vip = True
            except KeyError:
                easygui.msgbox("请先正常启动 PLiveMSC 以重新生成配置文件。", "PLiveMSC Configuration Menu", ok_button="确认")
                os.remove("user.json")
                exit()
            
            print(shinput)
            if shinput is None:
                print("用户指定：" + Fore.MAGENTA + "取消" + Fore.RESET + "。")
                exit()
            if shinput == "○ 修改直播间号":
                try:
                    roomid = easygui.enterbox("请输入你的直播间房间号。", "PLiveMSC Configuration Menu")
                    if not roomid:
                        roomid = config["roomid"]
                except ValueError:
                    easygui.msgbox("房间号只能是数字！\n\n如果你不知道你的直播间号，请将此链接复制到浏览器中打开。\nhttps://link.bilibili.com/p/center/index#/my-room/start-live", "LiveMSC v0.1 Alpha")
                except TypeError:
                    exit()
            if shinput == "○ 应用并退出":
                config["skip_vip"] = skip_vip
                config["roomid"] = int(roomid)
                with open("user.json", "w") as a:
                    a.write(json.dumps(config))
                exit()
except Exception as exc:
    print(Fore.RED + "PLiveMSC 崩溃了！" + Fore.RESET)
    print(Fore.RESET + "这通常是出现了某些无法尝试挽救的异常。我建议你重新运行 PLiveMSC，实在不行就让作者处理吧。")
    line()
    if processlib.search("mpg123.exe"):
        print("正在清理 mpg123 进程...")
        processlib.kill("mpg123.exe")
        line()
    print(traceback.format_exc())
    line()
    