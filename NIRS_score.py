import pandas as pd
import numpy as np

rest=[]
task_first=[]
task_last=[]
rest_ave=[]
rest_std=[]


#Aの場合
EX="YamadaTaro"
NoS=["01","12","13","14"]
SubjectS=["A","B","C","D","E","F","G","H","I","J"]


for No in NoS:
    Dscore_sample=pd.DataFrame()
    Zscore_sample=pd.DataFrame()
    for Subject in SubjectS: 
        importname = "F:\\元データ\\NIRS\\" +EX+"\\"+No+ Subject+"_Hb_CBox33_Oxy.csv" 
        h=49 
        #ch4からch19とMarkerを読み込み
        df=np.array(pd.read_csv(importname,index_col=None,usecols=[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,23],header=h)) 
        #マーカーの位置を探索
        mark=0
        mark_count=0
        for i in df[:,16]: 
            mark_count=mark_count+1
            if i!=0:mark=mark_count
        #データを分割
        rest=df[mark:mark+300,:] #前レスト
        task_first=df[mark+300:mark+1800,:] #タスク前半
        task_last=df[mark+1800:mark+3300,:] #タスク後半
        rest_ave=np.mean(rest,axis=0) #各chの平均値
        rest_std=np.std(rest,axis=0) #各chの標準偏差
        #各chのレストとタスク後半の差分を求める
        Dscore=[]
        D_ave=0
        Dscore_ave=[]
        #各chのZscoreの平均値を求める
        Zscore=[]
        Z_ave=0
        Zscore_ave=[]
        
        for j in range(16): #各chで計算
            r_ave=rest_ave[j]
            r_std=rest_std[j]
            Dscore=task_last[:,j]-r_ave#chの差分を計算
            Zscore=Dscore/r_std #chのZscoreを計算
            D_ave=np.mean(Dscore)
            Z_ave=np.mean(Zscore)
            Dscore_ave=np.append(Dscore_ave,D_ave)
            Zscore_ave=np.append(Zscore_ave,Z_ave)
        #サンプル番号Noの協力者名Subjectのデータ完成    
        col=[No+Subject]
        inx=['ch4','ch5','ch6','ch7','ch8','ch9','ch10','ch11','ch12','ch13','ch14','ch15','ch16','ch17','ch18','ch19']
        Dscore_ave=pd.DataFrame(data=Dscore_ave,index=inx,columns=col)
        Zscore_ave=pd.DataFrame(data=Zscore_ave,index=inx,columns=col)
        #記録用のデータフレームに連結
        Dscore_sample=pd.concat([Dscore_sample,Dscore_ave],axis=1)
        Zscore_sample=pd.concat([Zscore_sample,Zscore_ave],axis=1)
    #サンプルごとのデータを出力
    Dscore_sample=Dscore_sample.T
    Zscore_sample=Zscore_sample.T
    Dscore_sample.to_csv('F:\\解析結果\\NIRS\\'+EX+'\\D_score\\NIRS_No'+No+'_Dscore.csv')
    Zscore_sample.to_csv('F:\\解析結果\\NIRS\\'+EX+'\\Z_score\\NIRS_No'+No+'_Zscore.csv')