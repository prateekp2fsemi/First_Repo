import time
start = time.time()
import numpy as np
import pandas as pd

strtpt = np.array([])
endpt = np.array([])
strtclk = np.array([])
endclk = np.array([])
bclist = np.array([])
iclist = np.array([])
bdlist = np.array([])
idlist = np.array([])
bfinvperclist = np.array([])
slcklist = np.array([])
ntdelaylist = np.array([])
ntpthperc = np.array([])
clkperiodlist = np.array([])
throughlist = np.array([])
TotalLollist = np.array([])

df = pd.read_csv('parseroutput.csv',sep='\t',header=None)

# l1, l2 and l3 have the indexes of each path.
l1 = df.loc[df.applymap(lambda x:x.strip().startswith('Startpoint'))[0]].index
l2 = df.loc[df.applymap(lambda x:x.strip().startswith('Point'))[0]].index
l3 = df.loc[df.applymap(lambda x:x.strip().startswith('slack'))[0]].index+1

# print(len(l1))

for i in range(len(l1)):
    
    # Initialize variables to zero at the beginning of each loop
    BufferCount = 0
    BufferDelay = 0
    InverterCount = 0
    InverterDelay = 0
    Data_arr_time = 0
    BuffplusInv = 0
    BuffInvPathPerc = 0
    netdelay = 0
    ntprc = 0

    #####################################
    # Extract StartPoint, EndPoint, Start Clock and End Clock
    #####################################
    
    # Assign header of the report to a data frame for each path
    dfa = df.iloc[l1[i]:l2[i]]
    dfb = dfa[0].str.split(':',expand=True)

    # Startpoint
    strtpt = np.append(strtpt,[dfb.iloc[0,1].split()[0]],axis=0)
    # Endpoint
    endpt = np.append(endpt,[dfb.iloc[1,1].split()[0]],axis=0)
    # Start Clock
    strtclk = np.append(strtclk,[dfb.iloc[0,1].split()[-1].replace(')','')],axis=0)
    # End Clock
    endclk = np.append(endclk,[dfb.iloc[1,1].split()[-1].replace(')','')],axis=0)

    #####################################
    ######################################
    # Assign Body of the report to a DataFrame for each path
    dfa = df.iloc[l2[i]:l3[i]]

     # Calculate Buffer Count and Buffer delay
    dfb = dfa.loc[(dfa[0].str.contains('BUFF|BUF|BF'))& ~(dfa[0].str.contains('\(net\)'))]
    dfb = dfb[0].str.split(expand = True)
    # Buffer count
    BufferCount = format(int(len(dfb[1::2])),'d')
    bclist = np.append(bclist,[BufferCount],axis=0)
    # Buffer delay
    if(len(dfb)>0):
        BufferDelay = dfb[3].iloc[1::2].apply(lambda x:float(x))
        bdlist = np.append(bdlist,[format(BufferDelay.sum(),'.2f')],axis=0)
    else:
        bdlist = np.append(bdlist,[BufferDelay],axis=0)
    
    # Calculate INV count and delay
    dfb = dfa.loc[(dfa[0].str.contains('INV|IV'))]
    dfb = dfb[0].str.split(expand = True)
#     # Inverter count
    InverterCount = format(int(len(dfb[1::2])),'d')
    iclist = np.append(iclist,[InverterCount],axis=0)
