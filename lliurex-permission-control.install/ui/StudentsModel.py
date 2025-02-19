#!/usr/bin/python3
import os
import sys
from PySide2 import QtCore, QtGui, QtQml

class StudentsModel(QtCore.QAbstractListModel):

	PermissionIdRole= QtCore.Qt.UserRole + 1000
	IsEnabledRole = QtCore.Qt.UserRole + 1001
	ShowResultRole= QtCore.Qt.UserRole + 1002


	def __init__(self,parent=None):
		
		super(StudentsModel, self).__init__(parent)
		self._entries =[]
	
	#def __init__

	def rowCount(self, parent=QtCore.QModelIndex()):
		
		if parent.isValid():
			return 0
		return len(self._entries)

	#def rowCount

	def data(self, index, role=QtCore.Qt.DisplayRole):
		
		if 0 <= index.row() < self.rowCount() and index.isValid():
			item = self._entries[index.row()]
			if role == StudentsModel.PermissionIdRole:
				return item["permissionId"]
			elif role == StudentsModel.IsEnabledRole:
				return item["isEnabled"]
			elif role==StudentsModel.ShowResultRole:
				return item["showResult"]

	#def data

	def roleNames(self):
		
		roles = dict()
		roles[StudentsModel.PermissionIdRole] = b"permissionId"
		roles[StudentsModel.IsEnabledRole] = b"isEnabled"
		roles[StudentsModel.ShowResultRole] = b"showResult"

		return roles

	#def roleName

	def appendRow(self,pi,ie,sr):
		
		tmpId=[]
		for item in self._entries:
			tmpId.append(item["permissionId"])
		tmpPI=pi.strip()
		if pi not in tmpId and pi !="" and len(tmpPI)>0:
			self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(),self.rowCount())
			self._entries.append(dict(permissionId=pi, isEnabled=ie,showResult=sr))
			self.endInsertRows()

	#def appendRow

	def setData(self, index, param, value, role=QtCore.Qt.EditRole):
		
		if role == QtCore.Qt.EditRole:
			row = index.row()
			if param in ["isEnabled","showResult"]:
				self._entries[row][param]=value
				self.dataChanged.emit(index,index)
				return True
			else:
				return False
	
	#def setData

	def clear(self):
		
		count=self.rowCount()
		self.beginRemoveRows(QtCore.QModelIndex(), 0, count)
		self._entries.clear()
		self.endRemoveRows()
	
	#def clear
	
#class StudentsModel
