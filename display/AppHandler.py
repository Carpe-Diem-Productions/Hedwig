import json
import glob

'''
TODO: something like statically defining the buttons and their actions and have the main display driver
# drive all the animations and screen update and etc.

'''


class AppHandler:
    def __init__(self, startupAppName="HomeApp"):
        self.startupApp = startupAppName
        self.currentApp = self.startupApp
        self.apps = dict()
        allAppsJSON = glob.glob('*.json')
        if len(allAppsJSON) == 0:
            raise RuntimeError("No apps detected in the folder.")
        for singleAppJSON in allAppsJSON:
            f = open(singleAppJSON, 'r')
            if f:
                parsedApp = json.load(f)
                if parsedApp['name'] in self.apps.keys():
                    raise RuntimeError("Duplicate App JSON detected (name = {})".format(parsedApp['name']))
                else:
                    self.apps[parsedApp['name']] = parsedApp
                f.close()

    def getCurrentApp(self):
        return self.apps[self.currentApp]

    def setCurrentApp(self, appName):
        self.currentApp = appName


def test_AppHandler():
    testAppHandler = AppHandler()
    for app in testAppHandler.apps.items():
        print(app)
