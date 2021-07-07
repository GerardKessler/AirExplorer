# -*- coding: utf-8 -*-
# Copyright (C) 2021 Gerardo Kessler <ReaperYOtrasYerbas@gmail.com>
# This file is covered by the GNU General Public License.

import appModuleHandler
from scriptHandler import script
import api
import controlTypes
from ui import message
from winsound import PlaySound, SND_FILENAME, SND_ASYNC
from os import path
from keyboardHandler import KeyboardInputGesture
from inputCore import manager
import addonHandler

# Lína de traducción
addonHandler.initTranslation()

class AppModule(appModuleHandler.AppModule):

	fg = ""
	elementObj = ""
	toolObj = ""
	category = "AirExplorer"
	# Translators: Añade el texto herramientas activas al nombre de la nube
	activeTools = _('Herramientas activas de')

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		try:
			if obj.name == None and obj.role == controlTypes.ROLE_PANE:
				clsList.insert(0, CloudOptions)
		except:
			pass

	def event_NVDAObject_init(self, obj):
		self.fg = api.getForegroundObject()
		try:
			if obj.name == None and obj.role == controlTypes.ROLE_PANE:
				self.elementObj = obj.parent.next
				self.toolObj = obj.parent.next.next
				obj.name = "{} {}".format(self.activeTools, self.elementObj.children[3].children[0].children[5].name)
		except (AttributeError, IndexError):
			pass

	def event_gainFocus(self, obj, nextHandler):
		try:
			if obj.name == '' and obj.role == controlTypes.ROLE_DOCUMENT:
				obj.simplePrevious.doAction()
				PlaySound("C:/Windows/Media/Speech Disambiguation.wav", SND_FILENAME | SND_ASYNC)
				nextHandler()
			else:
				nextHandler()
		except:
			nextHandler()

	@script(gestures=[f"kb:control+{i}" for i in range(1, 10)])
	def script_status(self, gesture):
		key = -(int(gesture.mainKeyName) + 1)
		try:
			filePath = self.fg.children[0].children[3].children[0].children[3].children[0].children[3].children[0].children[3].children[1].children[3].children[0].children[3].children[0].children[3].children[key].children[1].name
			elementName = path.basename(filePath)
			progress = self.fg.children[0].children[3].children[0].children[3].children[0].children[3].children[0].children[3].children[1].children[3].children[0].children[3].children[0].children[3].children[key].children[5].name
			# Translators: Añade la palabra porcentaje al valor
			message(_('{}; {} porciento'.format(elementName, progress)))
		except (TypeError, IndexError):
			# Translators: Anuncia que no hay datos
			message(_('Sin datos'))

	@script(
		category = category,
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Activa el panel de cuentas'),
		gesture="kb:control+shift+c")
	def script_cuentas(self, gesture):
		obj = self.fg.children[0].children[3].children[3].children[3].children[0].children[3].children[5]
		message(obj.name)
		obj.doAction()

	@script(
		category = category,
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Activa el panel de opciones'),
		gesture="kb:control+shift+o")
	def script_opciones(self, gesture):
		obj = self.fg.children[0].children[3].children[3].children[3].children[0].children[3].children[6]
		message(obj.name)
		obj.doAction()

	@script(
		category = category,
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Se mueve al siguiente de los 3 elementos posibles'),
		gesture="kb:pagedown")
	def script_nextElement(self, gesture):
		fc = api.getFocusObject()
		if fc.role != controlTypes.ROLE_LISTITEM and fc.role != controlTypes.ROLE_LIST:
			manager.emulateGesture(KeyboardInputGesture.fromName("tab"))
		else:
			PlaySound("C:/Windows/Media/Windows Information Bar.wav", SND_ASYNC | SND_FILENAME)

	@script(
		category = category,
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Se mueve al anterior de los 3 elementos posibles'),
		gesture="kb:pageup")
	def script_previousElement(self, gesture):
		fc = api.getFocusObject()
		if fc.role != controlTypes.ROLE_TAB:
			manager.emulateGesture(KeyboardInputGesture.fromName("shift+tab"))
		else:
			PlaySound("C:/Windows/Media/Windows Information Bar.wav", SND_ASYNC | SND_FILENAME)

class CloudOptions():

	tools = ""

	def initOverlayClass(self):
		try:
			if self.name == None and self.role == controlTypes.ROLE_PANE:
				self.bindGestures({"kb:n":"newFolder", "kb:z":"zipLoad", "kb:v":"changeView", "kb:s":"freeSpace"})
				self.tools = self.parent.next.next
		except AttributeError:
			pass

	def script_newFolder(self, gesture):
		message(self.tools.children[3].children[1].name)
		self.tools.children[3].children[1].doAction()

	def script_zipLoad(self, gesture):
		message(self.tools.children[3].children[6].name)
		self.tools.children[3].children[6].doAction()

	def script_changeView(self, gesture):
		message(self.tools.children[3].children[-1].name)
		self.tools.children[3].children[-1].doAction()

	def script_freeSpace(self, gesture):
		message(self.parent.next.next.next.children[3].children[2].name)
