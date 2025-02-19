#!/usr/bin/python3

from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os
import threading
import signal
import copy
import time

import StudentsModel
signal.signal(signal.SIGINT, signal.SIG_DFL)

class UpdateStudentsInfo(QThread):

	def __init__(self,*args):

		QThread.__init__(self)

		self.listInfo=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):
		
		time.sleep(1)
		self.ret=Bridge.permissionMan.applyStudentsChanges(self.listInfo)

	#def run

#class UpdateStudentsInfo

class Bridge(QObject):

		
	def __init__(self,ticket=None):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		Bridge.permissionMan=self.core.permissionManager
		self._studentsModel=StudentsModel.StudentsModel()
		self._studentSettingsChanged=False
		self._showStudentSettingsMessage=[False,"","Ok"]
		self._showStudentChangesDialog=False
		
	#def __init__

	def getStudentsConfig(self):		

		self.studentsInfo=copy.deepcopy(Bridge.permissionMan.studentsInfo)
		self._updateStudentsModel()

	#def getStudentsConfig

	def _getStudentSettingsChanged(self):

		return self._studentSettingsChanged

	#def _getStudentSettingsChanged

	def _setStudentSettingsChanged(self,studentSettingsChanged):

		if self._studentSettingsChanged!=studentSettingsChanged:
			self._studentSettingsChanged=studentSettingsChanged
			self.on_studentSettingsChanged.emit()

	#def _setStudentSettingsChanged

	def _getShowStudentSettingsMessage(self):

		return self._showStudentSettingsMessage

	#def _getShowStudentSettingsMessage

	def _setShowStudentSettingsMessage(self,showStudentSettingsMessage):

		if self._showStudentSettingsMessage!=showStudentSettingsMessage:
			self._showStudentSettingsMessage=showStudentSettingsMessage
			self.on_showStudentSettingsMessage.emit()

	#def _setShowStudentSettingsMessage

	def _getShowStudentChangesDialog(self):

		return self._showStudentChangesDialog

	#def _getShowStudentChangesDialog	

	def _setShowStudentChangesDialog(self,showStudentChangesDialog):
		
		if self._showStudentChangesDialog!=showStudentChangesDialog:
			self._showStudentChangesDialog=showStudentChangesDialog		
			self.on_showStudentChangesDialog.emit()

	#def _setshowStudentChangesDialog
	
	def _getStudentsModel(self):
		
		return self._studentsModel

	#def _getStudentsModel

	def _updateStudentsModel(self):

		ret=self._studentsModel.clear()
		studentsEntries=Bridge.permissionMan.studentsData
		for item in studentsEntries:
			if item["permissionId"]!="":
				self._studentsModel.appendRow(item["permissionId"],item["isEnabled"],item["showResult"])
		
	#def _updateStudentsModel

	@Slot('QVariantList')
	def manageStudentsChecked(self,value):

		self.showStudentSettingsMessage=[False,"","Ok"]
		permissionId=value[0]
		isEnabled=value[1]

		if self.studentsInfo[permissionId]!=isEnabled:
			self.studentsInfo[permissionId]=isEnabled
			if self.studentsInfo!=Bridge.permissionMan.studentsInfo:
				self.studentSettingsChanged=True
			else:
				self.studentSettingsChanged=False
		
	#def manageStudentsChecked

	@Slot()
	def applyStudentsChanges(self):

		self.showStudentSettingsMessage=[False,"","Ok"]
		self.core.mainStack.closePopUp=False
		self.showStudentChangesDialog=False
		self.updateStudentsInfoT=UpdateStudentsInfo(self.studentsInfo)
		self.updateStudentsInfoT.start()
		self.updateStudentsInfoT.finished.connect(self._updateStudentsInfoRet)

	#def applyStudentChanges	

	def _updateStudentsInfoRet(self):

		if self.updateStudentsInfoT.ret[0]:
			self._updateStudentsConfig()
			self.showStudentSettingsMessage=[True,self.updateStudentsInfoT.ret[1],"Ok"]
			self.core.mainStack.closeGui=True
		else:
			self.showStudentSettingsMessage=[True,self.updateStudentsInfoT.ret[1],"Error"]
			self.core.mainStack.closeGui=False
			self.core.mainStack.moveToStack=""

		if self.core.mainStack.moveToStack!="":
			self.core.mainStack.currentOptionsStack=self.core.mainStack.moveToStack
			self.showStudentSettingsMessage=[False,"","Info"]
			self.core.mainStack.moveToStack=""

		self.studentSettingsChanged=False
		self.core.mainStack.closePopUp=True

	#def _applyUserChanges

	@Slot()
	def cancelStudentsChanges(self):

		self.showStudentSettingsMessage=[False,"","Ok"]
		self.core.mainStack.closePopUp=False
		self.showStudentChangesDialog=False
		self._cancelStudentsChanges()

	#def cancelStudentsChanges

	def _cancelStudentsChanges(self):

		self._updateStudentsConfig()
		self.studentSettingsChanged=False
		self.core.mainStack.closePopUp=True
		if self.core.mainStack.moveToStack!="":
			self.core.mainStack.currentOptionsStack=self.core.mainStack.moveToStack
		self.core.mainStack.moveToStack=""
		
		self.core.mainStack.closeGui=True

	#def _cancelStudentChanges

	def _updateStudentsConfig(self):

		self.studentsInfo=copy.deepcopy(Bridge.permissionMan.studentsInfo)
		self._updateStudentsModel()
	
	#def _updateUsersConfig

	on_studentSettingsChanged=Signal()
	studentSettingsChanged=Property(bool,_getStudentSettingsChanged,_setStudentSettingsChanged, notify=on_studentSettingsChanged)

	on_showStudentSettingsMessage=Signal()
	showStudentSettingsMessage=Property('QVariantList',_getShowStudentSettingsMessage,_setShowStudentSettingsMessage,notify=on_showStudentSettingsMessage)

	on_showStudentChangesDialog=Signal()
	showStudentChangesDialog=Property(bool,_getShowStudentChangesDialog,_setShowStudentChangesDialog, notify=on_showStudentChangesDialog)

	studentsModel=Property(QObject,_getStudentsModel,constant=True)

#class Bridge

import Core

