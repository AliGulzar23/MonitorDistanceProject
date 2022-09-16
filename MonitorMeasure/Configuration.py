import os
class Configuration:
    def __init__(self):
        # reads data from the config file to implement into the code
        self.frontalFaceDataLocation = "haarcascade_frontalface_default.xml"
        self.calibrationDistance = 100 #relativeDistance
        self.configFileName = "config.txt"
        self.area = 0
        self.ratio = 0
        self.minThreshold = 85 #is distance calculated is lower than value then user is too close
        self.maxThreshold = 150 #if distance calculated is higher than value then user is too far
        self.iterartion = 10
    def check_Config(self):
        return os.path.exists(self.configFileName)



    def load_From_Config(self):
        #runs when configuration is correct and program is able to run
        with open(self.configFileName) as file:
            lines = file.readlines()
            if lines is None:
                self.area = 30000 #fills in a default number
            else:
                self.area = int(lines[0])

            file.close()
        #area and distance are inversly proportional, when the face takes up more area that means the person is closer to the monitor.
        #meaured values will be using distance to determine if its close enough
        self.ratio = self.calibrationDistance * self.area

    def save_To_Config(self,area):
        file = open(self.configFileName, "w")
        file.write(str(area))
        file.close()
    def get_Ratio(self):
        return self.ratio
    def get_MinThreshold(self):
        return self.minThreshold
    def get_MaxThreshold(self):
        return self.maxThreshold
    def write_Config_File(self):
        file = open(self.configFileName, "x")

    def get_iteration(self):
        return self.iterartion
