#!/usr/bin/python3

import os
import subprocess
import sys
import shutil
import syslog

class PermissionManager:

	APPLY_CHANGES_SUCCESSFUL=0
	APPLY_CHANGES_ENABLE_DOCKER_ERROR=-1
	APPLY_CHANGES_DISABLE_DOCKER_ERROR=-2

	def __init__(self):

		self.debug=False
		self.isDockerEnabled=False
		self.lockTokenPath="/var/run/permissionControl.lock"
		self.currentConfig=[self.isDockerEnabled]
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
		self._getDockerStatus()
		self.writeLog("Initial configuration:")
		self.writeLog("- docker enabled: %s"%str(self.isDockerEnabled))

	#def loadConfig

	def _getDockerStatus(self):

		cmd="perm-control -s"
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()
		rc=p.returncode
		
		if rc==0:
			self.isDockerEnabled=True
		else:
			self.isDockerEnabled=False
		
		self.currentConfig[0]=self.isDockerEnabled

	#def _getDockerStatus

	def applyChanges(self,value):

		dockerError=False

		if value[0]!=self.currentConfig[0]:
			dockerError=self._manageDockerPermission(value[0])
			if not dockerError:
				self.currentConfig[0]=value[0]

		if dockerError:
			return [True,PermissionManager.APPLY_CHANGES_ENABLE_DOCKER_ERROR]
		else:
			return [False,PermissionManager.APPLY_CHANGES_SUCCESSFUL]

	#def applyChanges

	def _manageDockerPermission(self,value):

		if value:
			self.writeLog("- Action: enable docker permissions")
			cmd="perm-control -e"
		else:
			self.writeLog("- Action: disable docker permissions")
			cmd="perm-control -d"

		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()
		rc=p.returncode

		if rc==0:
			self.writeLog("- Result: Change apply successfully")
			return False
			
		else:
			self.writeLog("- Result: Failed to apply change")
			return True

	#def _manageDockerPermission

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
		except Exception as e:
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

#class PermissionManager
