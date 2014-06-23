from selenium import webdriver
import time
import os

user_id=''#Enter a user id
user_password=''#enter a user password
seedid=''#enter a seed id to start the gun




def login(emailid,password):#does the login with user and password provided and returns a driver object
    dr=webdriver.Firefox()
    dr.get('https://www.facebook.com')
    email=dr.find_element_by_id('email')
    email.send_keys(emailid)
    passwd=dr.find_element_by_id('pass')
    src=dr.page_source
    passwd.send_keys(password+'\n')
    while True:
        if dr.page_source!=src:
            break
    #login done
    return dr
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def msg(dr,message):#sends the message to the given page
    a_tag=dr.find_elements_by_tag_name('a')
    btn=[]
    for i in a_tag:
            lk=i.get_attribute('href')
            if lk!=None:
                      if '/messages/' in lk:
                                      btn.append(i)
    button=[]
    for i in btn:
            txt=i.text
            if txt=='Message':
                      button.append(i)
    btn=button[-1]
    src=dr.page_source
    btn.click()
    #message button clicked
    while True:
        if dr.page_source!=src:
            break
    for i in range(50):
        try:
            js5=dr.find_element_by_id('js_5')
        except:
            time.sleep(0.5)
        else:
            break
    txt=js5.find_element_by_tag_name('textarea')
    txt.send_keys(message)
    btn=dr.find_element_by_id('js_0')
    src=dr.page_source
    btn.click()
    time.sleep(1)
    return dr
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
dr=login(user_id,user_password)

files=os.listdir(os.path.join(os.getcwd(),'data'))
friends=[]
if seedid in files:
    import pickle
    f=file(os.path.join(os.getcwd(),'data',seedid),'r')
    data=pickle.load(f)
    f.close()
    for i in data['friends']:
        friends.append(i[0])
friends_of_friends=[]
for i in friends:
    if i in files:
        import pickle
        f=file(os.path.join(os.getcwd(),'data',i),'r')
        data=pickle.load(f)
        f.close()
        for i in data['friends']:
            friends_of_friends.append(i[0])
friends.extend(friends_of_friends)
print 'total messages to be sent ',len(friends)
done=[]


m=''
f=file('message.txt','r')
lines=f.readlines()
f.close()
for i in lines:
    m+=i

print m
        
for i in friends:
    try:
        dr.get('https://www.facebook.com/profile.php?id='+i)
        dr=msg(dr,m)
        print i,' done'
        done.append(i)
    except Exception as e:
        print e
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    

