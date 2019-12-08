
ScriptName = "Note"
Website = "http://chienjuho.com/courses/cse518a/fa2019/"
Description = "Awards viewers 10 currency for each video annotation"
Creator = "Charlie"
Version = "1.0.0"

def Init():
    return

def Execute(data):
    if data.GetParam(0) != "!note":
        return

    Parent.AddPoints(data.User,data.UserName,10)
    return

def Tick():
    return
