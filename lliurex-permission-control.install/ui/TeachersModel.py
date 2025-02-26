#!/usr/bin/python3
import os
import sys
from PySide6 import QtCore, QtGui, QtQml

class TeachersModel(QtCore.QAbstractListModel):

	PermissionIdRole= QtCore.Qt.UserRole + 1000
	IsEnabledRole = QtCore.Qt.UserRole + 1001
	ShowResultRole= QtCore.Qt.UserRole + 1002


	def __init__(self,parent=None):
		
		super(TeachersModel, self).__init__(parent)
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
			if role == TeachersModel.PermissionIdRole:
				return item["permissionId"]
			elif role == TeachersModel.IsEnabledRole:
				return item["isEnabled"]
			elif role==TeachersModel.ShowResultRole:
				return item["showResult"]

	#def data

	def roleNames(self):
		
		roles = dict()
		roles[TeachersModel.PermissionIdRole] = b"permissionId"
		roles[TeachersModel.IsEnabledRole] = b"isEnabled"
		roles[TeachersModel.ShowResultRole] = b"showResult"

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
	
#class TeachersModel
