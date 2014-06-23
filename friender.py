from selenium import webdriver
import time
from random import random
import urllib2
import threadpool as tp
import random
import request_names as graph



def getConfig():
       """
       read from file and get info
       """
       f=file('config.txt','r')
       name,passwd,seed,layers=f.readlines()
       f.close()
       name=name.replace('\n','')
       passwd=passwd.replace('\n','')
       seed=seed.replace('\n','')
       layers=eval(layers)
       d={'name':name,'password':passwd,'seed':seed,'layers':layers}
       print d
       return d



def setup():
       print 'Setting up crawler'
       dr=webdriver.Firefox()
       dr.get('https://www.facebook.com')
       frm=dr.find_element_by_id('login_form')

       config=getConfig()
       
       login=frm.find_element_by_id('email')
       login.send_keys(config['name'])
       pwd=frm.find_element_by_id('pass')
       pwd.send_keys(config['password'])
       frm.submit()
       dr.get('https://www.facebook.com/')
       print 'completetd'
       return dr
                     
def scroll(dr):
       el=dr.find_element_by_id('pageFooter')
       footer=el.location
       prev=dr.page_source
       timer=0
       print 'scrolling_to_end_of_page_with_ajax_elements'
       print '.',
       while True:
           dr.execute_script("window.scrollTo(0, "+str(footer['y'])+")")
           print '.',
           dr.execute_script("window.scrollTo(0, "+str(footer['y'])+")")
           dr.execute_script("window.scrollTo(0, "+str(footer['y'])+")")
           dr.execute_script("window.scrollTo(0, "+str(footer['y'])+")")
           footer=el.location
           new=dr.page_source
           if new==prev:
               timer+=1
               if timer>50:#determines wait time for scroll
                   break
           if new!=prev:
               if timer>0:
                   #print timer
                   timer=0
           prev=new
       print '|'
       print 'scrolling done'
       return dr

def find_friends(dr):
       print 'looking for friends',
       el=dr.find_element_by_id('pagelet_timeline_medley_friends')
       print '.',
       lis=el.find_elements_by_tag_name('ul')
       
       print '.',
       gen=(i for i in lis if 'uiList _262m' in i.get_attribute('class'))#generator
       lists=list(gen)#generate list

       #this took too much memory and time
       #for i in lists:
               #if 'uiList _262m' in i.get_attribute('class'):
                       #l.append(i)
       print '.',

       links=[]
       listsgen=(ul for ul in lists)
       print '.',
       for ul in listsgen:
              
               li=ul.find_elements_by_tag_name('li')
               ligen=(link for link in li)
               for link in ligen:
                       a=link.find_elements_by_tag_name('a')
                       agen=(tag for tag in a)
                       for tag in agen:
                               href=tag.get_attribute('href')
                               if 'https://www.facebook.com' and 'friends' in href:
                                       name=href[25:href.find('?',25)]
                                       links.append(str(name))
                                       print '.',
                               if 'https://www.facebook.com' and 'id=' in href:
                                       name=href[40:href.find('&',40)]
                                       #print name
                                       try:
                                              links.append(str(eval(name)))
                                       except:
                                              pass
                                       
       print '|'              
       links=list(set(links))
       lk=[]
       for i in links:
               if '/' not in i:
                       lk.append(i)
       print 'friends found(',len(lk),')'
       return dr,lk


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#get IDS using threadpool class

def getIDS(names):
       cnt=[]
       poolsize=60
       def f(name):
              for i in [1,2]:
                     try:
                            us_set=['Mozilla','IE','Opera','Chrome','Magic','theSage','Iceweasel','Rockmelt']
                            ua=random.choice(us_set)
                            req=urllib2.Request('http://graph.facebook.com/'+name+'?fields=id,name',headers={'User-Agent':ua})
                            r=urllib2.urlopen(req)
                            r=r.read()
                            r=eval(r)
                            result.append((r['id'],r['name']))
                            cnt.append(True)
                            if len(names)>550:
                                   time.sleep(60)# to prevent blocking of ip address by limiting rate
                     except Exception as e:
                            print e.reason,len(cnt)
                            if 'Nont Found' in e.reason:
                                   if len(names)>550:
                                          time.sleep(60)# to prevent blocking of ip address by limiting rate
                                   break
                            if 'Forbidden' in e.reason:
                                   time.sleep(600)
                            if len(names)>550:
                                   time.sleep(60)# to prevent blocking of ip address by limiting rate
                            pass
       result=[]
       pool=tp.ThreadPool(poolsize)
       requests=tp.makeRequests(f,names)
       r=[pool.putRequest(req) for req in requests]
       pool.wait()
       pool.dismissWorkers(poolsize)
       return result

#++++++++++++++++++++++++++++++++++++++++++++++++
'''
def getIDSserial(names):
       result=[]
       name_len=len(names)
       def f(name):
                     try:
                            s=time.time()
                            us_set=['Mozilla','IE','Opera','Chrome','Magic','theSage','Iceweasel','Rockmelt']
                            ua=random.choice(us_set)
                            req=urllib2.Request('http://graph.facebook.com/'+name+'?fields=id,name',headers={'User-Agent':ua})
                            r=urllib2.urlopen(req)
                            r=r.read()
                            r=eval(r)
                            result.append((r['id'],r['name']))
                            print name_len-len(result),r['name']
                            dt=time.time()-s
                            if dt<1:
                                   time.sleep(1-dt)
                     except Exception as e:
                            try:
                                   print e.reason
                                   if 'Forbidden' in e.reason:
                                          time.sleep(600)
                            except:
                                   pass
       for n in names:
              f(n)
       return result
'''
def getIDSserial(names):
       result=graph.getIDSserial(names)
       return result

