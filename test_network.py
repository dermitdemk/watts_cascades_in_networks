import json

def extract_first_cell(ipynb_file: str, output_py_file: str):
    """
    Extracts the first code cell from a Jupyter notebook and writes it to a .py file.

    :param ipynb_file: Path to the Jupyter notebook (.ipynb) file.
    :param output_py_file: Path to the output Python (.py) file.
    """
    try:
        # Load the notebook
        with open(ipynb_file, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Find the first code cell
        first_cell = next(
            (cell for cell in notebook.get('cells', []) if cell.get('cell_type') == 'code'), 
            None
        )
        
        if first_cell is None:
            raise ValueError("No code cell found in the notebook.")

        # Write the source code of the first cell to the output file
        with open(output_py_file, 'w', encoding='utf-8') as f:
            f.write("# Extracted from the notebook\n")
            f.write("\n".join(first_cell.get('source', [])))

        print(f"Successfully extracted the first cell to {output_py_file}.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
extract_first_cell("code/main.ipynb", "code/network.py")


import unittest
from network import network
import pandas as pd
from copy import deepcopy

class TestNetwork(unittest.TestCase):
    
    @classmethod
    def setUp(self):
        """
        defines all networks needet for the test

        Networks:
            simple_network
            second_network
            simple_temporal_network: has the same nodes as the simple network but addes timepontis to connections
        """
        
        ## first test network
        self.simple_network = network()
        for i in range(1,6):
            self.simple_network.add_node(info_as_list=[i,0.1,0])
        for i in range(6,8):
            self.simple_network.add_node(info_as_list=[i,0.2,2])
        self.simple_network.add_connection([1,2])
        self.simple_network.add_connection([1,3])
        self.simple_network.add_connection([2,4])
        self.simple_network.add_connection([3,2])
        self.simple_network.add_connection([6,7])


        ## second network
        self.second_network = network()
        for i in range(1,9):
            self.second_network.add_node(info_as_list=[i,0.1,0])
        for i in range(1,9):
            self.second_network.add_connection([i,((i)%8)+1])
        
        #######################################################
        ############## Temporal networks#######################
        #######################################################

        ## third network
        self.simple_temporal_network = network()
        for i in range(1,6):
            self.simple_temporal_network.add_node(info_as_list=[i,0.1,0])
        for i in range(6,8):
            self.simple_temporal_network.add_node(info_as_list=[i,0.2,2])
        self.simple_temporal_network.add_connection([1,2,0])
        self.simple_temporal_network.add_connection([1,3,0])
        self.simple_temporal_network.add_connection([1,3,1])
        self.simple_temporal_network.add_connection([1,3,4])
        self.simple_temporal_network.add_connection([1,3,2])
        self.simple_temporal_network.add_connection([2,4,0])
        self.simple_temporal_network.add_connection([2,4,4])
        self.simple_temporal_network.add_connection([3,2,3])
        self.simple_temporal_network.add_connection([6,7,2])



        ## second temporal network
        self.second_temporal_network = network()
        for i in range(1,9):
            self.second_temporal_network.add_node(info_as_list=[i,0.1,0])
        for i in range(1,9):
            self.second_temporal_network.add_connection([i,((i)%8)+1,i%6])
        
        pass
    
    def test_node_info(self):
        
        self.assertEqual(self.simple_network.nodeInfo.to_dict(), {
                                                        'p': {1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1, 6: 0.2, 7: 0.2},
                                                        'c': {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 2.0, 7: 2.0}}, 
                        'node info is not as expecdet')
        self.assertEqual(self.simple_temporal_network.nodeInfo.to_dict(), {
                                                        'p': {1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1, 6: 0.2, 7: 0.2},
                                                        'c': {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 2.0, 7: 2.0}}, 
                        'node info is not as expecdet')
    def test_adding_node(sefl):
        pass 
        
    def test_connection(self):
        """Test if node connections are correct."""
        connections = {
            1: [2, 3],
            2: [1, 3, 4],
            3: [1, 2],
            4: [2],
            5: [],
            6: [7],
            7: [6]
        }
        for node, expected in connections.items():
            self.assertEqual(self.simple_network.find_all_conection_of_node(node), expected, f'Connections for node {node} are wrong.')
        temporal_connections = {
            1: [{'time':0, 'connection':[2, 3]}, {'time':1, 'connection':[3]},{'time':2, 'connection':[3]}, {'time':4, 'connection':[3]}],
            2: [{'time':0, 'connection':[1,4]},{'time':4, 'connection':[4]} ],
            3: [{'time':0, 'connection':[1]}, {'time':1, 'connection':[1]}, {'time':3, 'connection':[2]} ],
            4: [{'time':0, 'connection':[2]}, {'time':4, 'connection':[2]},{'time':1, 'connection':[]}, ],
            5: [{'time':0, 'connection':[]}, {'time':2, 'connection':[]}, {'time':3, 'connection':[]},  ],
            6: [{'time':2, 'connection':[7]}, ],
            7: [{'time':2, 'connection':[6]}, ]
        }
        for node, connection_all_time in temporal_connections.items():
            for connection in connection_all_time:
                self.assertEqual(self.simple_temporal_network.find_all_conection_of_node(node,connection['time']), connection['connection'], f'Connections for node {node} at time {connection['time']} are wrong.')


        
            



    
    def test_path(self):
        path = {
            1 : [1, 2, 3, 4],
            2 :  [2, 1, 3, 4],
            3 :  [3, 1, 2, 4],
            4 :  [4, 2, 1, 3],
            5 :  [5],
            6 :  [6,7],
            7 :  [7,6],
        }
        for node, expected in path.items():
            self.assertEqual(self.simple_network.check_for_path(node),expected,  f'Path for node {node} is wrong.')
        
        path = {
            1 : [{'time':0, 'path':[1, 2, 3, 4]}, {'time':1, 'path':[1, 3]}, {'time':2, 'path':[1, 3]}, {'time':3, 'path':[1]}, {'time':4, 'path':[1, 3]}],
            2 :  [{'time':0, 'path':[2, 1, 4, 3]}, {'time':1, 'path':[2]}, {'time':2, 'path':[2]}, {'time':3, 'path':[2,3]}, {'time':4, 'path':[2,4]}],
            3 : [{'time':0, 'path':[3, 1, 2, 4]}, {'time':1, 'path':[3, 1]}, {'time':2, 'path':[3, 1]}, {'time':3, 'path':[3, 2]}, {'time':4, 'path':[3, 1]}],
            4 : [{'time':0, 'path':[4, 2, 1, 3]}, {'time':1, 'path':[4]}, {'time':2, 'path':[4]}, {'time':3, 'path':[4]}, {'time':4, 'path':[4,2]}],
            5 :[{'time':0, 'path':[5]}, {'time':1, 'path':[5]}, {'time':2, 'path':[5]}, {'time':3, 'path':[5]}, {'time':4, 'path':[5]}],
            6 :  [{'time':0, 'path':[6]}, {'time':1, 'path':[6]}, {'time':2, 'path':[6,7]}, {'time':3, 'path':[6]}, {'time':4, 'path':[6]}],
            7 :  [{'time':0, 'path':[7]}, {'time':1, 'path':[7]}, {'time':2, 'path':[7,6]}, {'time':3, 'path':[7]}, {'time':4, 'path':[7]}],
        }
        for node, expected in path.items():
            for intervall in expected:
                self.assertEqual(self.simple_temporal_network.check_for_path(node, intervall['time']),intervall['path'],  f'Path for node {node} at time {intervall["time"]} is wrong.')
        


    def test_color_testing(self):
        colors = {
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:2,
            7:2,
        }
        for node, color in colors.items():
            self.assertTrue(self.simple_network.test_if_c_is_color(node, color),f'color for {node} is not {color}')
            
            color2 = color*2
            self.simple_network.nodeInfo.iloc[node-1]['c'] = color2
            self.assertTrue(self.simple_network.test_if_c_is_color(node,color2),f'color for {node} is not {color2}')
            
            self.simple_network.update_node_c(node,color)
            self.assertTrue(self.simple_network.test_if_c_is_color(node, color),f'color for {node} is not {color}')

            ## temp network
            self.assertTrue(self.simple_temporal_network.test_if_c_is_color(node, color), f'color for {node} is not {color}')

    
    def test_mean_color(self):
        mean_colors = {
            1:0,
            2:0,
            3:0,
            6:2,
            7:2,
        }
        for node, mean_color in mean_colors.items():
            self.assertEqual(self.simple_network.get_mean_c_of_node(node), mean_color, f'node {node} has not mean color of {mean_color}')

        temp_mean_colors = {
                1:[{'time':0, 'color': 0.0}, {'time':1, 'color': 0.0}, {'time':2, 'color': 0.0}, {'time':4, 'color': 0.0}],
                2:[{'time':0, 'color': 0.0}, {'time':3, 'color': 0.0}, {'time':4, 'color': 0.0}],
                3:[{'time':0, 'color': 0.0}, {'time':1, 'color': 0.0}, {'time':2, 'color': 0.0}, {'time':3, 'color': 0.0},  {'time':4, 'color': 0.0}],
                4:[{'time':0, 'color': 0.0}, {'time':4, 'color': 0.0}],
                6:[{'time':2, 'color': 2.0}],
                7:[{'time':2, 'color': 2.0}],
            }
        
        for node, all_mean_color in temp_mean_colors.items():
            for point in all_mean_color:
                self.assertEqual(self.simple_temporal_network.get_mean_c_of_node(node, point['time']), point['color'], f'node {node} has not mean color of {point['color']} at time {point['time']}')
 


    def test_color_count(self):
        abulute_color_count ={
            1:{0: 2},
            2:{0: 3},
            3:{0: 2},
            4:{0: 1},
            5:{},
            6:{2: 1},
            7:{2: 1},
        }
        relativ_color_count = {
            3:{0: 1},
            4:{0: 1},
            1:{0: 1},
            2:{0: 1},
            5:{},
            6:{2: 1},
            7:{2: 1},
        }

        for node, color_count in abulute_color_count.items():
            self.assertEqual(self.simple_network.get_color_count_of_node(node, relativ=False), color_count,f'color count of node {node} is node {color_count}')
        for node, color_count in relativ_color_count.items():
            self.assertEqual(self.simple_network.get_color_count_of_node(node, relativ=True), color_count,f'color count of node {node} is node {color_count}')
        
        # key =tuple(node,time) value = expectet color cuont
        tepm_apsulut_color_coutn = {
            (0, 0) : {} ,(0, 1) : {} ,(0, 2) : {} ,(0, 3) : {} ,(0, 4) : {} ,
            (1, 0) : {0: 2} ,(1, 1) : {0: 1} ,(1, 2) : {0: 1} ,(1, 3) : {} ,(1, 4) : {0: 1} ,
            (2, 0) : {0: 2} ,(2, 1) : {} ,(2, 2) : {} ,(2, 3) : {0: 1} ,(2, 4) : {0: 1} ,
            (3, 0) : {0: 1} ,(3, 1) : {0: 1} ,(3, 2) : {0: 1} ,(3, 3) : {0: 1} ,(3, 4) : {0: 1} ,
            (4, 0) : {0: 1} ,(4, 1) : {} ,(4, 2) : {} ,(4, 3) : {} ,(4, 4) : {0: 1} ,
            (5, 0) : {} ,(5, 1) : {} ,(5, 2) : {} ,(5, 3) : {} ,(5, 4) : {} ,
            (6, 0) : {} ,(6, 1) : {} ,(6, 2) : {2: 1} ,(6, 3) : {} ,(6, 4) : {} ,
            (7, 0) : {} ,(7, 1) : {} ,(7, 2) : {2: 1} ,(7, 3) : {} ,(7, 4) : {} ,}
        
        tepm_relative_color_coutn = {
            (0, 0) : {} ,(0, 1) : {} ,(0, 2) : {} ,(0, 3) : {} ,(0, 4) : {} ,
            (1, 0) : {0: 1.0} ,(1, 1) : {0: 1.0} ,(1, 2) : {0: 1.0} ,(1, 3) : {} ,(1, 4) : {0: 1.0} ,
            (2, 0) : {0: 1.0} ,(2, 1) : {} ,(2, 2) : {} ,(2, 3) : {0: 1.0} ,(2, 4) : {0: 1.0} ,
            (3, 0) : {0: 1.0} ,(3, 1) : {0: 1.0} ,(3, 2) : {0: 1.0} ,(3, 3) : {0: 1.0} ,(3, 4) : {0: 1.0} ,
            (4, 0) : {0: 1.0} ,(4, 1) : {} ,(4, 2) : {} ,(4, 3) : {} ,(4, 4) : {0: 1.0} ,
            (5, 0) : {} ,(5, 1) : {} ,(5, 2) : {} ,(5, 3) : {} ,(5, 4) : {} ,
            (6, 0) : {} ,(6, 1) : {} ,(6, 2) : {2: 1.0} ,(6, 3) : {} ,(6, 4) : {} ,
            (7, 0) : {} ,(7, 1) : {} ,(7, 2) : {2: 1.0} ,(7, 3) : {} ,(7, 4) : {} ,}
        for (node, time), expected in tepm_apsulut_color_coutn.items():
            self.assertEqual(self.simple_temporal_network.get_color_count_of_node(node=node,relativ=False,time=time), expected,f'color count of node {node} is node {color_count}, at time {time}' )
        for (node, time), expected in tepm_relative_color_coutn.items():
            self.assertEqual(self.simple_temporal_network.get_color_count_of_node(node=node,relativ=True,time=time), expected,f'color count of node {node} is node {color_count}, at time {time}' )

        
    def test_get_p_of_node(self):
        p_of_node = {
            1:0.1,
            2:0.1,
            3:0.1,
            4:0.1,
            5:0.1,
            6:0.2,
            7:0.2,
        }
        for node, p in p_of_node.items():
            self.assertEqual(self.simple_network.get_p_of_node(node),p,f'p of node {node} is not {p}')
            self.assertEqual(self.simple_temporal_network.get_p_of_node(node),p, f'p of node {node} is not {p}')
    
    def test_color_change_of_node(self):
        ## TODO 
        ## ein netzwerk testen das hier auch die farbe wechselt
        color_change ={
            1:{'bool':False,'color':0,},
            2:{'bool':False,'color':0,},
            3:{'bool':False,'color':0,},
            4:{'bool':False,'color':0,},
            5:{'bool':False,'color':0,},
            6:{'bool':False,'color':2,},
            7:{'bool':False,'color':2,},
        }
        for node, color_info in color_change.items():
            self.assertEqual(self.simple_network.check_c_change_of_singel_node(node),color_info['bool'],f'Node {node}, did or did not changed color')
            self.assertTrue(self.simple_network.test_if_c_is_color(node,color_info['color']),f'node {node} did not swich to color {color_info['color']}')

        for time in range(0,5):
            for node in range(1,8):
                self.assertEqual(self.simple_temporal_network.check_c_change_of_singel_node(node = node, time = time), False, f'Node {node}, did or did not changed color at time {time}')

    def test_check_cascade(self):
        self.assertEqual(self.simple_network.check_cascade(),[2],'size of cascade wrong')
        self.assertEqual(self.simple_temporal_network.check_cascade(),[2,2,2,2,2],'size of cascade wrong')
        self.test_node_info()

        ## TODO 
        ## test hier ein temporal network
        testNetwork = deepcopy(self.second_network)
        testNetwork.shock_network(1,1)
        self.assertEqual(testNetwork.check_cascade(),[3, 5, 7, 8, 8],'size of cascade wrong')
        self.assertEqual(testNetwork.nodeInfo['c'].mean(),1,'cascade did not happend')

        test_temporal_Network = deepcopy(self.second_temporal_network)
        test_temporal_Network.nodeInfo.iloc[3]['c']= 1.0
        self.assertEqual(test_temporal_Network.check_cascade(),[1, 1, 1, 2, 2, 3, 3, 4, 4] ,'size of cascade wrong')
        self.assertAlmostEqual(test_temporal_Network.nodeInfo['c'].mean(),0.5, 'cascade did not happend')

        
    
    def test_size_of_cascade(self):
        self.assertEqual(self.simple_network.size_of_cascade(),2,'size of cascade wrong')
        self.assertEqual(self.simple_temporal_network.size_of_cascade(),2,'size of cascade wrong')

    def test_shock_network(self):
        for sizeOfShock in range(1,7):
            networkCopy = deepcopy(self.simple_network)
            networkCopy.shock_network(sizeOfShock,5.0)
            num_of_changed_nodes = networkCopy.nodeInfo.c.value_counts()[5.0]
            self.assertEqual(num_of_changed_nodes,sizeOfShock,f'the num of shocked nodes is not {sizeOfShock}')
    
    def test_fehler(self):
        ## das sind dinge die schon mal falschgelaufen sind
        from io import StringIO  
        ## hier gab es mal eine endlosschleife
        n = network()
        n.nodeInfo = pd.read_json(StringIO('{"p":{"0":0.05,"1":0.05,"2":0.05,"3":0.05,"4":0.05,"5":0.05,"6":0.05,"7":0.05,"8":0.05,"9":0.05,"10":0.05,"11":0.05,"12":0.05,"13":0.05,"14":0.05,"15":0.05,"16":0.05,"17":0.05,"18":0.05,"19":0.05,"20":0.05,"21":0.05,"22":0.05,"23":0.05,"24":0.05,"25":0.05,"26":0.05,"27":0.05,"28":0.05,"29":0.05,"30":0.05,"31":0.05,"32":0.05,"33":0.05,"34":0.05,"35":0.05,"36":0.05,"37":0.05,"38":0.05,"39":0.05,"40":0.05,"41":0.05,"42":0.05,"43":0.05,"44":0.05,"45":0.05,"46":0.05,"47":0.05,"48":0.05,"49":0.05,"50":0.05,"51":0.05,"52":0.05,"53":0.05,"54":0.05,"55":0.05,"56":0.05,"57":0.05,"58":0.05,"59":0.05,"60":0.05,"61":0.05,"62":0.05,"63":0.05,"64":0.05,"65":0.05,"66":0.05,"67":0.05,"68":0.05,"69":0.05,"70":0.05,"71":0.05,"72":0.05,"73":0.05,"74":0.05,"75":0.05,"76":0.05,"77":0.05,"78":0.05,"79":0.05,"80":0.05,"81":0.05,"82":0.05,"83":0.05,"84":0.05,"85":0.05,"86":0.05,"87":0.05,"88":0.05,"89":0.05,"90":0.05,"91":0.05,"92":0.05,"93":0.05,"94":0.05,"95":0.05,"96":0.05,"97":0.05,"98":0.05,"99":0.05},"c":{"0":1,"1":0,"2":1,"3":0,"4":1,"5":0,"6":1,"7":1,"8":0,"9":0,"10":1,"11":0,"12":1,"13":0,"14":1,"15":1,"16":1,"17":0,"18":0,"19":0,"20":1,"21":1,"22":0,"23":1,"24":0,"25":1,"26":0,"27":0,"28":0,"29":1,"30":0,"31":1,"32":0,"33":0,"34":0,"35":1,"36":1,"37":0,"38":0,"39":0,"40":1,"41":0,"42":0,"43":0,"44":1,"45":0,"46":1,"47":0,"48":1,"49":0,"50":1,"51":0,"52":0,"53":1,"54":1,"55":1,"56":0,"57":0,"58":0,"59":0,"60":0,"61":1,"62":1,"63":1,"64":0,"65":0,"66":0,"67":0,"68":0,"69":0,"70":1,"71":0,"72":0,"73":1,"74":0,"75":1,"76":0,"77":1,"78":0,"79":1,"80":1,"81":1,"82":0,"83":0,"84":1,"85":1,"86":0,"87":0,"88":0,"89":1,"90":1,"91":0,"92":0,"93":0,"94":1,"95":0,"96":1,"97":1,"98":0,"99":1}}'))
        n.network = pd.read_json(StringIO('{"node1":{"0":0,"1":0,"2":1,"3":1,"4":2,"5":2,"6":4,"7":5,"8":5,"9":6,"10":6,"11":6,"12":6,"13":6,"14":7,"15":7,"16":8,"17":8,"18":8,"19":8,"20":8,"21":8,"22":8,"23":9,"24":9,"25":9,"26":9,"27":11,"28":11,"29":11,"30":12,"31":13,"32":14,"33":15,"34":15,"35":15,"36":16,"37":16,"38":17,"39":19,"40":19,"41":19,"42":20,"43":21,"44":21,"45":22,"46":22,"47":23,"48":25,"49":27,"50":27,"51":27,"52":28,"53":28,"54":29,"55":29,"56":31,"57":31,"58":32,"59":32,"60":32,"61":32,"62":33,"63":33,"64":33,"65":33,"66":35,"67":35,"68":36,"69":36,"70":40,"71":44,"72":44,"73":45,"74":45,"75":46,"76":47,"77":47,"78":50,"79":52,"80":53,"81":56,"82":58,"83":58,"84":59,"85":61,"86":62,"87":63,"88":63,"89":64,"90":66,"91":68,"92":70,"93":73,"94":75,"95":75,"96":77,"97":80,"98":85,"99":85,"100":88,"101":88,"102":89,"103":91},"node2":{"0":20,"1":50,"2":45,"3":86,"4":4,"5":14,"6":99,"7":11,"8":98,"9":25,"10":46,"11":58,"12":70,"13":90,"14":61,"15":79,"16":9,"17":22,"18":28,"19":32,"20":38,"21":68,"22":73,"23":30,"24":37,"25":54,"26":73,"27":24,"28":78,"29":88,"30":15,"31":60,"32":73,"33":68,"34":69,"35":75,"36":55,"37":84,"38":49,"39":51,"40":58,"41":87,"42":62,"43":36,"44":80,"45":65,"46":99,"47":89,"48":55,"49":60,"50":77,"51":93,"52":43,"53":68,"54":48,"55":54,"56":56,"57":63,"58":51,"59":58,"60":66,"61":72,"62":50,"63":63,"64":69,"65":72,"66":56,"67":73,"68":47,"69":94,"70":54,"71":84,"72":99,"73":88,"74":90,"75":48,"76":65,"77":98,"78":59,"79":67,"80":99,"81":74,"82":59,"83":72,"84":64,"85":99,"86":63,"87":69,"88":96,"89":95,"90":91,"91":74,"92":98,"93":96,"94":79,"95":90,"96":97,"97":88,"98":89,"99":97,"100":90,"101":93,"102":90,"103":93},"time":{"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0,"16":0,"17":0,"18":0,"19":0,"20":0,"21":0,"22":0,"23":0,"24":0,"25":0,"26":0,"27":0,"28":0,"29":0,"30":0,"31":0,"32":0,"33":0,"34":0,"35":0,"36":0,"37":0,"38":0,"39":0,"40":0,"41":0,"42":0,"43":0,"44":0,"45":0,"46":0,"47":0,"48":0,"49":0,"50":0,"51":0,"52":0,"53":0,"54":0,"55":0,"56":0,"57":0,"58":0,"59":0,"60":0,"61":0,"62":0,"63":0,"64":0,"65":0,"66":0,"67":0,"68":0,"69":0,"70":0,"71":0,"72":0,"73":0,"74":0,"75":0,"76":0,"77":0,"78":0,"79":0,"80":0,"81":0,"82":0,"83":0,"84":0,"85":0,"86":0,"87":0,"88":0,"89":0,"90":0,"91":0,"92":0,"93":0,"94":0,"95":0,"96":0,"97":0,"98":0,"99":0,"100":0,"101":0,"102":0,"103":0}}'))
        self.assertEqual(n.check_cascade(),[58, 73, 83, 83],'es gab einen fehler ')
        
        ## hier ist mal ein node wieder weiß geworden
        n =network()
        n.nodeInfo = pd.read_json(StringIO('{"p":{"1":0.1,"4":0.1,"2":0.1,"3":0.1},"c":{"1":1,"4":1,"2":0,"3":0}}'))
        n.network= pd.read_json(StringIO('{"node1":{"0":1,"1":1,"2":2,"3":2,"4":3,"5":3,"6":1},"node2":{"0":2,"1":3,"2":1,"3":3,"4":1,"5":2,"6":4},"time":{"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0}}'))
        self.assertFalse (n.check_c_change_of_singel_node(1),'node sollte nicht seien farbe ändern')
    


if __name__ == '__main__':
    unittest.main()
