#!/usr/bin/python3

from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os
import threading
import signal
import copy
import time

import TeachersModel
signal.signal(signal.SIGINT, signal.SIG_DFL)

class UpdateTeachersInfo(QThread):

	def __init__(self,*args):

		QThread.__init__(self)

		self.listInfo=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):
		
		time.sleep(1)
		self.ret=Bridge.permissionMan.applyTeachersChanges(self.listInfo)

	#def run

#class UpdateTeachersInfo

class Bridge(QObject):

		
	def __init__(self,ticket=None):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		Bridge.permissionMan=self.core.permissionManager
		self._teachersModel=TeachersModel.TeachersModel()
		self._teacherSettingsChanged=False
		self._showTeacherSettingsMessage=[False,"","Ok"]
		self._showTeacherChangesDialog=False
		
	#def __init__

	def getTeachersConfig(self):		

		self.teachersInfo=copy.deepcopy(Bridge.permissionMan.teachersInfo)
		self._updateTeachersModel()

	#def getTeachersConfig

	def _getTeacherSettingsChanged(self):

		return self._teacherSettingsChanged

	#def _getTeacherSettingsChanged

	def _setTeacherSettingsChanged(self,teacherSettingsChanged):

		if self._teacherSettingsChanged!=teacherSettingsChanged:
			self._teacherSettingsChanged=teacherSettingsChanged
			self.on_teacherSettingsChanged.emit()

	#def _setTeacherSettingsChanged

	def _getShowTeacherSettingsMessage(self):

		return self._showTeacherSettingsMessage

	#def _getShowTeacherSettingsMessage

	def _setShowTeacherSettingsMessage(self,showTeacherSettingsMessage):

		if self._showTeacherSettingsMessage!=showTeacherSettingsMessage:
			self._showTeacherSettingsMessage=showTeacherSettingsMessage
			self.on_showTeacherSettingsMessage.emit()

	#def _setShowTeacherSettingsMessage

	def _getShowTeacherChangesDialog(self):

		return self._showTeacherChangesDialog

	#def _getShowTeacherChangesDialog	

	def _setShowTeacherChangesDialog(self,showTeacherChangesDialog):
		
		if self._showTeacherChangesDialog!=showTeacherChangesDialog:
			self._showTeacherChangesDialog=showTeacherChangesDialog		
			self.on_showTeacherChangesDialog.emit()

	#def _setshowTeacherChangesDialog
	
	def _getTeachersModel(self):
		
		return self._teachersModel

	#def _getTeachersModel

	def _updateTeachersModel(self):

		ret=self._teachersModel.clear()
		teachersEntries=Bridge.permissionMan.teachersData
		for item in teachersEntries:
			if item["permissionId"]!="":
				self._teachersModel.appendRow(item["permissionId"],item["isEnabled"],item["showResult"])
		
	#def _updateTeachersModel

	@Slot('QVariantList')
	def manageTeachersChecked(self,value):

		permissionId=value[0]
		isEnabled=value[1]

		if self.teachersInfo[permissionId]!=isEnabled:
			self.teachersInfo[permissionId]=isEnabled
			if self.teachersInfo!=Bridge.permissionMan.teachersInfo:
				self.teacherSettingsChanged=True
			else:
				self.teacherSettingsChanged=False
		
	#def manageTeachersChecked

	@Slot()
	def applyTeachersChanges(self):

		self.showTeacherChangesDialog=False
		self.core.mainStack.closePopUp=False
		self.manageTeacherFeedBack()
		self.updateTeachersInfoT=UpdateTeachersInfo(self.teachersInfo)
		self.updateTeachersInfoT.start()
		self.updateTeachersInfoT.finished.connect(self._updateTeachersInfoRet)

	#def applyTeachersChanges	

	def _updateTeachersInfoRet(self):

		self.teacherSettingsChanged=False
		self.getTeachersConfig()

		if self.updateTeachersInfoT.ret[0]:
			self.core.mainStack.closePopUp=True
			self.showTeacherSettingsMessage=[True,self.updateTeachersInfoT.ret[1],"Ok"]
			self.core.mainStack.closeGui=True
			if self.core.mainStack.moveToStack!="":
				self.manageTeacherFeedBack()
				self.core.mainStack.manageTransitions(self.core.mainStack.moveToStack)
		else:
			self.core.mainStack.closePopUp=True
			self.showTeacherSettingsMessage=[True,self.updateTeachersInfoT.ret[1],"Error"]
			self.core.mainStack.closeGui=False
			self.core.mainStack.moveToStack=""

	#def _applyUserChanges

	@Slot()
	def cancelTeachersChanges(self):

		self.core.mainStack.closePopUp=False
		self.showTeacherChangesDialog=False
		self.manageTeacherFeedBack()
		self._cancelTeachersChanges()

	#def cancelTeachersChanges

	def _cancelTeachersChanges(self):

		self.getTeachersConfig()
		self.teacherSettingsChanged=False
		self.core.mainStack.closePopUp=True
		if self.core.mainStack.moveToStack!="":
			self.core.mainStack.manageTransitions(self.core.mainStack.moveToStack)
		self.core.mainStack.moveToStack=""
		
		self.core.mainStack.closeGui=True

	#def _cancelTeachersChanges

	def _updateTeachersModelData(self):

		updateInfo=Bridge.permissionMan.teachersData
		if len(updateInfo)>0:
			for i in range(len(updateInfo)):
				index=self._teachersModel.index(i)
				self._teachersModel.setData(index,"showResult",-1)
	
	#def _updateTeachersModelData

	def manageTeacherFeedBack(self):

		Bridge.permissionMan.getTeachersConfig()
		self._updateTeachersModelData()
		self.showTeacherSettingsMessage=[False,"","Info"]

	#def manageStudentFeedBack

	on_teacherSettingsChanged=Signal()
	teacherSettingsChanged=Property(bool,_getTeacherSettingsChanged,_setTeacherSettingsChanged, notify=on_teacherSettingsChanged)

	on_showTeacherSettingsMessage=Signal()
	showTeacherSettingsMessage=Property('QVariantList',_getShowTeacherSettingsMessage,_setShowTeacherSettingsMessage,notify=on_showTeacherSettingsMessage)

	on_showTeacherChangesDialog=Signal()
	showTeacherChangesDialog=Property(bool,_getShowTeacherChangesDialog,_setShowTeacherChangesDialog, notify=on_showTeacherChangesDialog)

	teachersModel=Property(QObject,_getTeachersModel,constant=True)

#class Bridge

import Core

