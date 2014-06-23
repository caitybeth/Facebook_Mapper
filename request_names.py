import urllib
import urllib2
from collections import deque
import threadpool
import time


#========
site4='http://fbslave3-thesage2.rhcloud.com/query'
site5='http://fbslave4-thesage2.rhcloud.com/query'
site6='http://fbslave5-thesage2.rhcloud.com/query'
#========
site7='http://fbslave6-thesage3.rhcloud.com/query'
site8='http://fbslave7-thesage3.rhcloud.com/query'
site9='http://fbslave8-thesage3.rhcloud.com/query'
#========
site10='http://fbslave9-thesage4.rhcloud.com/query'
site11='http://fbslave10-thesage4.rhcloud.com/query'
site12='http://fbslave11-thesage4.rhcloud.com/query'
#========
site13='http://fbslave12-thesage5.rhcloud.com/query'
site14='http://fbslave13-thesage5.rhcloud.com/query'
site15='http://fbslave14-thesage5.rhcloud.com/query'
#========
site16='http://fbslave15-thesage6.rhcloud.com/query'
site17='http://fbslave16-thesage6.rhcloud.com/query'
site18='http://fbslave17-thesage6.rhcloud.com/query'
#========
site19='http://fbslave18-thesage7.rhcloud.com/query'
site20='http://fbslave19-thesage7.rhcloud.com/query'
site21='http://fbslave20-thesage7.rhcloud.com/query'
#========
slaves=[site4,site5,site6,site7,site8,site9,site10,site11,site12,site13,site14,site15,site16,site17,site18,site19,site20,site21]

q=deque(slaves)
result=deque()




def getname(name):
       global q,result
       while True:
              try:
                     url=q.pop()
                     break
              except:
                     time.sleep(0.1)
                     pass
       query='name='+name
       for try_count in range(4):
              try:
                     s=time.time()
                     r=urllib2.urlopen(url+'?'+query)
                     r=r.read()
                     r=eval(r)
                     t=time.time()-s
                     if t<1:
                            time.sleep(1-t)
                     result.append((r['id'],r['name']))
                     q.append(url)
                     print '.',
                     break
              except Exception as error:
                     time.sleep(1)
                     if try_count>=2:
                            print error,
                            q.append(url)
                            break

def getIDSserial(names):
       global result
       args=names
       pool=threadpool.ThreadPool(len(slaves))
       requests=threadpool.makeRequests(getname,args)
       r=[pool.putRequest(req) for req in requests]
       print 'waiting...'
       pool.wait()
       pool.dismissWorkers(pool.workers)
       r=list(result)
       result=deque()
       return r

if __name__=='__main__':
       import os
       names=os.listdir(os.path.join(os.getcwd(),'data'))
       print len(names)
       s=time.time()
       res=getIDSserial(names)
       e=time.time()
       print len(res)
       print e-s
       for i in res:
              print i
       
