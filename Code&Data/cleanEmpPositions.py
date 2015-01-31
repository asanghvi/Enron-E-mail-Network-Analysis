__author__ = 'Akhil'

import pandas as pd
names=["RawEmail","RawEmpName","Position","Role"]

f = open("enronEmployeePositionsDownload.txt")
fw = open("temp.csv","w")
n = 100

fw.writelines(",".join(names)+"\n")

for line in f:
    l = line.replace("\t",",")
    for i in range(n):
        l = l.replace(" "*(n+1-i),",")

    fw.writelines(l)
f.close()
fw.close()

data = pd.read_csv("temp.csv",header=0)
data["Email"] = data.RawEmpName.apply(lambda x: x.lower().replace(" ",".")+"@enron.com")

data = data.drop_duplicates(subset="Email")
data.to_csv("empPos.csv",index=False)

# combine all data
emailData = pd.read_csv("enronDataCleaned.csv")
print emailData.shape

# make one for the sender and one for the receiver
data_r = data[["Email","Position","Role"]].copy()
data_s = data[["Email","Position","Role"]].copy()

# rename columns and merge
data_s.rename(columns={'Email':'SenderEmail',"Position":"Position_s","Role":"Role_s"},inplace=True)
allData = pd.merge(emailData,data_s,how="left",on="SenderEmail")

# rename columns and merge
data_r.rename(columns={'Email':'ReceiverEmail',"Position":"Position_r","Role":"Role_r"},inplace=True)
allData = pd.merge(allData,data_r,how="left",on="ReceiverEmail")

print allData.shape
allData.to_csv("enronDataWithPositions.csv")
