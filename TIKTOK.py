def clear_status_lines(lines=7):
    sys.stdout.write('\x1b[1A\x1b[2K' * lines)
    sys.stdout.flush()

import os
import sys
import time
import random
import threading
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from colorama import Fore, Style, init
import json

# ===== Helper utilities (dynamic captcha, safe click, image save) =====
import base64, requests, urllib.parse
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
def save_element_image(driver, img_element, filename, base_url=None):
    """Save screenshot of element; fallback fetch src"""
    try:
        data = img_element.screenshot_as_png
        if data and len(data)>0:
            with open(filename,'wb') as f: f.write(data); return
    except Exception: pass
    src_attr = img_element.get_attribute('src')
    if not src_attr: raise Exception('Captcha img missing src')
    if src_attr.startswith('data:image'):
        header, b64data = src_attr.split(',',1)
        with open(filename,'wb') as f: f.write(base64.b64decode(b64data))
    else:
        if base_url and src_attr.startswith('/'):
            src_attr = urllib.parse.urljoin(base_url, src_attr)
        r = requests.get(src_attr, headers={'User-Agent':'Mozilla/5.0'}); r.raise_for_status()
        with open(filename,'wb') as f: f.write(r.content)

def wait_any(driver, selectors, timeout=10):
    for by, sel in selectors:
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, sel)))
        except TimeoutException:
            continue
    raise TimeoutException('None of the selectors found')

def safe_click(elem, driver=None):
    try:
        elem.click()
        return True
    except (ElementClickInterceptedException, Exception):
        if driver:
            driver.execute_script("arguments[0].click();", elem)
            return True
    return False
from concurrent.futures import ThreadPoolExecutor

# Khởi tạo colorama
init()

# Thông tin hiện tại
CURRENT_TIME = "2025" 
CURRENT_USER = "NGUYENLAM"

# Màu sắc
luc = "\033[1;32m"
trang = "\033[1;37m"
do = "\033[1;31m"
vang = "\033[0;93m"
hong = "\033[1;35m"
xduong = "\033[1;34m"
lam = "\033[1;36m"
red = '\u001b[31;1m'

# Biến global
driver = None
nreer_driver = None
running = True
likes_count = 0
followers_count = 0  
views_count = 0
shares_count = 0
favorites_count = 0
comment_likes_count = 0

def clear_screen():
    """Xóa màn hình terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text, delay=0.001):
    """In chữ với hiệu ứng chậm"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def load_animation(text, duration=3):
    """Hiệu ứng loading với thanh tiến trình"""
    animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{text} {animation[i % len(animation)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * (len(text) + 2) + "\r")
    sys.stdout.flush()

def print_banner():
    banner = f"""
\033[38;2;255;20;147m┏━━━❨❨★ ❩❩━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❨❨★ ❩❩━━━┓

\033[1;31m████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗                               
\033[1;31m╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝
\033[1;31m   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝ 
\033[1;31m   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗ 
\033[1;31m   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗
\033[1;31m   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝

\033[1;33m████████╗ ██████╗  ██████╗ ██╗      ███████╗
\033[1;33m╚══██╔══╝██╔═══██╗██╔═══██╗██║      ██╔════╝
\033[1;33m   ██║   ██║   ██║██║   ██║██║      ███████╗
\033[1;33m   ██║   ██║   ██║██║   ██║██║      ╚════██║
\033[1;33m   ██║   ╚██████╔╝╚██████╔╝███████╗ ███████║
\033[1;33m   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝ ╚══════╝\033[0m

\033[1;36m⭐️ DEVELOPED BY: \033[1;97mnglam
\033[1;36m⭐️FACEBOOK   : \033[1;97mhttps://www.facebook.com/nguyen.lam.227636/?locale=vi_VN
\033[1;36m⭐️ ZALO       : \033[1;97m0972882215
\033[1;36m⭐️ WEBSITE    : \033[1;97mNHO1NGUOI
\033[1;36m⭐️ VERSION    : \033[1;97m2.0.3 (free)
\033[1;36m⭐️ TIME       : \033[1;97m{CURRENT_TIME}
\033[1;36m⭐️ ADMIN      : \033[1;97m{CURRENT_USER}
\033[1;95m                  ╭─━━━━━━━━━━━━━━━━━━━━─╮
                  │   TIKTOK BOT DEV  │
                  ╰─━━━━━━━━━━━━━━━━━━━━─╯
\033[38;2;255;20;147m┗━━━❨❨★ ❩❩━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❨❨★ ❩❩━━━┛
"""
    print_slow(banner, 0.000001)

def print_menu():
    menu = f"""
\033[38;2;255;20;147m┏━━━❨❨★ ❩❩━━━━━━━━━━━ MENU CHÍNH ━━━━━━━━━━❨❨★ ❩❩━━━┓
\033[1;36m            ╭─━━━━━━━━━━━━━━━━━━━━─╮
            │    THÔNG TIN TOOL    │
            ╰─━━━━━━━━━━━━━━━━━━━━─╯
\033[1;36m     ╭─━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
     │  \033[1;97m[1]🚀 Tăng Follow Một Profile(🟢on)  \033[1;36m│
     │  \033[1;97m[2]🚀 Tăng Follow Nhiều Profile(🟢on)\033[1;36m│
     │  \033[1;97m[3]💖 Tăng Like Một Video(🟢on)      \033[1;36m│
     │  \033[1;97m[4]💖 Tăng Like Nhiều Video(🟢on)    \033[1;36m│
     │  \033[1;97m[5]👀 Tăng View Một Video(🟢on)      \033[1;36m│
     │  \033[1;97m[6]👀 Tăng View Nhiều Video(🟢on)    \033[1;36m│
     │  \033[1;97m[7]🔄 Tăng Share Một Video(🟢on)     \033[1;36m│
     │  \033[1;97m[8]🔄 Tăng Share Nhiều Video(🟢on)   \033[1;36m│
     │  \033[1;97m[9]⭐ Tăng Favorite Một Video(🟢on)  \033[1;36m│
     │  \033[1;97m[10]⭐Tăng Favorite Nhiều Video(🟢on)\033[1;36m│
     │  \033[1;97m[11]👍 Comment Like Một Video(🟢on)  \033[1;36m│
     │  \033[1;97m[12]👍 Comment Like Nhiều Video(🟢on)\033[1;36m│
     │  \033[1;97m[13]🌟 Chạy Gộp Tất Cả(🟢on)         \033[1;36m│
     │  \033[1;97m[14]ℹ️  Thông Tin Tool                 \033[1;36m│
     │  \033[1;97m[15]📝 Hướng Dẫn Sử Dụng              \033[1;36m│
     │  \033[1;97m[16]📊 Xem Thống Kê                   \033[1;36m│
     │  \033[1;97m[0]❌ Thoát                           \033[1;36m│
     ╰─━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
"""
    print_slow(menu, 0.001)

    

def openZefoy():
    """Mở Zefoy & Nreer, chặn quảng cáo, xử lý captcha thủ công"""
    global driver, nreer_driver
    try:
        zefoy_options = uc.ChromeOptions()
        nreer_options = uc.ChromeOptions()
        for opts in (zefoy_options, nreer_options):
            opts.add_argument('--disable-notifications')
            opts.add_argument('--mute-audio')
            opts.add_argument('--window-size=1366,768')

        driver = uc.Chrome(options=zefoy_options, use_subprocess=True)
        nreer_driver = uc.Chrome(options=nreer_options, use_subprocess=True)

        ad_urls = ['https://fundingchoicesmessages.google.com/*','*doubleclick.net/*','*googlesyndication.com/*','*adservice.google.*']
        for drv in (driver, nreer_driver):
            try:
                drv.execute_cdp_cmd('Network.setBlockedURLs', {'urls': ad_urls})
                drv.execute_cdp_cmd('Network.enable', {})
            except Exception: pass

        # === Zefoy ===
        print(f"{luc}[*] Mở Zefoy ...")
        driver.get('https://zefoy.com/')
        captcha_img = wait_any(driver, [
            (By.CSS_SELECTOR, 'form div img'),
            (By.CSS_SELECTOR, 'img[src*="captcha"]'),
            (By.XPATH, '//form//img[contains(@src,"captcha")]')])
        save_element_image(driver, captcha_img, 'captcha.png', base_url='https://zefoy.com')
        print(f"{luc}[*] Đã lưu captcha Zefoy -> captcha.png")
        cap1 = input(f"{luc}[?] Nhập captcha Zefoy: {trang}")
        captcha_input = wait_any(driver, [
            (By.CSS_SELECTOR, 'form input[type="text"]'),
            (By.XPATH, '//form//input[1]')])
        captcha_input.send_keys(cap1)
        submit_btn = wait_any(driver, [
            (By.CSS_SELECTOR, 'form button'),
            (By.XPATH, '//form//button')])
        safe_click(submit_btn, driver)
        time.sleep(2)

        # === Nreer ===
        print(f"{luc}[*] Mở Nreer ...")
        nreer_driver.get('https://nreer.com/')
        captcha2 = wait_any(nreer_driver, [(By.XPATH,'//*[@id="msg"]/div[2]/img')])
        save_element_image(nreer_driver, captcha2, 'captcha2.png', base_url='https://nreer.com')
        print(f"{luc}[*] Đã lưu captcha Nreer -> captcha2.png")
        cap2 = input(f"{luc}[?] Nhập captcha Nreer: {trang}")
        input2 = nreer_driver.find_element(By.XPATH,'//*[@id="cat"]/input')
        input2.send_keys(cap2)
        nreer_driver.find_element(By.XPATH,"//button[contains(@class,'btn-dark')]").click()
        time.sleep(2)
        try:
            nreer_driver.find_element(By.CSS_SELECTOR,'.btn.btn-primary.btn-lg.btn-block').click()
        except:
            pass
        return True
    except Exception as e:
        print(f"{do}[!] Lỗi openZefoy: {e}")
        try:
            driver.quit(); nreer_driver.quit()
        except: pass
        return False


def solve_nreer_captcha():
    try:
        captcha_img = nreer_driver.find_element(By.XPATH, '//*[@id="msg"]/div[2]/img')
        with open('captcha.png', 'wb') as f:
            f.write(captcha_img.screenshot_as_png)
            
        print(f"{luc}[*] Đã lưu captcha vào file captcha.png")
        captcha_value = input(f"{luc}[?] Nhập captcha: {trang}")
        
        input_box = nreer_driver.find_element(By.XPATH, '//*[@id="cat"]/input')
        input_box.send_keys(captcha_value)
        time.sleep(1)
        
        submit_btn = nreer_driver.find_element(By.XPATH, "//button[contains(@class, 'btn-dark')]")
        submit_btn.click()
        time.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"{do}[!] Lỗi khi xử lý captcha nreer: {str(e)}")
        return False
    
