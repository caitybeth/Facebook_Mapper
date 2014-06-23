from friender import *
from database import *

class crawler:
       def __init__(self,ident):
              self.dr=setup()
              self.config=getConfig()
              self.db=database(ident)
       def start(self):
              self.crawled={}
              target=self.config['seed']
              seed=getIDS([target])
              print '--'
              crawled={}
              seed=seed[0]
              tocrawl={seed[0]:seed[1]}
              for i in range(self.config['layers']):
                     total_for_layer=len(tocrawl)
                     new_crawl={}
                     for prof in tocrawl.keys():
                            print 'id=',prof
                            
                            if prof in self.db.available():
                                   data=self.db.get(prof)
                                   fr=data['friends']
                                   new_crawl.update(fr)
                                   total_for_layer-=1
                                   continue
                            
                            else:
                                   try:
                                          print '============================layer=',i,total_for_layer,'left'
                                          self.dr.get('https://www.facebook.com/profile.php?id='+prof+'&sk=friends')
                                          self.dr=scroll(self.dr)
                                          self.dr,fr=find_friends(self.dr)
                                   except Exception as e:
                                          print 'Exception encountered'
                                          print e
                                          fr=[]
                                          pass
                                   print 'getting_individual IDS'
                                   fr=getIDSserial(fr)
                                   print 'got IDS (',len(fr),')'
                                   print 'done'
                                   print '============================layer=',i,total_for_layer,'left'
                                   data={'id':prof,'name':tocrawl[prof],'friends':fr}
                                   self.db.add(data)
                                   self.db.save()
                                   new_crawl.update(fr)
                                   total_for_layer-=1
                     tocrawl=new_crawl
                     new_crawl={}
              self.dr.close()

if __name__=='__main__':
       c=crawler(0)
       print 'Crawler object created'
       print '              CRAWL_STARTING'
       c.start()
