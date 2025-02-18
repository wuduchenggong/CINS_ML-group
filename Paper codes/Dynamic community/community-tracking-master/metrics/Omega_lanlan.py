from __future__ import division
from itertools import combinations
from collections import Counter
from sklearn import metrics



class Omega:
    def __init__(self, comms1, comms2):
        # self.nodes1 = self.get_node_assignment(comms1)
        # self.nodes2 = self.get_node_assignment(comms2)
        # self.nodes = list(set().union([node for i, com in comms2.items() for node in com],
        #                               [node for i, com in comms1.items() for node in com]))
        # J, K, N, obs, tuples1, tuples2 = self.observed()
        # exp = self.expected(J, K, N, tuples1, tuples2)
        # # self.omega_score = self.calc_omega(obs, exp)
        # self.omega_score = metrics.adjusted_rand_score(labels_true, labels_pred)
        # print "obs = ", obs
        # print "exp = ", exp
        # print "Omega = ", self.omega_score
        self.omega_score = self.ari_score(comms1, comms2)

    def get_node_assignment(self, comms):
        """
        returns a dictionary with node-cluster assignments of the form {node_id :[cluster1, cluster_3]}
        :param comms:
        :return:
        """
        nodes = {}
        for i, com in comms.items():
            for node in com:
                try:
                    nodes[node].append(i)
                except KeyError:
                    nodes[node] = [i]
        return nodes

    def num_of_common_clusters(self, u, v, nodes_dict):
        """
        return the number of clusters in which the pair u,v appears in the
        :param u:
        :param v:
        :param nodes_dict:
        :return:
        """
        try:
            _sum = len(set(nodes_dict[u]) & set(nodes_dict[v]))
        except KeyError:
            _sum = 0
        return _sum

    def observed(self):
        N = 0
        tuples1 = {}
        J = 0
        for u, v in combinations(self.nodes, 2):
            N += 1
            n = self.num_of_common_clusters(u, v, self.nodes1)
            tuples1[(u, v)] = self.num_of_common_clusters(u, v, self.nodes1)
            J = n if n > J else J
        tuples2 = {}
        K = 0
        for u, v in combinations(self.nodes, 2):
            n = self.num_of_common_clusters(u, v, self.nodes2)
            tuples2[(u, v)] = self.num_of_common_clusters(u, v, self.nodes2)
            K = n if n > K else K
        obs = 0
        A = {j: 0 for j in range(min(J, K)+1)}
        for (u, v), n in tuples1.items():
            try:
                if n == tuples2[(u, v)]:
                    A[n] += 1
            except KeyError:
                pass
        obs = sum(A[j] for j in range(min(J, K)+1))/N
        return J, K, N, obs, tuples1, tuples2

    def expected(self, J, K, N, tuples1, tuples2):
        N1 = Counter(tuples1.values())
        N2 = Counter(tuples2.values())
        exp = sum((N1[j]*N2[j]) for j in range(min(J, K)+1))/(N**2)
        return exp

    def calc_omega(self, obs, exp):
        if exp==obs==1:
            return 1.0
        else:
            return (obs-exp)/(1-exp)

    def node_comms(self, comms):
        result = {}
        for c in comms.keys():
            for node in comms[c]:
                result[node] = c
        return result

    def ari_score(self, gt, pr):
        # gt = {cid: node_time}
        node1 = self.node_comms(gt)
        node2 = self.node_comms(pr)
        nodes = [node for node in node1.keys()]
        list1 = []  # gt
        list2 = []  # pr
        for node in nodes:
            list1.append(node1[node])
            list2.append(node2[node])
        ari = metrics.adjusted_rand_score(list1, list2)
        return ari

def readlabel(file):
        labels_dic = {}
        with open(file, 'r') as fp:
            for line in fp.readlines():
                lines = line.split(':')
                cid = float(lines[0].split()[-1])
                # print(cid)
                labels_dic[cid] = []
                temp1 = lines[-1].split(']')[0].split('[')[-1]
                nodes = temp1.split()
                for node in nodes:
                    # print(node)
                    if len(node) > 1:  # is string of node's name
                        labels_dic[cid].append(node.split(',')[0])
        return labels_dic