def solve_captcha():
    """Xử lý captcha"""
    try:
        # Lưu ảnh captcha
        captcha_img = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/form/div/div/img')
        with open('captcha.png', 'wb') as f:
            f.write(captcha_img.screenshot_as_png)
            
        print(f"{luc}[*] Đã lưu captcha vào file captcha.png")
        captcha_value = input(f"{luc}[?] Nhập captcha: {trang}")
        
        # Nhập captcha
        captcha_input = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/form/div/div/div/input[1]')
        captcha_input.send_keys(captcha_value)
        time.sleep(1)
        
        # Click submit
        submit_btn = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/form/div/div/div/div/button')
        submit_btn.click()
        time.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"{do}[!] Lỗi khi xử lý captcha: {str(e)}")
        return False


def increase_likes(video_url):
    """Tăng tim tự động, đếm chính xác, không nhảy menu"""
    global driver, nreer_driver, likes_count, running
    # mở tab hearts
    try:
        safe_click(driver.find_element(By.XPATH, "//button[contains(@class,'t-hearts-button')]"), driver)
    except: pass
    # set url
    try:
        heart_in = driver.find_element(By.XPATH, "//form//input[@type='text']")
        heart_in.clear(); heart_in.send_keys(video_url)
    except: pass
    # nreer set url
    try:
        safe_click(nreer_driver.find_element(By.CSS_SELECTOR,'.btn.btn-primary.btn-lg.btn-block'), nreer_driver)
    except: pass
    try:
        nreer_in = nreer_driver.find_element(By.CSS_SELECTOR,'.form-control.form-control-lg')
        nreer_in.clear(); nreer_in.send_keys(video_url)
    except: pass

    while running:
        acted=False
        # Zefoy
        try:
            safe_click(driver.find_element(By.XPATH,"//button[contains(text(),'Search') or contains(@class,'search')]"))
            send_btn = WebDriverWait(driver,8).until(
                EC.element_to_be_clickable((By.XPATH,"//form//button[contains(text(),'Send')]")))
            m = re.search(r'(\d+)', send_btn.text)
            plus = int(m.group(1)) if m else 25
            safe_click(send_btn, driver)
            likes_count += plus; acted=True
        except: pass
        # Nreer
        try:
            btn = nreer_driver.find_element(By.XPATH,"//button[contains(@onclick,'heart') and not(contains(@disabled,'disabled'))]")
            safe_click(btn, nreer_driver)
            time.sleep(1)
            try:
                nreer_driver.find_element(By.XPATH,"//button[@data-dismiss='modal' or contains(@class,'close')]").click()
            except: pass
            likes_count += 25; acted=True
        except: pass
        # print status single line
        sys.stdout.write(f"\r{luc}❤  Tổng tim đã buff: {likes_count} \033[K"); sys.stdout.flush()
        time.sleep(3 if acted else 6)


def increase_likes_server2(video_url):
    """Tăng like cho video sử dụng Server 2"""
    global likes_count
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi,en-US;q=0.7,en;q=0.6',
        'cache-control': 'max-age=0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }
    
    while running:
        try:
            access = requests.get('https://tikfollowers.com/free-tiktok-likes', headers=headers)
            session = access.cookies.get('ci_session', '')
            headers.update({'cookie': f'ci_session={session}'})
            token = access.text.split("csrf_token = '")[1].split("'")[0]

            data = f'{{"type":"like","q":"{video_url}","google_token":"t","token":"{token}"}}'
            search = requests.post('https://tikfollowers.com/api/free', headers=headers, data=data).json()

            if search.get('success'):
                data_like = search['data']
                data = f'{{"google_token":"t","token":"{token}","data":"{data_like}","type":"like"}}'
                send_like = requests.post('https://tikfollowers.com/api/free/send', headers=headers, data=data).json()

                if send_like.get('o') == 'Success!' and send_like.get('success'):
                    likes_count += 15
                    # Sau khi tăng thành công, chờ 3 giây
                    countdown_timer(3, "", likes_count, is_follow=False)

                elif send_like.get('o') == 'Oops...' and not send_like.get('success'):
                    try:
                        wait_time = int(send_like['message'].split('You need to wait for a new transaction. : ')[1].split(' Minutes')[0]) * 60
                        countdown_timer(wait_time, "", likes_count, is_follow=False)
                        continue
                    except:
                        pass

        except Exception as e:
            print(f"{do}[!] Lỗi: {str(e)}")
            time.sleep(5)
