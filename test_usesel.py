from usesel import usesel

usal = usesel()
pixiv_url = "https://www.pixiv.net/"

driver = usal.call_driver()

driver.get(pixiv_url)
path = r"/html/body/div[3]/div[3]/div[2]/a[2]"
item = usal.get_elem(driver=driver,key=path,actions=["click"])
item[0].click()

waiting = input("")
driver.quit()
