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

        
        pass
    
    def test_node_info(self):
        
        self.assertEqual(self.simple_network.nodeInfo.to_dict(), {'nodeId': {0: 1.0, 1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0, 6: 7.0},
                                                        'p': {0: 0.1, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.2, 6: 0.2},
                                                        'c': {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 2.0, 6: 2.0}}, 
                        'node info is not as expecdet')
        self.assertEqual(self.simple_temporal_network.nodeInfo.to_dict(), {'nodeId': {0: 1.0, 1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0, 6: 7.0},
                                                        'p': {0: 0.1, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.2, 6: 0.2},
                                                        'c': {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 2.0, 6: 2.0}}, 
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
    
    def test_color_change_of_node(self):
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

    def test_check_cascade(self):
        self.assertEqual(self.simple_network.check_cascade(),[2],'size of cascade wrong')
        self.test_node_info()

        testNetwork = deepcopy(self.second_network)
        testNetwork.shock_network(1,1)
        self.assertEqual(testNetwork.check_cascade(),[3, 5, 7, 8, 8],'size of cascade wrong')
        self.assertEqual(testNetwork.nodeInfo['c'].mean(),1,'cascade did not happend')

        
    
    def test_size_of_cascade(self):
        self.assertEqual(self.simple_network.size_of_cascade(),2,'size of cascade wrong')

    def test_shock_network(self):
        for sizeOfShock in range(1,7):
            networkCopy = deepcopy(self.simple_network)
            networkCopy.shock_network(sizeOfShock,5.0)
            num_of_changed_nodes = networkCopy.nodeInfo.c.value_counts()[5.0]
            self.assertEqual(num_of_changed_nodes,sizeOfShock,f'the num of shocked nodes is not {sizeOfShock}')
        
    


if __name__ == '__main__':
    unittest.main()