def show_server_menu():
    """Hiển thị menu chọn server"""
    print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║              CHỌN SERVER TĂNG LIKE          ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ [1] Server 1 - Ổn định (Cần Captcha)        ║
{luc}║ [2] Server 2 - Tốc độ nhanh (Không Captcha) ║
{luc}║ [=>] Nên chọn Server 1 để chạy Server 2 lúc ║
{luc}║      chạy được lúc không                    ║
{luc}╚═════════════════════════════════════════════╝""")



def countdown_timer(seconds, username, count, is_follow=True):
    """Hiển thị countdown timer trong bảng trạng thái"""
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f'{mins:02d}:{secs:02d}'
        
        # Xóa bảng cũ
        sys.stdout.write('\x1b[1A\x1b[2K' * 7)
        
        if is_follow:
            print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║             ĐANG CHẠY TĂNG FOLLOW           ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ Username: @{username:<30}║
{luc}║ Trạng thái: Đang chờ [{timer}]              ║
{luc}║ Số follow đã tăng: {count:<24}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")
        else:
            print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║             ĐANG CHẠY TĂNG LIKE            ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Đang chờ [{timer}]              ║
{luc}║ Số like đã tăng: {count:<25}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}║ Vui lòng check TikTok                      ║
{luc}╚═════════════════════════════════════════════╝""")
        
        time.sleep(1)
        seconds -= 1

def increase_followers(username):
    """Tăng follower cho profile"""
    global followers_count
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi,en-US;q=0.7,en;q=0.6',
        'cache-control': 'max-age=0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    while running:
        try:
            access = requests.get('https://tikfollowers.com/free-tiktok-followers', headers=headers)
            session = access.cookies.get('ci_session', '')
            headers.update({'cookie': f'ci_session={session}'})
            token = access.text.split("csrf_token = '")[1].split("'")[0]

            data = f'{{"type":"follow","q":"@{username}","google_token":"t","token":"{token}"}}'
            search = requests.post('https://tikfollowers.com/api/free', headers=headers, data=data).json()

            if search.get('success'):
                data_follow = search['data']
                data = f'{{"google_token":"t","token":"{token}","data":"{data_follow}","type":"follow"}}'
                send_follow = requests.post('https://tikfollowers.com/api/free/send', headers=headers, data=data).json()

                if send_follow.get('o') == 'Success!' and send_follow.get('success'):
                    followers_count += 10
                    # Sau khi tăng thành công, chờ 3 giây
                    countdown_timer(3, username, followers_count)

                elif send_follow.get('o') == 'Oops...' and not send_follow.get('success'):
                    try:
                        wait_time = int(send_follow['message'].split('You need to wait for a new transaction. : ')[1].split(' Minutes')[0]) * 60
                        countdown_timer(wait_time, username, followers_count)
                        continue
                    except:
                        pass

        except Exception as e:
            print(f"{do}[!] Lỗi: {str(e)}")
            time.sleep(5)
def increase_views(video_url):
    """Tăng view cho video"""
    global driver, views_count
    try:
        driver.find_element(By.XPATH, "//button[@class='btn btn-primary rounded-0 t-views-button']").click()
        time.sleep(1)
        
        input_box = driver.find_element(By.XPATH, '/html/body/div[10]/div/form/div/input')
        input_box.send_keys(video_url)
        time.sleep(1)
        
        print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║             ĐANG CHẠY TĂNG VIEW            ║ 
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Đang chạy                       ║
{luc}║ Số view đã tăng: {views_count:<25}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")
        
        while running:
            try:
                search_btn = driver.find_element(By.XPATH, '/html/body/div[10]/div/form/div/div/button')
                search_btn.click()
                time.sleep(1)
                
                submit_btn = driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div[1]/div/form/button')
                submit_btn.click()
                
                views_count += 500
                sys.stdout.write('\x1b[1A\x1b[2K' * 7)
                print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║             ĐANG CHẠY TĂNG VIEW            ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Tăng thành công ✓               ║
{luc}║ Số view đã tăng: {views_count:<25}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")
                time.sleep(3)
                
            except:
                sys.stdout.write('\x1b[1A\x1b[2K' * 7) 
                print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║             ĐANG CHẠY TĂNG VIEW            ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Đang chờ cooldown...            ║
{luc}║ Số view đã tăng: {views_count:<25}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")
                time.sleep(3)
                
    except Exception as e:
        print(f"{do}[!] Lỗi khi tăng view: {str(e)}")


def increase_shares(video_url):
    """Tăng share cho video"""
    global driver, nreer_driver, shares_count
    try:
        # Setup Zefoy
        share = driver.find_element(By.XPATH, "//button[@class='btn btn-primary rounded-0 t-shares-button']").click()
        time.sleep(1)
        
        input_box = driver.find_element(By.XPATH, '/html/body/div[11]/div/form/div/input')
        input_box.send_keys(video_url)
        time.sleep(1)

        # Setup Nreer
        max_retries = 3
        retry_count = 0 
        nreer_setup = False

        while retry_count < max_retries and not nreer_setup:
            try:
                use_button = nreer_driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-lg.btn-block')
                use_button.click()
                time.sleep(3)
                
                enterURL = nreer_driver.find_element(By.CSS_SELECTOR, '.form-control.form-control-lg')
                enterURL.clear()
                enterURL.send_keys(video_url) 
                time.sleep(1)
                
                search = nreer_driver.find_element(By.XPATH, '//*[@id="form1"]/div/div/button')
                search.click()
                time.sleep(2)
                nreer_setup = True
            except:
                retry_count += 1
                time.sleep(2)
                try:
                    nreer_driver.refresh()
                    time.sleep(3)  
                except:
                    pass

        print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║             ĐANG CHẠY TĂNG SHARE            ║ 
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Đang chạy                       ║
{luc}║ Số share đã tăng: {shares_count:<25}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")

        while running:
            # Zefoy share
            try:
                search_btn = driver.find_element(By.XPATH, '/html/body/div[11]/div/form/div/div/button')
                search_btn.click()
                time.sleep(1)
                
                submit_btn = driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div[1]/div/form/button')  
                submit_btn.click()
                shares_count += 150
                
                sys.stdout.write('\x1b[1A\x1b[2K' * 7)
                print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║             ĐANG CHẠY TĂNG SHARE            ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Tăng thành công ✓               ║
{luc}║ Số share đã tăng: {shares_count:<25}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")
                time.sleep(3)
                
            except:
                sys.stdout.write('\x1b[1A\x1b[2K' * 7)
                print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║             ĐANG CHẠY TĂNG SHARE            ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Đang chờ cooldown...            ║
{luc}║ Số share đã tăng: {shares_count:<25}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")
                time.sleep(3)

            # Nreer share
            try:
                # Click nút share
                share_button = nreer_driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div/div/div[1]/button[6]')
                share_button.click()
                time.sleep(5)
                
                # Click nút close
                close_button = nreer_driver.find_element(By.XPATH, '//*[@id="bootstrap-show-modal-0"]/div/div/div[1]/button')
                close_button.click()
                
                shares_count += 200
                sys.stdout.write('\x1b[1A\x1b[2K' * 7)
                print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║             ĐANG CHẠY TĂNG SHARE            ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Tăng thành công ✓               ║
{luc}║ Số share đã tăng: {shares_count:<25}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")
                time.sleep(2)
                
            except:
                try:
                    search_button = nreer_driver.find_element(By.XPATH, '//*[@id="form1"]/div/div/button')
                    search_button.click()
                    time.sleep(2)
                    
                    enterURL = nreer_driver.find_element(By.CSS_SELECTOR, '.form-control.form-control-lg')
                    enterURL.clear()
                    enterURL.send_keys(video_url)
                    time.sleep(1)
                except:
                    pass

    except Exception as e:
        print(f"{do}[!] Lỗi khi tăng share: {str(e)}")
