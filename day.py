import block
import constants as c

class Day:
    def __init__(self, df, week):
        self.df = df
        self.blocks = []
        self.date = df[c.TS_DATE].iloc[0]
        # TODO: change "Lunch" to a number
        self.lunchTaken = True
        lunchRow =  df[df[c.TS_ACTIVITY].str.contains(c.ACTIVITY_CODE_LUNCH)]
        if (not self.cannotHaveLunch()):
            if not lunchRow.empty:
                lunchRow = lunchRow.iloc[0]
                temp = lunchRow[c.TS_HOURS]
                # if temp is less than 20 minutes
                if (temp < (1.0 / 60.0) * 20.0):
                    self.lunchTaken = False

            else:
                self.lunchTaken = False



        self.hours = self.df[c.TS_PAYROLL_HOURS].sum()
        self.week = week


    def addBlock(self, row, totalHours):
        if (str(row[c.TS_ACTIVITY]).find(c.ACTIVITY_CODE_LUNCH) != -1):
            return
        elif (totalHours > 40 and (totalHours - row[c.TS_PAYROLL_HOURS] < 40)):
            nonOvertimeHours = 40 - (totalHours - row[c.TS_PAYROLL_HOURS])
            overtimeHours = row[c.TS_PAYROLL_HOURS] - nonOvertimeHours
            
            self.blocks.append(block.Block(row, self, nonOvertimeHours))
            self.blocks.append(block.Block(row, self, overtimeHours, True))
        elif (totalHours > 40):
            self.blocks.append(block.Block(row, self, row[c.TS_PAYROLL_HOURS], True))
        else:
            self.blocks.append(block.Block(row,self, row[c.TS_PAYROLL_HOURS]))

    def hadLunch(self):
        if not self.lunchTaken:
            return False
        return True

    def getLunchBlock(self, time, isOvertime):
        return block.Block(self.df.iloc[-1],self, time, isOvertime, False)

    def moveLunchBlock(self):
        # put lunch block at end of day
        self.blocks.append(self.blocks.pop(0))

    def cannotHaveLunch(self):
        # search through each rom and see if 
        # the activity code is 280 or 300 before the blocks are created
        for index, row in self.df.iterrows():
            activity = row[c.TS_ACTIVITY]
            costCode = c.DEFAULT_COSTCODE
            if '-' in activity:
                costCode = float(activity.split('-')[0].strip())
            # kill lunch deduct if related to snow pay
            if (costCode == 280 or costCode == 300):
                return True 
            # kill lunch deduct if related to deliveries (Joanne to add new cost code per discussion on 12/19/22
            elif (costCode ==4):
                return True
            # Joanne said NOT to kill lunch deduct if related to 9000-9999 per discussion on 12/19/22
            # elif (costCode >= 9000 and costCode <= 9999):
            #     return True

        return False


        

