# 通过URL地址，文件名字，保存路径来下载文件
def down_file_by_url(url, save_name, save_path='./'):
    import os
    import urllib.error
    import urllib.request
    from urllib import error
    import time
    n = 10  # 定义重复多少次下载,超过n次下载不到就放弃

    def cbk(a, b, c):
        '''回调函数
        @a: 已经下载的数据块
        @b: 数据块的大小
        @c: 远程文件的大小
        '''
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print('%.1f%%' % per)

    if os.path.exists(save_path) == False:
        os.makedirs(save_path)

    save_file = os.path.join(save_path, save_name)

    if os.path.exists(save_file):
        # print('文件：', save_file, '已经存在')
        pass
    else:

        def auto_down(url, filename, i=0):
            while i > n:
                print('\n>>>重复%s次没有获取到HTML,放弃获取HTML' % n)
                break
            else:
                try:
                    # print(save_name, url, '准备下载')
                    urllib.request.urlretrieve(url, filename)
                    # urllib.request.urlretrieve(url, filename, cbk)
                    # print('文件：', save_file, '下载成功')
                    # time.sleep(1)
                    # print(save_name, '下载成功')
                except error.ContentTooShortError as e:
                    time.sleep(1)
                    print('Network conditions is not good.Reloading<<<<ContentTooShortError')
                    print(e)

                    i += 1
                    print('睡眠1秒,正在第次%s重新尝试下载' % i, url)
                    auto_down(url, filename, i)
                except error.URLError as e:
                    print('Network conditions is not good.Reloading<<<<URLError')
                    print(e)
                except error.HTTPError as e:
                    print('Network conditions is not good.Reloading<<<<HTTPError')
                    print(e)
                    time.sleep(1)

                    i += 1
                    print('睡眠1秒,正在第次%s重新尝试下载' % i, url)
                    auto_down(url, filename, i)
                except ConnectionResetError as e:
                    print('Network conditions is not good.Reloading<<<<ConnectionResetError')
                    print(e)
                    time.sleep(1)

                    i += 1
                    print('睡眠1秒,正在第次%s重新尝试下载' % i, url)
                    auto_down(url, filename, i)
                except ValueError as e:
                    print('unknown url type:', url)
                    print(e)

        auto_down(url=url, filename=save_file)


# 直接通过url来获取网页数据
def get_html(url):
    import urllib.request
    from bs4 import BeautifulSoup
    import linecache
    import random
    import time

    # print('\n*************正在获取', url, 'HTML')
    # time.sleep(1)
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    filename = "USER_AGENTS.txt"
    lines = len(open(filename).readlines())
    html = None
    n = 10  # 定义重复多少次抓取不到就放弃

    def get_html_core(url, i=0):
        while i > n:
            print('\n>>>重复%s次没有获取到HTML,放弃获取HTML' % n)
            break
        else:
            try:
                a = random.randint(0, lines)
                # print("There are %d lines in %s" % (lines, filename), a)
                headers = {
                    'User-Agent': linecache.getline('USER_AGENTS.txt', a).replace(',', '').replace('\n', '').replace(
                        '\"',
                        '\'')}

                req = urllib.request.Request(url=url, headers=headers)
                html = urllib.request.urlopen(req).read()
                html = BeautifulSoup(html, 'lxml')
                return html
            except:
                i += 1
                print('正在第次%s重新获取HTML' % i, url)
                html = get_html_core(url, i)

    html = get_html_core(url)

    return html