def run_multi_shares():
    """Chạy nhiều video share luân phiên"""
    global running, shares_count, CURRENT_TIME
    
    # Cập nhật thời gian hiện tại
    CURRENT_TIME = "2025-04-21 15:26:14"
    
    print(f"\n{luc}[*] Vui lòng nhập danh sách link video:")
    video_urls = get_url_list()
    
    if not video_urls:
        print(f"{do}[!] Không có link video nào được nhập!")
        return
        
    if not openZefoy():
        return

    current_index = 0
    count_per_video = 0
    
    while running:
        video_url = video_urls[current_index]
        
        # In thông tin tiến trình
        print(f"""
{luc}╔════════════════════════════════════════════╗
{luc}║             ĐANG CHẠY TĂNG SHARE           ║
{luc}╠════════════════════════════════════════════╣
{luc}║ Video hiện tại: {current_index + 1}/{len(video_urls)}                ║
{luc}║ Lần thứ: {count_per_video + 1}/10                         ║
{luc}║ Trạng thái: Đang xử lý...                   ║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚════════════════════════════════════════════╝""")
        
        try:
            # Click nút share
            driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div/div[7]/div/button').click()
            time.sleep(1)
            
            # Nhập URL video
            input_box = driver.find_element(By.XPATH, '/html/body/div[11]/div/form/div/input')
            input_box.send_keys(video_url)
            time.sleep(1)
            
            while count_per_video < 10 and running:
                try:
                    # Click search
                    search_btn = driver.find_element(By.XPATH, '/html/body/div[11]/div/form/div/div/button')
                    search_btn.click()
                    time.sleep(1)
                    
                    # Click submit
                    submit_btn = driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div[1]/div/form/button')
                    submit_btn.click()
                    
                    shares_count += 30
                    count_per_video += 1
                    
                    # Cập nhật trạng thái thành công
                    sys.stdout.write('\x1b[1A\x1b[2K' * 8)
                    print(f"""
{luc}╔════════════════════════════════════════════╗
{luc}║             ĐANG CHẠY TĂNG SHARE           ║
{luc}╠════════════════════════════════════════════╣
{luc}║ Video hiện tại: {current_index + 1}/{len(video_urls)}                ║
{luc}║ Lần thứ: {count_per_video}/10                         ║
{luc}║ Trạng thái: Tăng thành công ✓              ║
{luc}║ Đã tăng: {shares_count} shares                    ║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚════════════════════════════════════════════╝""")
                    
                    # Delay ngẫu nhiên
                    time.sleep(random.uniform(2.5, 4.0))
                    
                except Exception as e:
                    # Xử lý cooldown hoặc lỗi
                    sys.stdout.write('\x1b[1A\x1b[2K' * 8)
                    print(f"""
{luc}╔════════════════════════════════════════════╗
{luc}║             ĐANG CHẠY TĂNG SHARE           ║
{luc}╠════════════════════════════════════════════╣
{luc}║ Video hiện tại: {current_index + 1}/{len(video_urls)}                ║
{luc}║ Lần thứ: {count_per_video}/10                         ║
{luc}║ Trạng thái: Đang chờ cooldown...           ║
{luc}║ Đã tăng: {shares_count} shares                    ║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚════════════════════════════════════════════╝""")
                    time.sleep(random.uniform(4.0, 6.0))
            
            # Chuyển sang video tiếp theo khi hoàn thành 10 lần
            if count_per_video >= 10:
                print(f"\n{luc}[*] Đã hoàn thành {count_per_video} lần cho video {current_index + 1}")
                
                # Reset bộ đếm và chuyển video
                count_per_video = 0
                current_index = (current_index + 1) % len(video_urls)
                
                print(f"""
{luc}╔════════════════════════════════════════════╗
{luc}║           THÔNG TIN CHUYỂN VIDEO           ║
{luc}╠════════════════════════════════════════════╣
{luc}║ Tổng shares đã tăng: {shares_count}                  ║
{luc}║ Chuyển sang video: {current_index + 1}/{len(video_urls)}                ║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚════════════════════════════════════════════╝""")
                time.sleep(2)
                
        except Exception as e:
            # Xử lý lỗi chung
            print(f"""
{do}╔════════════════════════════════════════════╗
{do}║                 THÔNG BÁO LỖI              ║
{do}╠════════════════════════════════════════════╣
{do}║ Lỗi khi xử lý video {current_index + 1}                  ║
{do}║ Chi tiết: {str(e)[:30]}...          ║
{luc}║ Đang x2 chạy nhanh                         ║
{do}╚════════════════════════════════════════════╝""")
            time.sleep(2)
            continue

        # Kiểm tra nếu người dùng dừng tool
        if not running:
            print(f"""
{luc}╔════════════════════════════════════════════╗
{luc}║              KẾT THÚC TOOL                 ║
{luc}╠════════════════════════════════════════════╣
{luc}║ Tổng shares đã tăng: {shares_count}                  ║
{luc}║ Số video đã xử lý: {current_index + 1}/{len(video_urls)}                ║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚════════════════════════════════════════════╝""")

def increase_favorites(video_url):
    """Tăng favorite cho video"""  
    global driver, nreer_driver, favorites_count
    try:
        # Setup Zefoy
        driver.find_element(By.XPATH, "//button[@class='btn btn-primary rounded-0 t-favorites-button']").click()
        time.sleep(1)
        
        input_box = driver.find_element(By.XPATH, '/html/body/div[12]/div/form/div/input')
        input_box.send_keys(video_url)
        time.sleep(1)

        # Setup Nreer
        max_retries = 3
        retry_count = 0
        nreer_setup = False

        while retry_count < max_retries and not nreer_setup:
            try:
                use_button = nreer_driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-lg.btn-block')
                use_button.click()
                time.sleep(3)
                
                enterURL = nreer_driver.find_element(By.CSS_SELECTOR, '.form-control.form-control-lg')
                enterURL.clear()
                enterURL.send_keys(video_url)
                time.sleep(1)
                
                search = nreer_driver.find_element(By.XPATH, '//*[@id="form1"]/div/div/button')
                search.click()
                time.sleep(2)
                nreer_setup = True
            except:
                retry_count += 1
                time.sleep(2)
                try:
                    nreer_driver.refresh()
                    time.sleep(3)
                except:
                    pass

        print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║           ĐANG CHẠY TĂNG FAVORITE           ║ 
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Đang chạy                       ║
{luc}║ Số favorite đã tăng: {favorites_count:<23}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")

        while running:
            # Zefoy favorite
            try:
                search_btn = driver.find_element(By.XPATH, '/html/body/div[12]/div/form/div/div/button')
                search_btn.click()
                time.sleep(1)

                submit_btn = driver.find_element(By.XPATH, '/html/body/div[12]/div/div/div[1]/div/form/button') 
                submit_btn.click()
                favorites_count += 90
                
                sys.stdout.write('\x1b[1A\x1b[2K' * 7)
                print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║           ĐANG CHẠY TĂNG FAVORITE           ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Tăng thành công ✓               ║
{luc}║ Số favorite đã tăng: {favorites_count:<23}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")
                time.sleep(3)

            except:
                sys.stdout.write('\x1b[1A\x1b[2K' * 7)
                print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║           ĐANG CHẠY TĂNG FAVORITE           ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Đang chờ cooldown...            ║
{luc}║ Số favorite đã tăng: {favorites_count:<23}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")
                time.sleep(3)

            # Nreer favorite
            try:
                # Click nút favorite
                favorite_button = nreer_driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div/div/div[1]/button[2]')
                favorite_button.click()
                time.sleep(5)
                
                # Click nút close
                close_button = nreer_driver.find_element(By.XPATH, '//*[@id="bootstrap-show-modal-0"]/div/div/div[1]/button')
                close_button.click()
                
                favorites_count += 100
                sys.stdout.write('\x1b[1A\x1b[2K' * 7)
                print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║           ĐANG CHẠY TĂNG FAVORITE           ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Tăng thành công ✓               ║
{luc}║ Số favorite đã tăng: {favorites_count:<23}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")
                time.sleep(2)
                
            except:
                try:
                    search_button = nreer_driver.find_element(By.XPATH, '//*[@id="form1"]/div/div/button')
                    search_button.click()
                    time.sleep(2)
                    
                    enterURL = nreer_driver.find_element(By.CSS_SELECTOR, '.form-control.form-control-lg')
                    enterURL.clear()
                    enterURL.send_keys(video_url)
                    time.sleep(1)
                except:
                    pass

    except Exception as e:
        print(f"{do}[!] Lỗi khi tăng favorite: {str(e)}")
