#!/usr/bin/python3

from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os
import threading
import signal
import copy
import time
import pwd
import PermissionManager

signal.signal(signal.SIGINT, signal.SIG_DFL)

class GatherInfo(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
	
	#def __init__
	
	def run(self,*args):
		
		time.sleep(1)
		LliurexPermissionControl.permissionMan.loadConfig()

	#def run

#class GatherInfo

class SetChanges(QThread):

	def __init__(self,*args):

		QThread.__init__(self)

		self.newValue=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):
		
		self.ret=LliurexPermissionControl.permissionMan.applyChanges(self.newValue)

	#def run

#class SetChanges

class LliurexPermissionControl(QObject):

	permissionMan=PermissionManager.PermissionManager()

	def __init__(self):

		QObject.__init__(self)
		self.initBridge()

	#def __init__

	def initBridge(self):

		self._isDockerEnabled=False
		self.isLoadError=False
		self._settingsChanged=False
		self._showSettingsMessage=[False,"","Ok"]
		self._closeGui=False
		self._closePopUp=True
		self._showChangesDialog=False
		self._currentStack=0
		self._currentOptionsStack=0
		self.gatherInfo=GatherInfo()
		self.gatherInfo.start()
		self.gatherInfo.finished.connect(self._loadConfig)

	#def initBridge

	def _loadConfig(self):		

		self.isDockerEnabled=LliurexPermissionControl.permissionMan.isDockerEnabled
		self.isLoadError=LliurexPermissionControl.permissionMan.isLoadError
		self.initialConfig=copy.deepcopy(LliurexPermissionControl.permissionMan.currentConfig)
		self.currentStack=1
		if self.isLoadError:
			self.showSettingsMessage=[True,LliurexPermissionControl.permissionMan.GET_STATUS_ERROR,"Error"]
		
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

	def _getIsDockerEnabled(self):

		return self._isDockerEnabled

	#def _getIsDockerEnabled

	def _setIsDockerEnabled(self,isDockerEnabled):

		if self._isDockerEnabled!=isDockerEnabled:
			self._isDockerEnabled=isDockerEnabled
			self.on_isDockerEnabled.emit()

	#def _setIsDockerEnabled

	def _getSettingsChanged(self):

		return self._settingsChanged

	#def _getSettingsChanged

	def _setSettingsChanged(self,settingsChanged):

		if self._settingsChanged!=settingsChanged:
			self._settingsChanged=settingsChanged
			self.on_settingsChanged.emit()

	#def _setSettingsChanged

	def _getShowSettingsMessage(self):

		return self._showSettingsMessage

	#def _getShowSettingsMessage

	def _setShowSettingsMessage(self,showSettingsMessage):

		if self._showSettingsMessage!=showSettingsMessage:
			self._showSettingsMessage=showSettingsMessage
			self.on_showSettingsMessage.emit()

	#def _setShowSettingsMessage

	def _getShowChangesDialog(self):

		return self._showChangesDialog

	#def _getShowChangesDialog

	def _setShowChangesDialog(self,showChangesDialog):

		if self._showChangesDialog!=showChangesDialog:
			self._showChangesDialog=showChangesDialog
			self.on_showChangesDialog.emit()

	#def _setShowChangesDialog

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

	@Slot(bool)
	def manageDockerChanges(self,value):

		self.showSettingsMessage=[False,"","Ok"]
		
		if value!=self.initialConfig[0]:
			self.isDockerEnabled=value
			self.initialConfig[0]=value
			if self.initialConfig!=LliurexPermissionControl.permissionMan.currentConfig:
				self.settingsChanged=True
			else:
				self.settingsChanged=False
					
	#def manageDockerChanges

	@Slot()
	def applyChanges(self):

		self.showSettingsMessage=[False,"","Ok"]
		self.closePopUp=False
		self.showChangesDialog=False
		self.setChangesT=SetChanges(self.initialConfig)
		self.setChangesT.start()
		self.setChangesT.finished.connect(self._applyChanges)

	#def applyChanges	

	def _applyChanges(self):

		if not self.setChangesT.ret[0]:
			self.showSettingsMessage=[True,self.setChangesT.ret[1],"Ok"]
			self.closeGui=True
		else:
			self.showSettingsMessage=[True,self.setChangesT.ret[1],"Error"]
			self.closeGui=False

		self.initialConfig=copy.deepcopy(LliurexPermissionControl.permissionMan.currentConfig)
		self.isDockerEnabled=self.initialConfig[0]
		self.settingsChanged=False
		self.closePopUp=True

	#def _applyChanges

	@Slot()
	def cancelChanges(self):

		self.showSettingsMessage=[False,"","Ok"]
		self.closePopUp=False
		self.closeGui=False
		self.showChangesDialog=False
		self._cancelChanges()

	#def cancelGroupChanges

	def _cancelChanges(self):

		self.initialConfig=copy.deepcopy(LliurexPermissionControl.permissionMan.currentConfig)
		self.isDockerEnabled=self.initialConfig[0]
		self.settingsChanged=False
		self.closePopUp=True
		self.closeGui=True

	#def _cancelGroupChanges

	@Slot(str)
	def manageSettingsDialog(self,action):
		
		if action=="Accept":
			self.applyChanges()
		elif action=="Discard":
			self.cancelChanges()
		elif action=="Cancel":
			self.closeGui=False
			self.showChangesDialog=False

	#def manageSettingsDialog

	@Slot(int)
	def manageTransitions(self,stack):

		if self.currentOptionsStack!=stack:
			self.currentOptionsStack=stack

	#def manageTransitions
	
	@Slot()
	def openHelp(self):
		
		runPkexec=False
		
		if "PKEXEC_UID" in os.environ:
			runPkexec=True

		if 'valencia' in LliurexPermissionControl.permissionMan.sessionLang:
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

		os.system(self.helpCmd)

	#def _openHelp

	@Slot()
	def closeApplication(self):

		self.closeGui=False
		if self.settingsChanged:
			self.showChangesDialog=True
		else:
			self.closeGui=True
			LliurexPermissionControl.permissionMan.removeLockToken()
			LliurexPermissionControl.permissionMan.writeLog("Close Session")

	#def closeApplication
	
	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)
	
	on_currentOptionsStack=Signal()
	currentOptionsStack=Property(int,_getCurrentOptionsStack,_setCurrentOptionsStack, notify=on_currentOptionsStack)

	on_isDockerEnabled=Signal()
	isDockerEnabled=Property(bool,_getIsDockerEnabled,_setIsDockerEnabled,notify=on_isDockerEnabled)

	on_settingsChanged=Signal()
	settingsChanged=Property(bool,_getSettingsChanged,_setSettingsChanged, notify=on_settingsChanged)

	on_showSettingsMessage=Signal()
	showSettingsMessage=Property('QVariantList',_getShowSettingsMessage,_setShowSettingsMessage,notify=on_showSettingsMessage)

	on_closePopUp=Signal()
	closePopUp=Property(bool,_getClosePopUp,_setClosePopUp, notify=on_closePopUp)

	on_closeGui=Signal()
	closeGui=Property(bool,_getCloseGui,_setCloseGui, notify=on_closeGui)

	on_showChangesDialog=Signal()
	showChangesDialog=Property(bool,_getShowChangesDialog,_setShowChangesDialog, notify=on_showChangesDialog)

#class LliurexPermissionControl

