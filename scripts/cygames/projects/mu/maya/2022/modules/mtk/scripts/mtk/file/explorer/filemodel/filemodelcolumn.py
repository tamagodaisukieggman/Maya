from enum import Enum

class MtkExplorerFileModelColumn(Enum):
    u"""File Table ColumnID, Name"""
    Name = 0, "Name"
    Rev = 1, "Rev"
    Date_Modified = 2, "Date Modified"
    P4_Status = 3, "P4 Status"
    #SG_Asset_Status = 4, "SG Asset Status"
    SG_Task = 4, "SG Task                "
    #SG_Task_Status = 6, "SG Task Status"
    P4_Users = 5, "P4 Users"

    # Column Id's
    @staticmethod
    def Name_Id():
        return MtkExplorerFileModelColumn.Name.value[0]

    @staticmethod
    def Rev_Id():
        return MtkExplorerFileModelColumn.Rev.value[0]

    @staticmethod
    def Date_Modified_Id():
        return MtkExplorerFileModelColumn.Date_Modified.value[0]

    @staticmethod
    def P4_Status_Id():
        return MtkExplorerFileModelColumn.P4_Status.value[0]

    #@staticmethod
    #def SG_Asset_Status_Id():
    #    return MtkExplorerFileModelColumn.SG_Asset_Status.value[0]

    @staticmethod
    def SG_Task_Id():
        return MtkExplorerFileModelColumn.SG_Task.value[0]

    @staticmethod
    def P4_Users_Id():
        return MtkExplorerFileModelColumn.P4_Users.value[0]

    #@staticmethod
    #def SG_Task_Status_Id():
    #    return MtkExplorerFileModelColumn.SG_Task_Status.value[0]

    # Column Labels
    @staticmethod
    def Name_Label():
        return MtkExplorerFileModelColumn.Name.value[1]

    @staticmethod
    def Rev_Label():
        return MtkExplorerFileModelColumn.Rev.value[1]

    @staticmethod
    def Date_Modified_Label():
        return MtkExplorerFileModelColumn.Date_Modified.value[1]

    @staticmethod
    def P4_Status_Label():
        return MtkExplorerFileModelColumn.P4_Status.value[1]

    #@staticmethod
    #def SG_Asset_Status_Label():
    #    return MtkExplorerFileModelColumn.SG_Asset_Status.value[1]

    @staticmethod
    def SG_Task_Label():
        return MtkExplorerFileModelColumn.SG_Task.value[1]

    @staticmethod
    def P4_Users_Label():
        return MtkExplorerFileModelColumn.P4_Users.value[1]

    #@staticmethod
    #def SG_Task_Status_Label():
    #    return MtkExplorerFileModelColumn.SG_Task_Status.value[1]

    @staticmethod
    def column_ids():
        return [
            MtkExplorerFileModelColumn.Name.value[0],
            MtkExplorerFileModelColumn.Rev.value[0],
            MtkExplorerFileModelColumn.Date_Modified.value[0],
            MtkExplorerFileModelColumn.P4_Status.value[0],
            #MtkExplorerFileModelColumn.SG_Asset_Status.value[0],
            MtkExplorerFileModelColumn.SG_Task.value[0],
            #MtkExplorerFileModelColumn.SG_Task_Status.value[0],
        ]

    @staticmethod
    def column_labels():
        return [
            MtkExplorerFileModelColumn.Name.value[1],
            MtkExplorerFileModelColumn.Rev.value[1],
            MtkExplorerFileModelColumn.Date_Modified.value[1],
            MtkExplorerFileModelColumn.P4_Status.value[1],
            #MtkExplorerFileModelColumn.SG_Asset_Status.value[1],
            MtkExplorerFileModelColumn.SG_Task.value[1],
            #MtkExplorerFileModelColumn.SG_Task_Status.value[1],
        ]