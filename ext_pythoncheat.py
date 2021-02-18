import pymem
import pymem.process
import time
import oGUI
import keyboard

# !! This code is definitely not written to be read, it's more of a learning experience for me. !! 

dwLocalPlayer = (0xD8B2BC)
m_flFlashMaxAlpha = (0xA41C)
dwEntityList = (0x4DA2F44)
m_iTeamNum = (0xF4)
dwGlowObjectManager = (0x52EB540)
m_iGlowIndex = (0xA438)
dwSetClanTag = (0x8A1A0)

print("Waiting for OGUI...")

oGUI.init()
print("oGUI initialized.")

noFlashCheck = oGUI.Checkbox(oGUI.gray, oGUI.orange, 125, 150, 20, 20, True)
glowCheck = oGUI.Checkbox(oGUI.gray, oGUI.orange, 125, 125, 20, 20, True)
glowText = oGUI.Text(oGUI.gray, 70, 125, 15, "Glow")
noFlashText = oGUI.Text(oGUI.gray, 60, 150, 15, "No Flash")
title = oGUI.Text(oGUI.green, 50, 50, 20, "CSGO Pycheat developed by: awsumturtle#6969")

def main():
	print('CSGO Pycheat has been initialized.')
	pm = pymem.Pymem("csgo.exe")
	client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
	engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll

	while True:
		if keyboard.is_pressed('end'):
			exit(0)
		player = pm.read_int(client + dwLocalPlayer)
		glow_manager = pm.read_int(client + dwGlowObjectManager)
		oGUI.startLoop()
		noFlashCheck.draw()
		noFlashText.draw()
		title.draw()
		glowCheck.draw()
		glowText.draw()
		oGUI.endLoop()
		for i in range(1, 32):
			entity = pm.read_int(client + dwEntityList + i * 0x10)

			if entity:
				entity_team_id = pm.read_int(entity + m_iTeamNum)
				entity_glow = pm.read_int(entity + m_iGlowIndex)

				if entity_team_id == 2:
					pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))
					pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))
					pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))
					pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))
					isGlow = glowCheck.is_enabled()
					if isGlow:
						pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)
					elif isGlow == False:
						pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 0)

				elif entity_team_id == 3:
					pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))
					pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))
					pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))
					pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))
					isGlow = glowCheck.is_enabled()
					if isGlow:
						pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)
					elif isGlow == False:
						pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 0)

		if player:
			flash_value = player + m_flFlashMaxAlpha
			if flash_value:
				isNoFlash = noFlashCheck.is_enabled()
				if isNoFlash:
					pm.write_float(flash_value, float(0))
				elif isNoFlash == False:
					pm.write_float(flash_value, float(200))

if __name__ == '__main__':
	main()