def increase_comment_likes(video_url):
    """Tăng comment like cho video"""
    global comment_likes_count
    try:
        # Click nút comment like - updated xpath
        driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div/div[4]/div/button').click()
        time.sleep(1)
        
        # Nhập URL video - updated xpath
        input_box = driver.find_element(By.XPATH, '/html/body/div[9]/div/form/div/input')
        input_box.send_keys(video_url)
        time.sleep(1)

        # In bảng thống kê ban đầu
        print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║         ĐANG CHẠY TĂNG COMMENT LIKE         ║ 
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Đang chạy                       ║
{luc}║ Số comment like đã tăng: {comment_likes_count:<19}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")

        while running:
            try:
                # Click search
                search_btn = driver.find_element(By.XPATH, '/html/body/div[9]/div/form/div/div/button')
                search_btn.click()
                time.sleep(1)

                # Kiểm tra thông báo lỗi 
                try:
                    error_msg = driver.find_element(By.CSS_SELECTOR, '.text-center.text-red-500')
                    if "Too many requests" in error_msg.text:
                        # Xóa 6 dòng trước
                        sys.stdout.write('\x1b[1A\x1b[2K' * 7)
                        print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║         ĐANG CHẠY TĂNG COMMENT LIKE         ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Đang chờ cooldown...            ║
{luc}║ Số comment like đã tăng: {comment_likes_count:<19}║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")
                        time.sleep(10)
                        continue
                except:
                    pass

                # Click submit
                submit_btn = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/div[1]/div/form/button')
                submit_btn.click()
                
                # Tăng số đếm và cập nhật giao diện
                comment_likes_count += 30
                # Xóa 6 dòng trước
                sys.stdout.write('\x1b[1A\x1b[2K' * 7)
                
                print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║         ĐANG CHẠY TĂNG COMMENT LIKE         ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Tăng thành công ✓               ║
{luc}║ Số comment like đã tăng: {comment_likes_count:<19}║
{luc}║ Vui lòng check tiktok                      ║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")

                # Delay ngẫu nhiên
                time.sleep(random.uniform(2.5, 4.0))

            except:
                # Xóa 6 dòng trước
                sys.stdout.write('\x1b[1A\x1b[2K' * 7)
                print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║         ĐANG CHẠY TĂNG COMMENT LIKE         ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ Trạng thái: Đang chờ cooldown...            ║
{luc}║ Số comment like đã tăng: {comment_likes_count:<19}║
{luc}║ Vui lòng check tiktok                      ║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚═════════════════════════════════════════════╝""")
                time.sleep(random.uniform(4.0, 6.0))

    except Exception as e:
        print(f"{do}[!] Lỗi khi tăng comment like: {str(e)}")

def show_stats():
    """Hiển thị thống kê"""
    print(f"""
{luc}╔═══════════════════════════════════╗
{luc}║          THỐNG KÊ HIỆN TẠI        ║
{luc}╠═══════════════════════════════════╣
{luc}║ Số likes đã tăng     : {trang}{likes_count:<11}{luc}║
{luc}║ Số follows đã tăng   : {trang}{followers_count:<11}{luc}║ 
{luc}║ Số views đã tăng     : {trang}{views_count:<11}{luc}║
{luc}║ Số shares đã tăng    : {trang}{shares_count:<11}{luc}║
{luc}║ Số favorites đã tăng : {trang}{favorites_count:<11}{luc}║
{luc}║ Comment likes đã tăng: {trang}{comment_likes_count:<11}{luc}║
{luc}╚═══════════════════════════════════╝
    """)

def show_info():
    """Hiển thị thông tin tool"""
    print(f"""
{luc}╔═══════════════════════════════════╗
{luc}║          THÔNG TIN TOOL           ║
{luc}╠═══════════════════════════════════╣
{luc}║ Phiên bản: {trang}2.0.3 Premium         {luc}║
{luc}║ Tác giả  : {trang}TienDev              {luc}║
{luc}║ Facebook : {trang}fb.com/tiendev.2000   {luc}║
{luc}║ Zalo    : {trang}0347160155            {luc}║
{luc}║ Website  : {trang}nguyennamtien.shop    {luc}║
{luc}║ => MUA TOOL KHÔNG CẦN VƯỢT KEY NHÉ           ║
{luc}╚═══════════════════════════════════╝
    """)

def show_guide():
    """Hiển thị hướng dẫn sử dụng"""
    print(f"""
{luc}╔═══════════════════════════════════════════════╗
{luc}║              HƯỚNG DẪN SỬ DỤNG               ║
{luc}╠═══════════════════════════════════════════════╣
{luc}║ 1. Chọn chức năng muốn sử dụng               ║
{luc}║ 2. Nhập link profile/video tiktok            ║
{luc}║ 3. Giải captcha khi được yêu cầu             ║
{luc}║ 4. Đợi tool hoạt động                        ║
{luc}║                                               ║
{luc}║ Lưu ý:                                       ║
{luc}║ - Mỗi lần tăng view sẽ được 1000 views       ║
{luc}║ - ...và các chức năng khác nữa               ║
{luc}║ => MUA TOOL KHÔNG CẦN VƯỢT KEY NHÉ           ║
{luc}╚═══════════════════════════════════════════════╝
    """)
def get_url_list():
    """Lấy danh sách URL từ người dùng"""
    urls = []
    print(f"\n{luc}[*] Nhập link (nhấn Enter 2 lần để kết thúc):")
    while True:
        url = input(f"{trang}=> ")
        if url == "":
            if len(urls) == 0:
                continue
            break
        urls.append(url)
    return urls
def run_multi_favorites():
    """Chạy nhiều video favorite luân phiên"""
    global running
    
    print(f"\n{luc}[*] Vui lòng nhập danh sách link video:")
    video_urls = get_url_list()
    
    if not video_urls:
        print(f"{do}[!] Không có link video nào được nhập!")
        return
        
    if not openZefoy():
        return

    current_index = 0
    count_per_video = 0
    
    while running:
        video_url = video_urls[current_index]
        
        # In thông tin tiến trình
        print(f"""
{luc}╔════════════════════════════════════════════╗
{luc}║            ĐANG CHẠY TĂNG FAVORITE         ║
{luc}╠════════════════════════════════════════════╣
{luc}║ Video hiện tại: {current_index + 1}/{len(video_urls)}                ║
{luc}║ Lần thứ: {count_per_video + 1}/10                         ║
{luc}║ Trạng thái: Đang xử lý...                   ║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚════════════════════════════════════════════╝""")
        
        try:
            driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div/div[8]/div/button').click()
            time.sleep(1)
            
            input_box = driver.find_element(By.XPATH, '/html/body/div[12]/div/form/div/input')
            input_box.send_keys(video_url)
            time.sleep(1)
            
            while count_per_video < 10 and running:
                try:
                    search_btn = driver.find_element(By.XPATH, '/html/body/div[12]/div/form/div/div/button')
                    search_btn.click()
                    time.sleep(1)
                    
                    submit_btn = driver.find_element(By.XPATH, '/html/body/div[12]/div/div/div[1]/div/form/button')
                    submit_btn.click()
                    
                    favorites_count += 90
                    count_per_video += 1
                    
                    # Cập nhật trạng thái
                    sys.stdout.write('\x1b[1A\x1b[2K' * 7)
                    print(f"""
{luc}╔════════════════════════════════════════════╗
{luc}║            ĐANG CHẠY TĂNG FAVORITE         ║
{luc}╠════════════════════════════════════════════╣
{luc}║ Video hiện tại: {current_index + 1}/{len(video_urls)}                ║
{luc}║ Lần thứ: {count_per_video}/10                         ║
{luc}║ Trạng thái: Tăng thành công ✓              ║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚════════════════════════════════════════════╝""")
                    time.sleep(3)
                    
                except:
                    sys.stdout.write('\x1b[1A\x1b[2K' * 7)
                    print(f"""
{luc}╔════════════════════════════════════════════╗
{luc}║            ĐANG CHẠY TĂNG FAVORITE         ║
{luc}╠════════════════════════════════════════════╣
{luc}║ Video hiện tại: {current_index + 1}/{len(video_urls)}                ║
{luc}║ Lần thứ: {count_per_video}/10                         ║
{luc}║ Trạng thái: Đang chờ cooldown...           ║
{luc}║ Đang x2 chạy nhanh                         ║
{luc}╚════════════════════════════════════════════╝""")
                    time.sleep(3)
            
            # Chuyển sang video tiếp theo
            if count_per_video >= 10:
                print(f"\n{luc}[*] Đã hoàn thành {count_per_video} lần cho video {current_index + 1}")
                count_per_video = 0
                current_index = (current_index + 1) % len(video_urls)
                print(f"{luc}[*] Chuyển sang video {current_index + 1}")
                time.sleep(2)
                
        except Exception as e:
            print(f"{do}[!] Lỗi khi xử lý video {current_index + 1}: {str(e)}")
            time.sleep(2)
            continue

def run_multi_comment_likes():
    """Chạy nhiều video comment like luân phiên"""
    global running
    
    print(f"\n{luc}[*] Vui lòng nhập danh sách link video:")
    video_urls = get_url_list()
    
    if not video_urls:
        print(f"{do}[!] Không có link video nào được nhập!")
        return
        
    if not openZefoy():
        return

    current_index = 0
    count_per_video = 0
    
    while running:
        video_url = video_urls[current_index]
        
        # In thông tin tiến trình
        print(f"""
{luc}╔════════════════════════════════════════════╗
{luc}║          ĐANG CHẠY TĂNG COMMENT LIKE       ║
{luc}╠════════════════════════════════════════════╣
{luc}║ Video hiện tại: {current_index + 1}/{len(video_urls)}                ║
{luc}║ Lần thứ: {count_per_video + 1}/10                         ║
{luc}║ Trạng thái: Đang xử lý...                   ║
{luc}╚════════════════════════════════════════════╝""")
        
        try:
            driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div/div[9]/div/button').click()
            time.sleep(1)
            
            input_box = driver.find_element(By.XPATH, '/html/body/div[13]/div/form/div/input')
            input_box.send_keys(video_url)
            time.sleep(1)
            
            while count_per_video < 10 and running:
                try:
                    search_btn = driver.find_element(By.XPATH, '/html/body/div[13]/div/form/div/div/button')
                    search_btn.click()
                    time.sleep(1)
                    
                    submit_btn = driver.find_element(By.XPATH, '/html/body/div[13]/div/div/div[1]/div/form/button')
                    submit_btn.click()
                    
                    comment_likes_count += 30
                    count_per_video += 1
                    
                    # Cập nhật trạng thái
                    sys.stdout.write('\x1b[1A\x1b[2K' * 7)
                    print(f"""
{luc}╔════════════════════════════════════════════╗
{luc}║          ĐANG CHẠY TĂNG COMMENT LIKE       ║
{luc}╠════════════════════════════════════════════╣
{luc}║ Video hiện tại: {current_index + 1}/{len(video_urls)}                ║
{luc}║ Lần thứ: {count_per_video}/10                         ║
{luc}║ Trạng thái: Tăng thành công ✓              ║
{luc}╚════════════════════════════════════════════╝""")
                    time.sleep(3)
                    
                except:
                    sys.stdout.write('\x1b[1A\x1b[2K' * 7)
                    print(f"""
{luc}╔════════════════════════════════════════════╗
{luc}║          ĐANG CHẠY TĂNG COMMENT LIKE       ║
{luc}╠════════════════════════════════════════════╣
{luc}║ Video hiện tại: {current_index + 1}/{len(video_urls)}                ║
{luc}║ Lần thứ: {count_per_video}/10                         ║
{luc}║ Trạng thái: Đang chờ cooldown...           ║
{luc}╚════════════════════════════════════════════╝""")
                    time.sleep(3)
            
            # Chuyển sang video tiếp theo
            if count_per_video >= 10:
                print(f"\n{luc}[*] Đã hoàn thành {count_per_video} lần cho video {current_index + 1}")
                count_per_video = 0
                current_index = (current_index + 1) % len(video_urls)
                print(f"{luc}[*] Chuyển sang video {current_index + 1}")
                time.sleep(2)
                
        except Exception as e:
            print(f"{do}[!] Lỗi khi xử lý video {current_index + 1}: {str(e)}")
            time.sleep(2)
            continue
def run_multi_videos(action_type):
    """Chạy nhiều video luân phiên, mỗi video 10 lần"""
    global running
    
    print(f"\n{luc}[*] Vui lòng nhập danh sách link video:")
    video_urls = get_url_list()
    
    if not video_urls:
        print(f"{do}[!] Không có link video nào được nhập!")
        return
        
    if not openZefoy():
        return

    current_index = 0
    count_per_video = 0
    
    while running:
        video_url = video_urls[current_index]
        
        # In thông tin video hiện tại
        print(f"\n{luc}╔════════════════════════════════════╗")
        print(f"{luc}║   Đang xử lý video {current_index + 1}/{len(video_urls)}   ")
        print(f"{luc}║   Lần thứ: {count_per_video + 1}/10        ")
        print(f"{luc}╚════════════════════════════════════╝")
        
        if action_type == "like":
            increase_likes(video_url)
        elif action_type == "view":
            increase_views(video_url)
            
        count_per_video += 1
        
        # Sau 10 lần thì chuyển video
        if count_per_video >= 10:
            print(f"\n{luc}[*] Đã hoàn thành 10 lần cho video {current_index + 1}")
            count_per_video = 0  # Reset bộ đếm
            current_index = (current_index + 1) % len(video_urls)  # Chuyển video theo vòng tròn
            print(f"{luc}[*] Chuyển sang video {current_index + 1}")
            time.sleep(2)

def get_usernames():
    """Lấy danh sách username TikTok từ người dùng"""
    usernames = []
    count = 1
    
    # Print header box
    print("""
