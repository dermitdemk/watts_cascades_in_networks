import unittest
from network import network
import pandas as pd

class TestNetwork(unittest.TestCase):
    
    @classmethod
    def setUp(self):
        self.simpleNetwork = network()
        for i in range(1,6):
            self.simpleNetwork.add_node(info_as_list=[i,0.1,0])
        for i in range(6,8):
            self.simpleNetwork.add_node(info_as_list=[i,0.2,2])
        self.simpleNetwork.add_connection([1,2])
        self.simpleNetwork.add_connection([1,3])
        self.simpleNetwork.add_connection([2,4])
        self.simpleNetwork.add_connection([3,2])
        self.simpleNetwork.add_connection([6,7])
        
        pass
    
    def test_node_info(self):
        
        self.assertEqual(self.simpleNetwork.nodeInfo.to_dict(), {'nodeId': {0: 1.0, 1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0, 6: 7.0},
                                                        'p': {0: 0.1, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.2, 6: 0.2},
                                                        'c': {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 2.0, 6: 2.0}}, 
                        'adding_node')
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
            self.assertEqual(
                self.simpleNetwork.find_all_conection_of_node(node),
                expected,
                f'Connections for node {node} are wrong.'
            )

    
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
            self.assertEqual(self.simpleNetwork.check_for_path(node),expected,  f'Path for node {node} is wrong.')


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
            self.assertTrue(self.simpleNetwork.test_if_c_is_color(node, color),f'color for {node} is not {color}')
            
            color2 = color*2
            self.simpleNetwork.nodeInfo.iloc[node-1]['c'] = color2
            self.assertTrue(self.simpleNetwork.test_if_c_is_color(node,color2),f'color for {node} is not {color2}')
            
            self.simpleNetwork.update_node_c(node,color)
            self.assertTrue(self.simpleNetwork.test_if_c_is_color(node, color),f'color for {node} is not {color}')
    
    def test_mean_color(self):
        mean_colors = {
            1:0,
            2:0,
            3:0,
            6:2,
            7:2,
        }
        for node, mean_color in mean_colors.items():
            self.assertEqual(self.simpleNetwork.get_mean_c_of_node(node), mean_color, f'node {node} has not mean color of {mean_color}')


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
            self.assertEqual(self.simpleNetwork.get_color_count_of_node(node, relativ=False), color_count,f'color count of node {node} is node {color_count}')
        for node, color_count in relativ_color_count.items():
            self.assertEqual(self.simpleNetwork.get_color_count_of_node(node, relativ=True), color_count,f'color count of node {node} is node {color_count}')
        
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
            self.assertEqual(self.simpleNetwork.get_p_of_node(node),p,f'p of node {node} is not {p}')
    
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
            self.assertEqual(self.simpleNetwork.check_c_change_of_singel_node(node),color_info['bool'],f'Node {node}, did or did not changed color')
            self.assertTrue(self.simpleNetwork.test_if_c_is_color(node,color_info['color']),f'node {node} did not swich to color {color_info['color']}')

    def test_check_cascade(self):
        self.assertEqual(self.simpleNetwork.check_cascade(),[2],'size of cascade wrong')
        self.test_node_info()
    
    def test_size_of_cascade(self):
        self.assertEqual(self.simpleNetwork.size_of_cascade(),2,'size of cascade wrong')

    def test_shock_network(self):
        from copy import deepcopy
        for sizeOfShock in range(1,7):
            networkCopy = deepcopy(self.simpleNetwork)
            networkCopy.shock_network(sizeOfShock,5.0)
            num_of_changed_nodes = networkCopy.nodeInfo.c.value_counts()[5.0]
            self.assertEqual(num_of_changed_nodes,sizeOfShock,f'the num of shocked nodes is not {sizeOfShock}')
        
    


if __name__ == '__main__':
    unittest.main()
