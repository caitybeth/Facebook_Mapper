from crawler import *
import os
import time
def facebook_crawl():
       for i in range(20):
              try:
                     c=crawler(0)
                     print 'Crawler object created'
                     print '              CRAWL_STARTING'
                     c.start()
              except Exception as e:
                     print e
                     try:
                            del c
                     except:
                            pass
                     time.sleep(20)
if __name__=='__main__':
       facebook_crawl()
