#!/usr/bin/env python3

import sys


import PermissionManager
import TeacherStack
import StudentStack
import MainStack

class Core:
	
	singleton=None
	DEBUG=False
	
	@classmethod
	def get_core(self):
		
		if Core.singleton==None:
			Core.singleton=Core()
			Core.singleton.init()

		return Core.singleton
		
	
	def __init__(self,args=None):

	
		self.dprint("Init...")
		
	#def __init__
	
	def init(self):

	
		self.permissionManager=PermissionManager.PermissionManager()
		self.teacherStack=TeacherStack.Bridge()
		self.studentStack=StudentStack.Bridge()
		self.mainStack=MainStack.Bridge()
		
		self.mainStack.initBridge()
	
		
	#def init

	def dprint(self,msg):
		
		if Core.DEBUG:
			
			print("[CORE] %s"%msg)
	
	#def  dprint