if __name__ == '__main__':
    # comms1 = {1: [5, 6, 7], 2: [3, 4, 5], 3: [6, 7, 8]}
    # comms2 = {1: [5, 6, 7], 2: [3, 4, 6], 3: [6, 7, 8]}
    # comms3 = {1: [5, 6, 7], 2: [6, 7, 8], 3: [3, 4, 5]}
    # comms4 = {0: ['1-t0', '2-t0', '3-t0', '4-t0', '1-t1', '2-t1',  '3-t1','4-t1', '1-t2','2-t2','3-t2','4-t2'],
    #           1: ['11-t1', '12-t1', '13-t1'],
    #           2: ['5-t2', '6-t2', '7-t2', '5-t0', '6-t0', '7-t0']}
    # comms5 = {1: ['11-t1', '12-t1', '13-t1'],
    #           2: ['1-t0', '2-t0', '3-t0', '4-t0', '1-t1', '2-t1',  '3-t1','4-t1', '1-t2','2-t2','3-t2','4-t2'],
    #           3: ['5-t2', '6-t2', '7-t2', '5-t0', '6-t0', '7-t0']}
    # comms6 ={0: ["1-t0", "2-t0", "3-t0", "4-t0","1-t1", "2-t1", "3-t1", "4-t1", "1-t2", "2-t2", "3-t2",
    #                       "4-t2"],
	# 		 1: ["5-t0", "6-t0", "7-t0", "8-t0", "5-t2", "6-t2", "7-t2", "8-t2"]}
    # omega = Omega(comms6, comms6)
    # print(omega.nodes1)
    # print(omega.omega_score)
    import os

    # path = 'E:/DATASet/node classify/karate/communities'
    # path = 'E:/DATASet/node classify/cora/communities'
    path = 'E:/DATASet/node classify/email-EuAll/communities'

    ground_truth = readlabel(os.path.join(path, 'ground_truth.label'))
    print('******************** k_clique **********************')
    for k in range(2, 10):
        print(k)
        file_non = os.path.join(path, str(k) + '_clique.label')
        file_sr = os.path.join(path, str(k) + '_clique_surep.label')
        print('method\tomega_score')
        try:
            comms_non = readlabel(file_non)
            b_non = Omega(ground_truth, comms_non)
            print('before\t', "{0:.4f}".format(b_non.omega_score))
        except:
            print(file_non + ' is not existent.')
        try:
            comms_sr = readlabel(file_sr)
            b_sr = Omega(ground_truth, comms_sr)
            print('after\t', "{0:.4f}".format(b_sr.omega_score))
        except:
            print(file_sr + ' is not existent.')


    print('\n******************** greedy_modularity **********************')
    file_non = os.path.join(path, 'greedy_modularity.label')
    file_sr = os.path.join(path, 'greedy_modularity_surep.label')
    print('method\tomega_score')
    try:
        comms_non = readlabel(file_non)
        b_non = Omega(ground_truth, comms_non)
        print('before\t', "{0:.4f}".format(b_non.omega_score))
    except:
        print(file_non + ' is not existent.')
    try:
        comms_sr = readlabel(file_sr)
        b_sr = Omega(ground_truth, comms_sr)
        print('after\t', "{0:.4f}".format(b_sr.omega_score))
    except:
        print(file_sr + ' is not existent.')

    print('\n******************** label_propagation **********************')
    file_non = os.path.join(path, 'label_propagation.label')
    file_sr = os.path.join(path, 'label_propagation_surep.label')
    print('method\tomega_score')
    try:
        comms_non = readlabel(file_non)
        b_non = Omega(ground_truth, comms_non)
        print('before\t', "{0:.4f}".format(b_non.omega_score))
    except:
        print(file_non + ' is not existent.')
    try:
        comms_sr = readlabel(file_sr)
        b_sr = Omega(ground_truth, comms_sr)
        print('after\t', "{0:.4f}".format(b_sr.omega_score))
    except:
        print(file_sr + ' is not existent.')

    print('\n******************** girvan_newman **********************')
    file_non = os.path.join(path, 'girvan_newman.label')
    file_sr = os.path.join(path, 'girvan_newman_surep.label')
    print('method\tomega_score')
    try:
        comms_non = readlabel(file_non)
        b_non = Omega(ground_truth, comms_non)
        print('before\t', "{0:.4f}".format(b_non.omega_score))
    except:
        print(file_non + ' is not existent.')
    try:
        comms_sr = readlabel(file_sr)
        b_sr = Omega(ground_truth, comms_sr)
        print('after\t', "{0:.4f}".format(b_sr.omega_score))
    except:
        print(file_sr + ' is not existent.')

    print('\n******************** asyn_fluidc **********************')
    file_non = os.path.join(path, 'asyn_fluidc.label')
    file_sr = os.path.join(path, 'asyn_fluidc_surep.label')
    print('method\tomega_score')
    try:
        comms_non = readlabel(file_non)
        b_non = Omega(ground_truth, comms_non)
        print('before\t', "{0:.4f}".format(b_non.omega_score))
    except:
        print(file_non + ' is not existent.')
    try:
        comms_sr = readlabel(file_sr)
        b_sr = Omega(ground_truth, comms_sr)
        print('after\t', "{0:.4f}".format(b_sr.omega_score))
    except:
        print(file_sr + ' is not existent.')
