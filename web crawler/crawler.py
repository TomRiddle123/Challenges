__author__ = 'TomRiddle'
import requests, httplib, os
from bs4 import BeautifulSoup

save_files = False  # does the user want to save the files instead of saveing just the links
main_site = ""  # the main site of the crawl
only_https = False  # does the user want the crawler to crawl only to sites that support https

# recursive crawl
def crawl(url, depth):
    global save_files, main_site, only_https


    if only_https and url.startswith("https"):

        try:
            page = requests.get(url, timeout=1.3)  # get the page
        except:
            return

        soup = BeautifulSoup(page.text, "lxml")  # soup of the page

        imgs_links = get_all_images_soup(soup)  # all the images links in the soup
        scrpts_links = get_all_scripts_soup(soup)  # all the scripts links in the soup

        if save_files:  # if you want to save the files:
            scripts_links_to_files(scrpts_links)
            imgs_links_to_files(imgs_links)

        else:  # if you want to save just the links to the images and the scripts
            _dir = os.getcwd() + "\\" + main_site.split(".")[0].split("/")[-1]
            if not (os.path.isdir(_dir)):
                os.mkdir(_dir)

            with open(_dir + "\logged_links.txt", "a+") as f2w:
                f2w.write(url + "\n\nimages:\n")
                for lnk in imgs_links:
                    try:
                        f2w.write(lnk+"\n")
                    except:
                        pass

                f2w.write("\nscripts:\n")

                for lnk in scrpts_links:
                    try:
                        f2w.write(lnk+"\n")
                    except:
                        pass

        for link in soup.find_all("a"):  # find all the links in the webpage that lead to a site and crawl to them

            title = link.text.strip()

            lnk = link.get("href")
            if lnk and "http" in lnk:
                if lnk and lnk.startswith("/"):
                    lnk = main_site + lnk

                if depth != 0:
                    print "crawling to " + lnk + " with depth " + str(depth - 1)
                    crawl(lnk, depth - 1)


def get_all_images_soup(soup):
    """
        a function that gets all the images links in a soup of a webpage
    """
    global main_site
    images_links = []

    for image in soup.find_all("img"):
        source = image.get("src")
        if source:
            if source.startswith("/"):
                source = main_site+source

            images_links.append(source)

    return images_links

def get_all_scripts_soup(soup):
    """
        a function that gets all the links for scripts in a soup of a webpage.
    """
    global main_site
    scripts_links = []

    for script in soup.find_all("script"):
        source = script.get("src")
        if source and source.endswith("js"):
            if source.startswith("/"):
                source = "https://ynet.co.il"+source

            scripts_links.append(source)

    return scripts_links


def imgs_links_to_files(links):
    """
        a function that gets the images behind the links into the images folder
    """
    global main_site
    _dir = os.getcwd() + "\\" + main_site.split(".")[0].split("/")[-1] + "\images"  # the directory
    if not (os.path.isdir(_dir)):  # if the directory doesn't exist create it.
        os.mkdir(_dir)

    for link in links:
        page = requests.get(link)
        with open(_dir + "\\" + link.split("/")[-1], "wb+") as f_2_w:
            for chunk in page:
                f_2_w.write(chunk)



def scripts_links_to_files(links):
    """
        a function that gets the files behind the links into the scripts folder
    """
    global main_site
    _dir = os.getcwd() + "\\" + main_site.split(".")[0].split("/")[-1] + "\scripts"  # the directory
    if not (os.path.isdir(_dir)):  # if the directory doesn't exist create it.
        os.mkdir(_dir)

    for link in links:
        page = requests.get(link)
        with open(_dir + "\\" + link.split("/")[-1], "w+") as f_2_w:
            f_2_w.write(page.content)



def main():
    global save_files, main_site, only_https

    print "hello and welcome to our web crawler!\n" \
          "through this software you will be able to search for certain stuff in your url and in the linked pages.\n\n"\
          "Before we start, several questions to fit the program for you:"

    answer = raw_input("1. By default, we save the links for the pages, scripts and images, would you like to save the "
                       "actual files in a directory? it will take much more time and space. (yes/no)\n")

    if answer == "yes":
        save_files = True

    answer = raw_input("\n2. would you like the crawler to crawl only to websites that support https?(yes/no)\n")
    if answer == "yes":
        only_https = True


    start_url = raw_input("\n3. What is the url you want us to start 'digging' from? (enter the full url)\n")
    main_site = "/".join(start_url.split("/")[0:3])
    try:
        requests.get(start_url)
    except:
        print "not a valid url!"
        exit()

    depth_str = raw_input("\n4. What is the depth of the crawl you want? (enter numeric value)\nFor instance, if you "
                          "will type 2, we will sort through the starting url, the linked pages in that url and the "
                          "linked pages in the linked pages.\n")
    depth = 0
    try:
        depth = int(depth_str)
    except:
        print "numeric value only!"
        exit()

    crawl(start_url, depth)



if __name__ == "__main__":
    main()