#     # Inverter delay
    if(len(dfb)>0):
        InverterDelay = dfb[3].iloc[1::2].apply(lambda x:float(x))
        idlist = np.append(idlist,[format(InverterDelay.sum(),'.2f')],axis=0)
    else:
        idlist = np.append(idlist,[InverterDelay],axis=0)

    # Calculate %(Buff+Inv/Path)
    dfb = dfa.loc[dfa[0].str.contains('data arrival time')]
    # Extract Data Arrival Time
    Data_arr_time = float(dfb[0].str.split(expand=True)[3].iloc[0].replace(',',''))

    if int(BufferCount) and int(InverterCount) > 0:
        BuffplusInv = np.add(BufferDelay.sum(),InverterDelay.sum())
        BuffInvPathPerc = BuffplusInv/Data_arr_time*100 
        bfinvperclist = np.append(bfinvperclist,[format(BuffInvPathPerc,'.2f')],axis=0)
    else:
        BuffplusInv = np.add(BufferDelay,InverterDelay)
        BuffInvPathPerc = BuffplusInv/Data_arr_time*100
        bfinvperclist = np.append(bfinvperclist,[format(BuffInvPathPerc.sum(),'.2f')],axis=0)
   
    # Calculate Net delay and %(Net/Path)
    dfb = df.iloc[dfa.loc[dfa[0].str.contains('\(net\)')].index+1]
    dfb = dfb[0].str.split(expand=True)[3].astype(np.float64)
    if (len(dfb)>0):
        netdelay = dfb.sum()
    ntdelaylist = np.append(ntdelaylist,[netdelay],axis=0)
    ntprc = format(netdelay/Data_arr_time*100,'.2f')
    ntpthperc = np.append(ntpthperc,[ntprc],axis=0) 

    # Slack
    dfb = dfa.loc[dfa[0].str.contains('slack')]
    slcklist = np.append(slcklist,[dfb[0].str.split(expand=True)[2].sum().replace(',','')],axis=0)
    
#     # Clock Period
    dfb = dfa.loc[dfa[0].str.contains('\(rise edge\)')]
    dfb = dfb[0].str.split(expand = True)
    dfb = dfb.reset_index(drop = True)
    clkperiodlist = np.append(clkperiodlist,[np.diff(float(dfb.iloc[1,4]),float(dfb.iloc[0,4]))],axis=0)

    # Total LOL
    dfa = df.iloc[l2[i]+3:l3[i]-14]
    dfb = dfa.loc[~dfa[0].str.contains('BUFF|BUF|BF|INV|IV|\(net\)|CLK',case=True)]
    
    TotalLollist = np.append(TotalLollist,[dfb[1::2][0].count()],axis=0)

    #Through
    dfa = df.iloc[l2[i]+4 :l3[i]-12]    
    dfa = dfa.loc[~dfa[0].str.contains('\(net\)')]
    dfb = dfa[0].str.split(expand=True)
    dfb = dfb[0]+dfb[1]
    dfb = dfb.str.split('/',4,expand=True)
    dfb[0] = dfb[0]+'/'+dfb[1]+'/'+dfb[2]
    dfb = dfb.drop(columns=[1])
    dfba = dfb[1::2]
    # dfba = pd.concat([dfba,dfb.iloc[len(dfb)-1].to_frame().transpose()],axis=0)
    # dfba = dfba.groupby([0])[0].count()
    # d = dfba.to_dict()
    # throughlist = np.append(throughlist,[d],axis=0)
    print(dfba)
    break 
    
    # print(throughlist)
# df = pd.DataFrame({"Startpoint"                 :           strtpt,
#                     "Endpoint"                  :           endpt ,
#                     "Start Clock"               :           strtclk,
#                     "End Clock"                 :           endclk,
#                     "Net Delay"                 :           ntdelaylist,
#                     "CLK_Period"                :           clkperiodlist,
#                     "Through"                   :           throughlist,
#                     "% Net/Path"                :           ntpthperc,
#                     "#Buff_Count"               :           bclist,
#                     "BUFF_Delay"                :           bdlist,
#                     "Inv_Count_list"            :           iclist,
#                     "Inv_delay_list"            :           idlist,
#                     "Buff_plus_inv_perc_list"   :           bfinvperclist,
#                     "Approximate LOL"           :           TotalLollist,
#                     "Slack"                     :           slcklist})

# with pd.ExcelWriter("output3.xlsx") as writer:
#     df.to_excel(writer,index=None)
    

# # print("Execution time : ",(time.time()-start)/100)

# print(strtpt)
# print(endpt)
# print(strtclk)
# print(endclk)
# print(bclist)
# print(bdlist)
# print(iclist)
# print(idlist)
# print(bfinvperclist)
# print(ntdelaylist)
# print(ntpthperc)
# print(slcklist)
# print(clkperiodlist)
# print(TotalLollist)