# -*- coding: utf-8 -*-
# Copyright (C) 2021 Gerardo Kessler <ReaperYOtrasYerbas@gmail.com>
# This file is covered by the GNU General Public License.

import appModuleHandler
from scriptHandler import script
import api
import winUser
import controlTypes
from ui import message
from winsound import PlaySound, SND_FILENAME, SND_ASYNC
from re import search
from os import path
from keyboardHandler import KeyboardInputGesture
from inputCore import manager
from threading import Thread
from time import sleep
import addonHandler

# Lína de traducción
addonHandler.initTranslation()

class AppModule(appModuleHandler.AppModule):

	fg = ""
	elementObj = ""
	toolObj = ""
	category = "AirExplorer"
	# Translators: Mensaje que anuncia la disponibilidad solo desde un objeto específico
	errorMsg = _('Opción solo disponible desde el objeto situado entre el árbol y la lista de archivos')

	def event_NVDAObject_init(self, obj):
		self.fg = api.getForegroundObject()

	def event_gainFocus(self, obj, nextHandler):
		try:
			if obj.name == '' and obj.role == controlTypes.ROLE_DOCUMENT:
				obj.simplePrevious.doAction()
				PlaySound("C:/Windows/Media/Windows Recycle.wav", SND_FILENAME | SND_ASYNC)
			elif obj.parent.next.name == 'elementHost1' and obj.role == controlTypes.ROLE_PANE:
				self.elementObj = obj.parent.next
				self.toolObj = obj.parent.next.next
				message(self.elementObj.children[3].children[0].children[5].name)
			else:
				nextHandler()
		except:
			nextHandler()

	@script(gestures=[f"kb:control+{i}" for i in range(1, 10)])
	def script_status(self, gesture):
		key = -(int(gesture.mainKeyName) + 1)
		try:
			statusObj = self.fg.children[0].children[3].children[0].children[3].children[0].children[3].children[0].children[3].children[1].children[3].children[0].children[3].children[0].children[3].children[key].name
			objName = search(r"Origen.+Destino", statusObj)
			fileName = path.basename(objName[0][8:][:-9])
			progress = search(r"Progreso\:\s\d+", statusObj)
			# Translators: añade la palabra porciento al número del porcentaje
			message(_('{}; {} porciento').format(fileName, progress[0][10:]))
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
		gesture="kb:.")
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
		gesture="kb:,")
	def script_previousElement(self, gesture):
		fc = api.getFocusObject()
		if fc.role != controlTypes.ROLE_TREEVIEWITEM:
			manager.emulateGesture(KeyboardInputGesture.fromName("shift+tab"))
		else:
			PlaySound("C:/Windows/Media/Windows Information Bar.wav", SND_ASYNC | SND_FILENAME)

	@script(
		category = category,
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Activa la opción opciones de la nube'),
		gesture="kb:control+shift+p"
	)
	def script_cloudOptions(self, gesture):
		try:
			toolObj = api.getFocusObject().parent.next.next
			if toolObj.name == 'toolStrip1':
				message(toolObj.children[3].children[10].name)
				toolObj.children[3].children[10].doAction()
			else:
				message(self.errorMsg)
		except (IndexError, AttributeError):
			message(self.errorMsg)
