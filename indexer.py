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
               

              
