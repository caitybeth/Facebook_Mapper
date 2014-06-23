import cPickle as pic
import time
import os


class index:       
       def __check__(self):
               path=os.getcwd()
               files=os.listdir(path)
               if 'index-'+self.identity in files:
                       return True
               return False
               
       def __init__(self,identity):
              self.identity=str(identity)
              self.hash_table={}
              if self.__check__():
                      self.load(self.identity)
       def add(self,ident,name):
              if ident not in self.hash_table.keys():
                     self.hash_table[ident]=name
       def delete(self,ident):
              if ident in self.hash_table.keys():
                     self.hash_table.pop(ident)
                
       def save(self):
              f=file('index-'+self.identity,'w')
              pic.dump(self.hash_table,f)
              f.close()
              
       def load(self,idno):
               try:
                       f=file('index-'+idno,'r')
                       self.hash_table=pic.load(f)
                       f.close()
               except:
                       print 'error'
               
class database:
       def __init__(self,identity):
              self.idex=index(identity)
       def __del__(self):
              self.idex.save()
       def __put__(self,data):
              here=os.getcwd()
              path=os.path.join(here,'data',data['id'])
              f=file(path,'w')
              pic.dump(data,f)
              f.close()
       def __get__(self,ident):
              here=os.getcwd()
              path=os.path.join(here,'data',ident)
              f=file(path,'r')
              data=pic.load(f)
              f.close()
              return data
       def save(self):
              self.idex.save()
       def add(self,data):
              self.__put__(data)
              self.idex.add(data['id'],data['name'])
       def delete(self,ident):
              self.idex.delete(ident)
       def get(self,ident):
              if ident in self.idex.hash_table.keys():
                     data=self.__get__(ident)
                     return data
              print ident,' not in database'
              return None
       def available(self):
              return self.idex.hash_table.keys()
              
