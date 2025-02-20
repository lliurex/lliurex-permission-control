#!/usr/bin/python3

from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os
import threading
import signal
import copy
import time
import sys

signal.signal(signal.SIGINT, signal.SIG_DFL)

class GatherInfo(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
	
	#def __init__
		
	def run(self,*args):
		
		time.sleep(1)
		self.manager=Bridge.permissionMan.loadConfig()

	#def run

#class GatherInfo

class Bridge(QObject):

	def __init__(self):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		Bridge.permissionMan=self.core.permissionManager
		self._closeGui=False
		self._closePopUp=True
		self._currentStack=0
		self._currentOptionsStack=0
		self._isAdminUser=Bridge.permissionMan.isAdminUser()
		self.moveToStack=""

	#def __init__

	def initBridge(self):

		self.gatherInfo=GatherInfo()
		self.gatherInfo.start()
		self.gatherInfo.finished.connect(self._loadConfig)

	#def initBridge

	def _loadConfig(self):		

		self.core.studentStack.getStudentsConfig()
		if self._isAdminUser:
			self.core.teacherStack.getTeachersConfig()
		self.currentStack=1

	#def _loadConfig

	def _getCurrentStack(self):

		return self._currentStack

	#def _getCurrentStack

	def _setCurrentStack(self,currentStack):

		if self._currentStack!=currentStack:
			self._currentStack=currentStack
			self.on_currentStack.emit()

	#def _setCurrentStack

	def _getCurrentOptionsStack(self):

		return self._currentOptionsStack

	#def _getCurrentOptionsStack

	def _setCurrentOptionsStack(self,currentOptionsStack):

		if self._currentOptionsStack!=currentOptionsStack:
			self._currentOptionsStack=currentOptionsStack
			self.on_currentOptionsStack.emit()

	#def _setCurrentOptionsStack

	def _getClosePopUp(self):

		return self._closePopUp

	#def _getClosePopUp

	def _setClosePopUp(self,closePopUp):
		
		if self._closePopUp!=closePopUp:
			self._closePopUp=closePopUp		
			self.on_closePopUp.emit()

	#def _setClosePopUp		

	def _getCloseGui(self):

		return self._closeGui

	#def _getCloseGui	

	def _setCloseGui(self,closeGui):
		
		if self._closeGui!=closeGui:
			self._closeGui=closeGui		
			self.on_closeGui.emit()

	#def _setCloseGui

	def _getIsAdminUser(self):

		return self._isAdminUser

	#def _getIsAdminUser

	@Slot(int)
	def manageTransitions(self,stack):

		if self.currentOptionsStack!=stack:
			self.moveToStack=stack
			if self.core.studentStack.studentSettingsChanged:
				self.core.studentStack.showStudentChangesDialog=True
			elif self.core.teacherStack.teacherSettingsChanged:
				self.core.teacherStack.showTeacherChangesDialog=True
			else:
				self.core.studentStack.manageStudentFeedBack()
				self.core.teacherStack.manageTeacherFeedBack()
				self.currentOptionsStack=stack
				self.moveToStack=""
	
	#def manageTransitions
	
	@Slot(str)
	def manageSettingsDialog(self,action):
		
		if action=="Apply":
			if self.core.studentStack.studentSettingsChanged:
				self.core.studentStack.applyStudentsChanges()
			elif self.core.teacherStack.teacherSettingsChanged:
				self.core.teacherStack.applyTeachersChanges()
		elif action=="Discard":
			if self.core.studentStack.studentSettingsChanged:
				self.core.studentStack.cancelStudentsChanges()
			elif self.core.teacherStack.teacherSettingsChanged:
				self.core.teacherStack.cancelTeachersChanges()
		elif action=="Cancel":
			self.closeGui=False
			if self.core.studentStack.studentSettingsChanged:
				self.core.studentStack.showStudentChangesDialog=False
			if self.core.teacherStack.teacherSettingsChanged:
				self.core.teacherStack.showTeacherChangesDialog=False
			self.moveToStack=""

	#def manageSettingsDialog
	
	@Slot()
	def openHelp(self):
		
		runPkexec=False
		
		if "PKEXEC_UID" in os.environ:
			runPkexec=True

		if 'valencia' in Bridge.permissionMan.sessionLang:
			self.helpCmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page='
		else:
			self.helpCmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page='
		
		if not runPkexec:
			self.helpCmd="su -c '%s' $USER"%self.helpCmd
		else:
			user=pwd.getpwuid(int(os.environ["PKEXEC_UID"])).pw_name
			self.helpCmd="su -c '%s' %s"%(self.helpCmd,user)

		self.openHelp_t=threading.Thread(target=self._openHelp)
		self.openHelp_t.daemon=True
		self.openHelp_t.start()

	#def openHelp

	def _openHelp(self):

		os.system(self.help_cmd)

	#def _openHelp

	@Slot()
	def closeApplication(self):

		self.closeGui=False
		if self.core.studentStack.studentSettingsChanged:
			self.core.studentStack.showStudentChangesDialog=True
		elif self.core.teacherStack.teacherSettingsChanged:
			self.core.teacherStack.showTeacherChangesDialog=True
		else:
			Bridge.permissionMan.removeLockToken()
			self.closeGui=True

	#def closeApplication
	
	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)
	
	on_currentOptionsStack=Signal()
	currentOptionsStack=Property(int,_getCurrentOptionsStack,_setCurrentOptionsStack, notify=on_currentOptionsStack)

	on_closePopUp=Signal()
	closePopUp=Property(bool,_getClosePopUp,_setClosePopUp, notify=on_closePopUp)

	on_closeGui=Signal()
	closeGui=Property(bool,_getCloseGui,_setCloseGui, notify=on_closeGui)

	isAdminUser=Property(bool,_getIsAdminUser,constant=True)

#class Bridge

import Core