\033[38;2;147;112;219m╔═════════════════════════════════════════════════════════╗\033[0m
\033[38;2;147;112;219m║\033[38;2;0;255;255m              NHẬP DANH SÁCH USERNAME                   \033[38;2;147;112;219m║\033[0m
\033[38;2;147;112;219m╠═════════════════════════════════════════════════════════╣\033[0m
\033[38;2;147;112;219m║\033[38;2;0;255;255m ▶ Nhập username TikTok (không cần @)                   \033[38;2;147;112;219m║\033[0m
\033[38;2;147;112;219m║\033[38;2;0;255;255m ▶ Nhấn Enter để bắt đầu sau khi nhập xong             \033[38;2;147;112;219m║\033[0m
\033[38;2;147;112;219m║\033[38;2;0;255;255m ▶ Thời gian: 2025-04-22 06:01:21                      \033[38;2;147;112;219m║\033[0m
\033[38;2;147;112;219m║\033[38;2;0;255;255m ▶ User: tiendev                                    \033[38;2;147;112;219m║\033[0m
\033[38;2;147;112;219m╚═════════════════════════════════════════════════════════╝\033[0m""")

    # Input loop
    while True:
        username = input(f"\033[38;2;255;182;193m[{count}] ⪼ \033[38;2;255;218;185mNhập username thứ {count}: \033[0m").strip()
        
        if username == "":
            if len(usernames) == 0:
                print("\033[38;2;255;20;147m[!] Vui lòng nhập ít nhất một username!\033[0m")
                continue
            break
            
        # Add username and increment counter
        usernames.append(username)
        count += 1
        
        # Print current list
        print(f"\033[38;2;147;112;219m╔════════════════ DANH SÁCH USERNAME ═══════════════╗\033[0m")
        for i, user in enumerate(usernames, 1):
            print(f"\033[38;2;147;112;219m║\033[38;2;0;255;255m [{i}] @{user:<45}\033[38;2;147;112;219m║\033[0m")
        print(f"\033[38;2;147;112;219m╚══════════════════════════════════════════════════╝\033[0m")
    
    # Print summary
    print(f"""
\033[38;2;147;112;219m╔═════════════════════════════════════════════════════════╗\033[0m
\033[38;2;147;112;219m║\033[38;2;0;255;255m                 THÔNG TIN TỔNG QUÁT                    \033[38;2;147;112;219m║\033[0m
\033[38;2;147;112;219m╠═════════════════════════════════════════════════════════╣\033[0m
\033[38;2;147;112;219m║\033[38;2;0;255;255m ▶ Tổng số username: {len(usernames):<34}\033[38;2;147;112;219m║\033[0m
\033[38;2;147;112;219m║\033[38;2;0;255;255m ▶ Thời gian bắt đầu: 2025-04-22 06:01:21              \033[38;2;147;112;219m║\033[0m
\033[38;2;147;112;219m╚═════════════════════════════════════════════════════════╝\033[0m""")
    
    return usernames      
def run_multi_profiles():
    """Chạy nhiều profile luân phiên"""
    global running
    
    print(f"\n{luc}[*] Vui lòng nhập danh sách username TikTok (không có @):")
    usernames = get_usernames()
    
    if not usernames:
        print(f"{do}[!] Không có username nào được nhập!")
        return

    print(f"""
{luc}╔═══════════════════════════════════════════════╗
{luc}║           BẮT ĐẦU TĂNG FOLLOW TỰ ĐỘNG         ║
{luc}╠═══════════════════════════════════════════════╣
{luc}║ Số lượng username: {len(usernames):<26}║
{luc}║ Trạng thái: Đang chạy...              ║
{luc}╚═══════════════════════════════════════════════╝""")

    with ThreadPoolExecutor(max_workers=len(usernames)) as executor:
        for username in usernames:
            executor.submit(increase_followers, username)

    print(f"""
{luc}╔═══════════════════════════════════════════════╗
{luc}║              KẾT THÚC TĂNG FOLLOW             ║
{luc}╠═══════════════════════════════════════════════╣
{luc}║ Tổng số follow đã tăng: {followers_count:<20}║
{luc}║ Trạng thái: Hoàn thành                       ║
{luc}╚═══════════════════════════════════════════════╝""")
    
    
    
    
def run_combined_features():
    """Chạy gộp các tính năng theo lựa chọn"""
    global running, followers_count, likes_count, views_count, shares_count, favorites_count, comment_likes_count
    current_user = "Tiendev"
    # Khởi tạo các biến đếm
    followers_count = 0
    likes_count = 0
    views_count = 0
    shares_count = 0
    favorites_count = 0
    comment_likes_count = 0
    print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║            CHỌN TÍNH NĂNG MUỐN CHẠY         ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ 1. 🚀 Tăng Follow                           ║
{luc}║ 2. 💖 Tăng Like (Server 1 & 2)              ║
{luc}║ 3. 👀 Tăng View                             ║
{luc}║ 4. 🔄 Tăng Share                            ║
{luc}║ 5. ⭐ Tăng Favorite                          ║
{luc}║ 6. 👍 Tăng Comment Like                     ║
{luc}║                                             ║
{luc}║ Cách chọn: Nhập số theo format (VD: 1+2+3) ║
{luc}╚═════════════════════════════════════════════╝""")

    choice = input(f"\n{luc}[?] Nhập lựa chọn của bạn: {trang}")
    selected_features = [x.strip() for x in choice.split("+") if x.strip() in ["1","2","3","4","5","6"]]
    
    if not selected_features:
        print(f"{do}[!] Không có lựa chọn hợp lệ!")
        return

    # Xử lý server cho tính năng like
    like_server = "0"
    if "2" in selected_features:
        print(f"\n{luc}{'='*20} SETUP LIKE {'='*20}")
        print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║              CHỌN SERVER TĂNG LIKE          ║
{luc}╠═════════════════════════════════════════════╣
{luc}║ [1] Server 1 - Ổn định (Cần Captcha)        ║
{luc}║ [2] Server 2 - Tốc độ nhanh (Không Captcha) ║
{luc}║ [=>] Nên chọn Server 1 để chạy Server 2 lúc ║
{luc}║      chạy được lúc không                    ║
{luc}╚═════════════════════════════════════════════╝""")
        while True:
            like_server = input(f"{luc}[?] Chọn server (1-2): {trang}")
            if like_server in ["1","2"]:
                break
            print(f"{do}[!] Lựa chọn không hợp lệ!")

    # Nhập thông tin cho từng tính năng
    video_url = None 
    username = None

    if "1" in selected_features:
        print(f"\n{luc}{'='*20} SETUP FOLLOW {'='*20}")
        username = input(f"{luc}[?] Nhập username TikTok (không cần @): {trang}")

    if any(x in selected_features for x in ["2","3","4","5","6"]):
        print(f"\n{luc}{'='*20} SETUP VIDEO {'='*20}")
        video_url = input(f"{luc}[?] Nhập link video: {trang}")

    # Setup Zefoy cho các tính năng cần thiết
    if like_server == "1" or any(x in selected_features for x in ["3","4","5","6"]):
        print(f"\n{luc}{'='*20} SETUP TOOL {'='*20}")
        if not openZefoy():
            return

    def print_running_stats():
        """In thống kê hiện tại"""
        clear_screen()
        print_banner()
        print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║               ĐANG CHẠY TOOL                ║
{luc}║          {current_time}              ║
{luc}╠═════════════════════════════════════════════╣""")
        if "1" in selected_features:
            print(f"{luc}║ Follow đã tăng: {followers_count:<28}║")
        if "2" in selected_features:
            print(f"{luc}║ Like đã tăng: {likes_count:<30}║")
        if "3" in selected_features:
            print(f"{luc}║ View đã tăng: {views_count:<30}║")
        if "4" in selected_features:
            print(f"{luc}║ Share đã tăng: {shares_count:<29}║")
        if "5" in selected_features:
            print(f"{luc}║ Favorite đã tăng: {favorites_count:<26}║")
        if "6" in selected_features:
            print(f"{luc}║ Comment Like đã tăng: {comment_likes_count:<22}║")
        print(f"{luc}║                                             ║")
        print(f"{luc}║ Admin: {current_user:<37}║")
        print(f"{luc}╚═════════════════════════════════════════════╝")

    # Bắt đầu chạy tool
    running = True
    print(f"\n{luc}[*] Hoàn tất setup, bắt đầu chạy tool...")
    time.sleep(2)
    print_running_stats()

    # Thêm biến đếm thời gian
    last_update = time.time()
    update_interval = 10  # Cập nhật mỗi 10 giây

    while running:
        try:
            for feature in selected_features:
                if not running:
                    break

                # Kiểm tra và cập nhật thống kê mỗi 10s
                current_time = time.time()
                if current_time - last_update >= update_interval:
                    print_running_stats()
                    last_update = current_time

                try:
                    if feature == "1":
                        increase_followers(username)
                        # Sau khi tăng thành công, cập nhật thống kê và chuyển feature
                        followers_count += 10
                        print_running_stats()
                        continue  # Chuyển sang feature tiếp theo

                    elif feature == "2":
                        if like_server == "1":
                            increase_likes(video_url)
                            likes_count += 20
                        else:
                            increase_likes_server2(video_url)
                            likes_count += 15
                        print_running_stats()
                        continue

                    elif feature == "3":
                        increase_views(video_url)
                        views_count += 1000
                        print_running_stats()
                        continue

                    elif feature == "4":
                        increase_shares(video_url)
                        shares_count += 150
                        print_running_stats()
                        continue

                    elif feature == "5":
                        increase_favorites(video_url)
                        favorites_count += 90
                        print_running_stats()
                        continue

                    elif feature == "6":
                        increase_comment_likes(video_url)
                        comment_likes_count += 30
                        print_running_stats()
                        continue

                except Exception as e:
                    # Nếu lỗi, chuyển sang feature tiếp theo
                    continue

        except KeyboardInterrupt:
            running = False
            break
        except Exception as e:
            # Lỗi chung, tiếp tục vòng lặp
            continue

    # In thống kê cuối cùng
    print(f"""
{luc}╔═════════════════════════════════════════════╗
{luc}║             KẾT THÚC CHẠY TOOL              ║
{luc}╠═════════════════════════════════════════════╣""")
    if "1" in selected_features:
        print(f"{luc}║ Tổng Follow: {followers_count:<30}║")
    if "2" in selected_features:
        print(f"{luc}║ Tổng Like: {likes_count:<32}║")
    if "3" in selected_features:
        print(f"{luc}║ Tổng View: {views_count:<32}║")
    if "4" in selected_features:
        print(f"{luc}║ Tổng Share: {shares_count:<31}║")
    if "5" in selected_features:
        print(f"{luc}║ Tổng Favorite: {favorites_count:<28}║")
    if "6" in selected_features:
        print(f"{luc}║ Tổng Comment Like: {comment_likes_count:<24}║")
    print(f"{luc}║                                             ║")
    print(f"{luc}║ Thời gian kết thúc: {current_time}    ║")
    print(f"{luc}║ Admin: {current_user:<37}║")
    print(f"{luc}╚═════════════════════════════════════════════╝")
def main():
    global running
    while True:
        try:
            clear_screen()
            print_banner()
            print_menu()
            
            choice = input(f"\n{luc}[?] Nhập lựa chọn: {trang}")
            
            if choice == "1":
                username = input(f"\n{luc}[?] Nhập username TikTok (không cần @): {trang}")
                running = True
                increase_followers(username)
                
            elif choice == "2":
                running = True
                run_multi_profiles()
                
            elif choice == "3":
                show_server_menu()
                server = input(f"\n{luc}[?] Chọn server (1-2): {trang}")
                video_url = input(f"\n{luc}[?] Nhập link video: {trang}")
                running = True
                
                if server == "1":
                    if not openZefoy():
                        continue
                    increase_likes(video_url)
                elif server == "2":
                    increase_likes_server2(video_url)
                else:
                    print(f"{do}[!] Lựa chọn server không hợp lệ!")
                    time.sleep(2)
            
            elif choice == "4":
                show_server_menu()
                server = input(f"\n{luc}[?] Chọn server (1-2): {trang}")
                running = True
                
                if server == "1":
                    run_multi_videos("like")
                elif server == "2":
                    print(f"\n{luc}[*] Vui lòng nhập danh sách link video:")
                    video_urls = get_url_list()
                    if not video_urls:
                        print(f"{do}[!] Không có link video nào được nhập!")
                        continue
                        
                    for video_url in video_urls:
                        increase_likes_server2(video_url)
                else:
                    print(f"{do}[!] Lựa chọn server không hợp lệ!")
                    time.sleep(2)
                
            elif choice == "5":
                if not openZefoy():
                    continue
                video_url = input(f"\n{luc}[?] Nhập link video: {trang}")
                running = True
                increase_views(video_url)
                
            elif choice == "6":
                running = True
                run_multi_videos("view")
                
            elif choice == "7":
                if not openZefoy():
                    continue
                video_url = input(f"\n{luc}[?] Nhập link video: {trang}")
                running = True
                increase_shares(video_url)
                
            elif choice == "8":
                running = True
                run_multi_shares()
                
            elif choice == "9":
                if not openZefoy():
                    continue
                video_url = input(f"\n{luc}[?] Nhập link video: {trang}")
                running = True
                increase_favorites(video_url)
                
            elif choice == "10":
                running = True
                run_multi_favorites()
                
            elif choice == "11":
                if not openZefoy():
                    continue
                video_url = input(f"\n{luc}[?] Nhập link video: {trang}")
                running = True
                increase_comment_likes(video_url)
                
            elif choice == "12":
                running = True
                run_multi_comment_likes()
                
            elif choice == "13":
                running = True
                run_combined_features()
                
            elif choice == "14":
                clear_screen()
                print_banner()
                show_info()
                input(f"\n{luc}[*] Nhấn Enter để tiếp tục...")

            elif choice == "15":
                clear_screen() 
                print_banner()
                show_guide()
                input(f"\n{luc}[*] Nhấn Enter để tiếp tục...")

            elif choice == "16":
                clear_screen()
                print_banner() 
                show_stats()
                input(f"\n{luc}[*] Nhấn Enter để tiếp tục...")

                
            elif choice == "0":
                clear_screen()
                print_banner()
                print(f"\n{luc}[*] Cảm ơn đã sử dụng tool!")
                print(f"{luc}[*] Developed by TienDev")
                time.sleep(2)
                break
                
            else:
                print(f"\n{do}[!] Lựa chọn không hợp lệ!")
                time.sleep(2)
                
        except KeyboardInterrupt:
            print(f"\n{do}[!] Đã dừng tool!")
            break
            
        except Exception as e:
            print(f"\n{do}[!] Lỗi không mong muốn: {str(e)}")
            time.sleep(2)
            
        finally:
            if driver:
                driver.quit()
            running = False
if __name__ == "__main__":
    
    try:
        
        main()
    except Exception as e:
        print(f"\n{do}[!] Lỗi không mong muốn: {str(e)}")
