#######################################################################
#
#    MyMetrix
#    Coded by iMaxxx (c) 2013
#    Settings for BlackSpirit.HD by DeadEyE
#
#
#  This plugin is licensed under the Creative Commons
#  Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#  To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
#  or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  Alternatively, this plugin may be distributed and executed on hardware which
#  is licensed by Dream Multimedia GmbH.
#
#
#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially
#  distributed other than under the conditions noted above.
#
#
#######################################################################

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Language import language
from os import environ, listdir, remove, rename, system
from shutil import move
from skin import parseColor
from Components.Pixmap import Pixmap
from Components.Label import Label
import gettext
from enigma import ePicLoad
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from enigma import eConsoleAppContainer

#############################################################

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("BlackSpiritHD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/BlackSpiritHD/locale/"))

def _(txt):
	t = gettext.dgettext("BlackSpiritHD", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

def translateBlock(block):
	for x in TranslationHelper:
		if block.__contains__(x[0]):
			block = block.replace(x[0], x[1])
	return block


#############################################################

config.plugins.BlackSpiritHD = ConfigSubsection()

config.plugins.BlackSpiritHD.System = ConfigSelection(default="system-openatv", choices = [
				("system-openatv", _("openATV")),
				("system-openvix", _("OpenViX")),
				("system-openhdf", _("openHDF")),
				("system-openmips", _("openMips"))
				])

config.plugins.BlackSpiritHD.SelectionBackground = ConfigSelection(default="002c2c2c", choices = [
				("00000000", _("Black")),
				("002c2c2c", _("Dark Grey")),
				("007b7a7a", _("Grey")),
				("00a19181", _("BlackSpirit")),
				("00593e1e", _("Brown")),
				("00ca7700", _("Amber")),				
				("00dc5221", _("Orange")),				
				("00172b4e", _("Blue")),
				("00006292", _("Cyan")),
				("00a61d4d", _("Magenta")),
				("00A4C400", _("Lime")),
				("006A00FF", _("Indigo")),
				("00628727", _("Green")),
				("006D8764", _("Olive")),
				("009d3126", _("Red")),
				("00492561", _("Violet")),
				("00ab882a", _("Yellow"))
				])
				
config.plugins.BlackSpiritHD.SelectionFont = ConfigSelection(default="00ca7700", choices = [
				("00ffffff", _("White")),
				("00000000", _("Black")),
				("002c2c2c", _("Dark Grey")),
				("007b7a7a", _("Grey")),
				("00a19181", _("BlackSpirit")),
				("00593e1e", _("Brown")),
				("00ca7700", _("Amber")),				
				("00dc5221", _("Orange")),				
				("00172b4e", _("Blue")),
				("00006292", _("Cyan")),
				("00a61d4d", _("Magenta")),
				("00A4C400", _("Lime")),
				("006A00FF", _("Indigo")),
				("0070ad12", _("Green")),
				("006D8764", _("Olive")),
				("009d3126", _("Red")),
				("00492561", _("Violet")),
				("00ab882a", _("Yellow"))
				])
	
config.plugins.BlackSpiritHD.ProgressColor = ConfigSelection(default="_1", choices = [
				("_1", _("Normal")),
				("_2", _("Bar 2")),
				("_3", _("Bar 3")),
				("_4", _("Bar 4"))
				])
		
config.plugins.BlackSpiritHD.Infobar = ConfigSelection(default="infobar-normal", choices = [
				("infobar-normal", _("Normal")),
				("infobar-ext-sys", _("Extended ECM & System Info")),
				("infobar-ext-sat", _("Extended ECM & Sat Info"))
				])

config.plugins.BlackSpiritHD.Channelselection = ConfigSelection(default="channelsel-normal", choices = [
				("channelsel-normal", _("Normal")),
				("channelsel-minitv", _("MiniTV (Only Multi-Tuner)")),
				("channelsel-threecolumns", _("ThreeColumns")),
				("channelsel-threecolumns-minitv", _("ThreeColumns MiniTV (Only Multi-Tuner)"))
				])
				
config.plugins.BlackSpiritHD.EMCcover = ConfigSelection(default="emc-normal", choices = [
				("emc-normal", _("Text Only, Without Cover")),
				("emc-cover", _("Show Cover"))
				])
				
config.plugins.BlackSpiritHD.PluginPics = ConfigSelection(default="installpics", choices = [
				("installpics", _("Use BlackSpirit Pics")),
				("removepics", _("No, Use Default "))
				])
				
				
#######################################################################

class BlackSpiritHD(ConfigListScreen, Screen):
	skin = """
<screen name="BlackSpiritHD-Setup" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="#90000000" title="BlackSpirit.HD Konfiguration">
			<eLabel backgroundColor="#23000000" position="0,0" size="1280,720" transparent="0" zPosition="-9" />
	    <ePixmap position="0,0" size="1280,720" zPosition="-9" pixmap="BlackSpirit.HD/img/bg_screen_main.png" alphatest="off" />
    	<eLabel font="Regular; 30" halign="center" position="center,5" size="800,50" text="BlackSpirit.HD *0.53.rc1* Konfiguration" backgroundColor="#23000000" foregroundColor="#00a19181" render="Label" transparent="1" valign="center" noWrap="1" />
   		<ePixmap position="40,55" size="1200,1" pixmap="BlackSpirit.HD/img/line1200_1px.png" zPosition="1" />
   		<widget source="global.CurrentTime" position="70,25" size="180,30" font="Regular; 16" render="Label" halign="left" valign="bottom" backgroundColor="#23000000" foregroundColor="#00a19181" noWrap="1" transparent="1" zPosition="2">
   			<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
   		</widget>
   		<widget source="global.CurrentTime" position="1150,25" size="90,30" font="Regular; 16" render="Label" halign="left" valign="bottom" backgroundColor="#23000000" foregroundColor="#00a19181" noWrap="1" transparent="1" zPosition="2">
   			<convert type="ClockToText">WithSeconds</convert>
   		</widget>
			<ePixmap position="40,670" size="1200,1" zPosition="1" pixmap="BlackSpirit.HD/img/line1200_1px.png" />
	    <ePixmap position="40,710" size="1200,1" zPosition="1" pixmap="BlackSpirit.HD/img/line1200_1px.png" />
      <widget name="config" position="80,110" size="680,490" scrollbarMode="showOnDemand" backgroundColor="#23000000" transparent="1" />
      <widget name="helperimage" position="810,185" size="380,360" zPosition="1" backgroundColor="#000000" transparent="0" alphatest="blend" />
    	<ePixmap position="69,99" size="702,516" zPosition="-5" pixmap="BlackSpirit.HD/img/bg_702x516.png" transparent="0" alphatest="off" />
 	    <eLabel font="RegularBold; 15" halign="center" text="Preview" position="810,167" size="380,20" valign="top" backgroundColor="#23000000" foregroundColor="#00a19181" transparent="1" zPosition="1" />
   	  <ePixmap position="800,center" size="400,400" zPosition="-5" pixmap="BlackSpirit.HD/img/bg_eventnext.png" backgroundColor="#000000" transparent="0" alphatest="on" />
	    <ePixmap pixmap="BlackSpirit.HD/img/key_red1.png" position="113,700" size="200,5" backgroundColor="#23000000" alphatest="on" />
	    <eLabel font="Regular; 20" halign="center" text="Cancel" position="118,675" size="200,24" backgroundColor="#23000000" foregroundColor="#00a19181" transparent="1" zPosition="1" />
	    <ePixmap pixmap="BlackSpirit.HD/img/key_green1.png" position="288,700" size="200,5" backgroundColor="#23000000" alphatest="on" />
	    <eLabel font="Regular; 20" halign="center" text="Save" position="293,675" size="200,24" backgroundColor="#23000000" foregroundColor="#00a19181" transparent="1" zPosition="1" />
	    <ePixmap pixmap="BlackSpirit.HD/img/key_yellow1.png" position="463,700" size="200,5" backgroundColor="#23000000" alphatest="on" />
	    <eLabel font="Regular; 20" halign="center" text="Reboot" position="468,675" size="200,24" backgroundColor="#23000000" foregroundColor="#00a19181" transparent="1" zPosition="1" />
</screen>
"""

	def __init__(self, session, args = None, picPath = None):
		self.skin_lines = []
		Screen.__init__(self, session)
		self.container=eConsoleAppContainer()
		self.session = session
		self.datei = "/usr/share/enigma2/BlackSpirit.HD/skin.xml"
		self.dateiTMP = self.datei + ".tmp"
		self.daten = "/usr/lib/enigma2/python/Plugins/Extensions/BlackSpiritHD/data/"
		self.komponente = "/usr/lib/enigma2/python/Plugins/Extensions/BlackSpiritHD/comp/"
		self.picinstallscript = "/usr/lib/enigma2/python/Plugins/Extensions/BlackSpiritHD/pluginpics/install_pluginpics.sh"
		self.picPath = picPath
		self.Scale = AVSwitch().getFramebufferScale()
		self.PicLoad = ePicLoad()
		self["helperimage"] = Pixmap()
		list = []
		list.append(getConfigListEntry(_("________________________________ System __________________________________"), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Image"), config.plugins.BlackSpiritHD.System))
		list.append(getConfigListEntry(_("________________________________ Colors __________________________________"), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Color Selectionbar"), config.plugins.BlackSpiritHD.SelectionBackground))
		list.append(getConfigListEntry(_("Color Selectionbar Font"), config.plugins.BlackSpiritHD.SelectionFont))
		list.append(getConfigListEntry(_("Color Progress Bar"), config.plugins.BlackSpiritHD.ProgressColor))
		list.append(getConfigListEntry(_("________________________________ General __________________________________"), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Infobar and SecondInfobar"), config.plugins.BlackSpiritHD.Infobar))
		list.append(getConfigListEntry(_("Channelselection (MiniTV)"), config.plugins.BlackSpiritHD.Channelselection))
		list.append(getConfigListEntry(_("EMC Description"), config.plugins.BlackSpiritHD.EMCcover))
		list.append(getConfigListEntry(_("Special Plugin Pictures"), config.plugins.BlackSpiritHD.PluginPics))

		ConfigListScreen.__init__(self, list)
		self["actions"] = ActionMap(["OkCancelActions","DirectionActions", "InputActions", "ColorActions"], {"left": self.keyLeft,"down": self.keyDown,"up": self.keyUp,"right": self.keyRight,"red": self.exit,"yellow": self.reboot, "blue": self.showInfo, "green": self.save,"cancel": self.exit}, -1)
		self.onLayoutFinish.append(self.UpdatePicture)

	def GetPicturePath(self):
		try:
			returnValue = self["config"].getCurrent()[1].value
			path = "/usr/lib/enigma2/python/Plugins/Extensions/BlackSpiritHD/images/" + returnValue + ".png"
			return path
		except:
			pass

	def UpdatePicture(self):
		self.PicLoad.PictureData.get().append(self.DecodePicture)
		self.onLayoutFinish.append(self.ShowPicture)

	def ShowPicture(self):
		self.PicLoad.setPara([self["helperimage"].instance.size().width(),self["helperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#002C2C39"])
		self.PicLoad.startDecode(self.GetPicturePath())

	def DecodePicture(self, PicInfo = ""):
		ptr = self.PicLoad.getData()
		self["helperimage"].instance.setPixmap(ptr)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.ShowPicture()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.ShowPicture()

	def keyDown(self):
		self["config"].instance.moveSelection(self["config"].instance.moveDown)
		self.ShowPicture()

	def keyUp(self):
		self["config"].instance.moveSelection(self["config"].instance.moveUp)
		self.ShowPicture()

	def reboot(self):
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("Do you really want to reboot now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def showInfo(self):
		self.session.open(MessageBox, _("Information"), MessageBox.TYPE_INFO)

	def getDataByKey(self, list, key):
		for item in list:
			if item["key"] == key:
				return item
		return list[0]

	def save(self):
		for x in self["config"].list:
			if len(x) > 1:
					x[1].save()
			else:
					pass

		try:
			#global tag search and replace in all skin elements
			self.skinSearchAndReplace = []
			self.skinSearchAndReplace.append(["002c2c2c", config.plugins.BlackSpiritHD.SelectionBackground.value])
			self.skinSearchAndReplace.append(["00ca7700", config.plugins.BlackSpiritHD.SelectionFont.value])
			self.skinSearchAndReplace.append(["progressbar1200_1.png", "progressbar1200" + config.plugins.BlackSpiritHD.ProgressColor.value + ".png"])
			self.skinSearchAndReplace.append(["progressbar1080_1.png", "progressbar1080" + config.plugins.BlackSpiritHD.ProgressColor.value + ".png"])
			self.skinSearchAndReplace.append(["progressbar280_1.png", "progressbar280" + config.plugins.BlackSpiritHD.ProgressColor.value + ".png"])
			self.skinSearchAndReplace.append(["progressbar260_1.png", "progressbar260" + config.plugins.BlackSpiritHD.ProgressColor.value + ".png"])

#			self.container.execute("chmod a+x /usr/lib/enigma2/python/Plugins/Extensions/BlackSpiritHD/pluginpics/install_pluginpics.sh ")
			self.container.execute("chmod a+x " + self.picinstallscript + " && " + self.picinstallscript + " " + config.plugins.BlackSpiritHD.PluginPics.value)

			###Header XML
			self.appendSkinFile(self.daten + "header.xml")

			###InfoBar
			self.appendSkinFile(self.daten + config.plugins.BlackSpiritHD.Infobar.value + ".xml")

			###Channelselection
			self.appendSkinFile(self.daten + config.plugins.BlackSpiritHD.Channelselection.value + ".xml")

			###EMCcover
			self.appendSkinFile(self.daten + config.plugins.BlackSpiritHD.EMCcover.value + ".xml")

			###skin-main
			self.appendSkinFile(self.daten + "main.xml")

			###system
			self.appendSkinFile(self.daten + config.plugins.BlackSpiritHD.System.value + ".xml")

			###The End
			self.appendSkinFile(self.daten + "the-end.xml")

			xFile = open(self.dateiTMP, "w")
			for xx in self.skin_lines:
				xFile.writelines(xx)
			xFile.close()

			move(self.dateiTMP, self.datei)

			#system('rm -rf ' + self.dateiTMP)
		except:
			self.session.open(MessageBox, _("Error creating Skin!"), MessageBox.TYPE_ERROR)

		configfile.save()
		
		


		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("GUI needs a restart to apply a new skin.\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def appendSkinFile(self, appendFileName, skinPartSearchAndReplace=None):
		"""
		add skin file to main skin content

		appendFileName:
		 xml skin-part to add

		skinPartSearchAndReplace:
		 (optional) a list of search and replace arrays. first element, search, second for replace
		"""
		skFile = open(appendFileName, "r")
		file_lines = skFile.readlines()
		skFile.close()

		tmpSearchAndReplace = []

		if skinPartSearchAndReplace is not None:
			tmpSearchAndReplace = self.skinSearchAndReplace + skinPartSearchAndReplace
		else:
			tmpSearchAndReplace = self.skinSearchAndReplace

		for skinLine in file_lines:
			for item in tmpSearchAndReplace:
				skinLine = skinLine.replace(item[0], item[1])
			self.skin_lines.append(skinLine)

	def restartGUI(self, answer):
		if answer is True:
			configfile.save()
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()

	def exit(self):
		for x in self["config"].list:
			if len(x) > 1:
					x[1].cancel()
			else:
					pass
		self.close()

#############################################################

def main(session, **kwargs):
	session.open(BlackSpiritHD,"/usr/lib/enigma2/python/Plugins/Extensions/BlackSpiritHD/colors.jpg")

def Plugins(**kwargs):
	return PluginDescriptor(name="BlackSpiritHD", description=_("BlackSpirit.HD Skin configuration"), where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)