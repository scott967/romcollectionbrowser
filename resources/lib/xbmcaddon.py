"""
	This is a dummy file for testing and debugging XBMC plugins from the
	command line. The file contains definitions for the functions found
	in xbmc, xbmcgui and xbmcplugin built in modules
"""



import os
#Addon = Addon()
_settings = {'rcb_fuzzyFactor': '3',
			'rcb_enableFullReimport': 'true',
			'rcb_createNfoWhileScraping': 'false',
			'rcb_overwriteWithNullvalues': 'false',
			'rcb_ignoreGamesWithoutDesc': 'false',
			'rcb_ignoreGamesWithoutArtwork': 'false',
			# Interact with cut-down MAME history dat file in the unittests
			'rcb_MAMEDescriptionFilePath': 'testdata/scraper_web_responses/history.dat'}


class Addon:

	def __init__(self, *args, **kwargs):
		pass

	def getAddonInfo(self, key):
		
		print 'getAddonInfo called with key: ' +str(key)
		
		if(key == 'path'):
			basepath = os.getcwd()
			path = os.path.join(basepath, "..\..")
			print 'path = ' +str(path)
			return path
		
		return 'dummy'


	def getLocalizedString(self, stringId ):
		return "mytext"

	def getSetting(self, settingId):
		"""
			Returns the value of a setting as a string.
	
			id		: string - id of the setting that the module needs to access.
	
			*Note, You can use the above as a keyword.
	
			example:
				apikey = xbmcplugin.getSetting('apikey')
		"""
		global _settings
		if _settings.has_key(settingId):
			return _settings[settingId]


