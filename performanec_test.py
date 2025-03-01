## should import the network and runn standatized test and track time 
from time import time
from datetime import datetime
import pandas as pd
from network import network
import os 

def read_file()->pd.DataFrame:
    ''' 
    tryes to read the file with the last test runns and return the pd dataframe
    if file not exist creat it
    '''
    PATH_TO_FILE = 'code/percomance_test.csv'
    COLUMNS = ['test_id','date','time', 'nodes', 'time_intervall', 'time_frame']
    ## test if file exist
    if os.path.exists(PATH_TO_FILE) == False:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(PATH_TO_FILE,index=None)
    df = pd.read_csv(PATH_TO_FILE)
    return df

def write_file(df):
    PATH_TO_FILE = 'code/percomance_test.csv'
    df.to_csv(PATH_TO_FILE,index=None)
    return None



def manage_test():
    print('1: random network 5000 nodes\n2:Brazill data with pow(10,3)')
    auswahl = input('which test do you want to run?: ')
    auswahl = auswahl.strip()
    if isinstance(int(auswahl),int) == False:
        raise TypeError ('auswahl muss eine zahl sein')
    auswahl = int(auswahl)

    start_time = time()
    if auswahl == 1 :
        size = 5000
        time_intervall = 1
        time_frame = 0
        run_test_1(size)
    
    if auswahl == 2:
        size, time_frame, time_intervall = run_test_2()


    run_time = time()-start_time
    date_time = str(datetime.now())
    
    return([auswahl,date_time,run_time,size,time_intervall,time_frame])


def run_test_1(size):
    ''' 
    läst den ersten test laufen
    '''
    n = network()
    n.generate_a_network_version2(size,3,0.4)
    n.shock_network(30,1)
    n.check_cascade_with_new_nodes()

def run_test_2():
    time_frame = pow(10,3)
    n = network(time_frame)
    n.read_csv('code/dataFakhteh/brazil.txt',0.4)
    size = len(n.nodes)
    time_interval = len(n.get_zeitpunkte())
    n.shock_network(int(size*0.05),1)
    n.check_cascade_with_new_nodes()
    return size , time_frame, time_interval
















performance_df =  read_file()
results = manage_test()
performance_df.loc[len(performance_df)] = results
write_file(performance_df)
