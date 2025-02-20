#!/usr/bin/python3

import os
import subprocess
import sys
import shutil
import syslog
import pwd
import grp
import ast

class PermissionManager:

	APPLY_CHANGES_SUCCESSFUL=0
	APPLY_CHANGES_ERROR=-1

	def __init__(self):

		self.debug=False
		self.isLoadError=False
		self.lockTokenPath="/var/run/permissionControl.lock"
		self.studentsData=[]
		self.studentsInfo={}
		self.teachersData=[]
		self.teachersInfo={}
		self._createLockToken()
		self.getSessionLang()
		self.clearCache()
		self._getCurrentUser()

	#def __init__

	def _createLockToken(self):
		
		if not os.path.exists(self.lockTokenPath):
			f=open(self.lockTokenPath,'w')
			upPid=os.getpid()
			f.write(str(upPid))
			f.close()

	#def createLockToken

	def loadConfig(self):
		
		self.writeLog("Init session in lliurex-permission-control GUI")
		self.writeLog("User login in GUI: %s"%self.currentUser)
		self.writeLog("Initial configuration:")
		self._getInformationGroups()
		self.getStudentsConfig()
		self.getTeachersConfig()

	#def loadConfig

	def _getInformationGroups(self):

		self.studentsInfo={}
		self.teachersInfo={}
		tmpGroups=[]

		cmd="perm_control -l"
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		output=p.communicate()[0].decode()
		
		if ":" in output:
			try:
				tmpGroups=output.split(":")[1].strip()
				tmpGroups=ast.literal_eval(tmpGroups)
			
				for group in tmpGroups:
					try:
						cmd="perm_control -s %s"%group
						p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
						output=p.communicate()[0].decode().split("-")
						self.studentsInfo[group]=eval(output[0].split(":")[1].strip())
						self.teachersInfo[group]=eval(output[1].split(":")[1].strip())
					
					except Exception as e:
						self.writeLog("Get Information Groups. Group info error: %"%str(e))
						pass
			
			except Exception as e:
				self.writeLog("Get Information Groups. Groups list error: %s"%str(e))
				pass

	#def _getInformationGroups

	def getStudentsConfig(self):

		self.studentsData=[]

		for item in self.studentsInfo: 
			tmp={}
			tmp["permissionId"]=item
			tmp["isEnabled"]=self.studentsInfo[item]
			tmp["showResult"]=-1

			self.studentsData.append(tmp)

	#def _getDockerStatus

	def getTeachersConfig(self):

		self.teachersData=[]
		
		for item in self.teachersInfo: 
			tmp={}
			tmp["permissionId"]=item
			tmp["isEnabled"]=self.teachersInfo[item]
			tmp["showResult"]=-1

			self.teachersData.append(tmp)

	#def _getDockerStatus

	def applyStudentsChanges(self,newConfig):

		errorCount=0

		self.getStudentsConfig()
		
		for item in newConfig:
			if newConfig[item]!=self.studentsInfo[item]:
				if newConfig[item]:
					self.writeLog("- Action: enable %s permissions for alu"%item)
					cmd="perm_control -u alu -e %s"%item
				else:
					self.writeLog("- Action: disable %s permission for alu"%item)
					cmd="perm_control -u alu -d %s"%item

				p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
				poutput=p.communicate()[0]
				rc=p.returncode
				ret=poutput.decode()

				if rc==0:
					if 'enabled' in ret or 'disabled' in ret:
						self.writeLog("- Result: Change apply successfully")
						self.studentsInfo[item]=newConfig[item]
						self._updateStudentsData(item,0)
					elif 'unavailable':
						self.writeLog("- Result: group is unavailable")
				else:
					self.writeLog("- Result: Failed to apply change")
					errorCount+=1
					self._updateStudentsData(item,1)
	
		if errorCount==0:
			return [True,PermissionManager.APPLY_CHANGES_SUCCESSFUL]
		else:
			return [False,PermissionManager.APPLY_CHANGES_ERROR]

	#def applyStudentsChanges

	def _updateStudentsData(self,group,showResult=-1):

		for item in self.studentsData:
			if item["permissionId"]==group:
				item["isEnabled"]=self.studentsInfo[group]
				item["showResult"]=showResult

	#def _updateStudentsData

	def applyTeachersChanges(self,newConfig):

		errorCount=0

		self.getTeachersConfig()
		
		for item in newConfig:
			if newConfig[item]!=self.teachersInfo[item]:
				if newConfig[item]:
					self.writeLog("- Action: enable %s permissions for doc"%item)
					cmd="perm_control -u doc -e %s"%item
				else:
					self.writeLog("- Action: disable %s permission for doc"%item)
					cmd="perm_control -u doc -d %s"%item

				p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
				poutput=p.communicate()[0]
				rc=p.returncode
				ret=poutput.decode()

				if rc==0:
					if 'enabled' in ret or 'disabled' in ret:
						self.writeLog("- Result: Change apply successfully")
						self.teachersInfo[item]=newConfig[item]
						self._updateTeachersData(item,0)
					elif 'unavailable':
						self.writeLog("- Result: group is unavailable")
				else:
					self.writeLog("- Result: Failed to apply change")
					errorCount+=1
					self._updateTeachersData(item,1)
	
		if errorCount==0:
			return [True,PermissionManager.APPLY_CHANGES_SUCCESSFUL]
		else:
			return [False,PermissionManager.APPLY_CHANGES_ERROR]

	#def applyStudentsChanges

	def _updateTeachersData(self,group,showResult=-1):

		for item in self.teachersData:
			if item["permissionId"]==group:
				item["isEnabled"]=self.teachersInfo[group]
				item["showResult"]=showResult

	#def _updateStudentsData

	def getSessionLang(self):

		lang=os.environ["LANG"]
		
		if 'valencia' in lang:
			self.sessionLang="ca@valencia"
		else:
			self.sessionLang="es"

	#def getSessionLang

	def writeLog(self,msg):

		syslog.openlog("PERMISSION-CONTROL")
		syslog.syslog(msg)

	#def writeLog

	def clearCache(self):

		clear=False
		versionFile="/root/.lliurex-permission-control.conf"
		cachePath1="/root/.cache/lliurex-permission-control"
		installedVersion=self.getPackageVersion()

		if not os.path.exists(versionFile):
			with open(versionFile,'w') as fd:
				fd.write(installedVersion)

			clear=True

		else:
			with open(versionFile,'r') as fd:
				fileVersion=fd.readline()
				fd.close()

			if fileVersion!=installedVersion:
				with open(versionFile,'w') as fd:
					fd.write(installedVersion)
					fd.close()
				clear=True
		
		if clear:
			if os.path.exists(cachePath1):
				shutil.rmtree(cachePath1)

	#def clearCache

	def getPackageVersion(self):

		packageVersionFile="/var/lib/lliurex-permission-control/version"
		pkgVersion=""

		if os.path.exists(packageVersionFile):
			with open(packageVersionFile,'r') as fd:
				pkgVersion=fd.readline()
				fd.close()

		return pkgVersion

	#def getPackageVersion

	def _getCurrentUser(self):

		sudoUser=""
		loginUser=""
		pkexecUser=""

		try:
			sudoUser=(os.environ["SUDO_USER"])
		except:
			pass
		try:
			loginUser=os.getlogin()
		except:
			pass

		try:
			cmd="id -un $PKEXEC_UID"
			p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			pkexecUser=p.communicate()[0].decode().strip()
			print("USER:%s"%pkexecUser)
		except Exception as e:
			print("error")
			pass

		if pkexecUser!="root" and pkexecUser!="":
			self.currentUser=pkexecUser

		elif sudoUser!="root" and sudoUser!="":
			self.currentUser=sudoUser

	#def _getCurrentUser

	def removeLockToken(self):
		
		if os.path.exists(self.lockTokenPath):
			os.remove(self.lockTokenPath)

	#def removeLockToken

	def isAdminUser(self):
		
		isAdmin=False

		try:
			user=pwd.getpwuid(int(os.environ["PKEXEC_UID"])).pw_name
			gid = pwd.getpwnam(user).pw_gid
			groupsGids = os.getgrouplist(user, gid)
			userGroups = [ grp.getgrgid(x).gr_name for x in groupsGids ]

			if 'sudo' in userGroups or 'admins' in userGroups:
				isAdmin=True

		except Exception as e:
			isAdmin=True

		return isAdmin

	#def isAdminUser

#class PermissionManager
