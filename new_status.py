#Python 3.7.3
#Make by Lonely_Dark

import time
import requests
import random

class tor:
	
	def method(self,method,params):
		params['access_token']=self.token
		params['v']='5.10l'
		self.result=requests.get('https://api.vk.com/method/{m}'.format(m=method),params=params).json()
		print(time.strftime('%H')+':'+time.strftime('%M')+'|[running]: Method: '+ str(method))
		return self.result
	
	def setToken(self,token):
		self.token=token


status=tor()
status.setToken('db1a2303e51c267cc86f7c96dc93f5e34ce5ab9b99f0157f70469eca1f59e05c27cce65df71b3cc2d957a')

while True:
	friends_online=status.method('friends.getOnline', {})
	friends_online=len(friends_online['response'])
	time.sleep(3)
	friends_all=status.method('friends.get', {})
	friends_all=friends_all['response']['count']
	time.sleep(3)
	friends_recent=status.method('friends.getRecent',{'count':1})
	friends_recent=friends_recent['response'][0]
	time.sleep(3)
	recent_info=status.method('users.get', {'user_ids': friends_recent})
	recent_name=recent_info['response'][0]['first_name']+' '+recent_info['response'][0]['last_name']
	offline_friends=int(friends_all)-int(friends_online)
	time.sleep(3)
	text='Friends online: '+str(friends_online)+','+'\n'+'Friends offline: '+str(offline_friends)+','+'\n'+'Last application from: '+str(recent_name)+','+'\n'+'Time now: '+time.strftime('%H')+':'+time.strftime('%M')
	status_finish=status.method('status.set',{'text': text})
