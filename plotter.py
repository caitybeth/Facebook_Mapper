import cPickle as pic
import time
import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

def test():
	p=plotter()
	p.plotAll()
	f=file('plot_ids.txt','r')
	names=f.readlines()
	f.close()
	n=[]
	names=list(set(names))
	for i in names:
                x=i
                try:
                        x.replace('\n','')
                except:
                        pass
                try:
                        x.replace('\r','')
                except:
                        pass
                n.append(x)
        for i in n:
                for j in n:
                        p.plotReln(i,j)



class plotter:
	def __init__(self):
		self.__setup__()
	def __setup__(self):
		self.__g__=nx.Graph()
		self.__nodes__=self.__getFiles__()
		here=os.getcwd()
		
		for n in self.__nodes__:
			path=os.path.join(here,'data',n)
			f=file(path,'r')
			data=pic.load(f)
			f.close()
			self.__g__.add_node(n,{'name':data['name']})#friends field is list of tuples
			gen=(i for i in data['friends'])
			for fr in gen:
				self.__g__.add_node(fr[0],{'name':fr[1]})
				self.__g__.add_edge(n,fr[0])

	def __getFiles__(self):
		here=os.getcwd()
		path=os.path.join(here,'data')
		file_lst=os.listdir(path)
		return file_lst
	def plotAll(self):
		self.__setup__()
		print 'drawing'
		pos=nx.layout.random_layout(self.__g__)
		print 'positions obtained'
		nx.draw_networkx_nodes(self.__g__,pos,nodelist=self.__g__.nodes(),node_size=10,node_color='r',node_shape='o',alpha=0.2)
		print 'nodes drawn, drawing edges'
		nx.draw_networkx_edges(self.__g__,pos,edgelist=self.__g__.edges(),width=1,edge_color='k',style='solid',alpha=0.1)
		print 'edges drawn, rendering '
		plt.axis('off')
		details='Profiles: '+str(len(self.__g__.nodes()))+' Connections: '+str(len(self.__g__.edges()))
		plt.figtext(0.2,0.8,details)
		print 'saving'
		fig=plt.gcf()
		fig.set_size_inches(20,20)
		plt.savefig(os.path.join(os.getcwd(),'plots','complete_plot.png'),dpi=100)
		print 'showing'
		#plt.show()
		print 'Complete'
		plt.close()

	def plotReln(self,a,b):
		self.__setup__()
		try:
			short=nx.shortest_path(self.__g__,a,b)
		except Exception as err:
			print err
			print 'Plot not completed'
			return
		else:
			print 'shortest path exists'
			nodes=short
			s_path=''
			for i in nodes:
				print i,'->',
				try:
					if i!=nodes[-1]:
						s_path+=str(self.__g__.node[i]['name'])+'->'
					else:
						s_path+=str(self.__g__.node[i]['name'])
				except:
					if i!=nodes[-1]:
						s_path+=i+'->'
					else:
						s_path+=i
			del short
			s_path=s_path.encode('string-escape')
			print s_path
			edges=[]
			print 'generating relevent edges'
			for i in xrange(len(nodes)-1):
				edges.append((nodes[i],nodes[i+1]))
			print 'computing position of nodes'
			
			pos=nx.layout.random_layout(self.__g__)

			nx.draw_networkx_nodes(self.__g__,pos,nodelist=[i for i in self.__g__.nodes() if i not in nodes],node_size=10,node_color='b',node_shape='o',alpha=.1)
			nx.draw_networkx_edges(self.__g__,pos,edgelist=[i for i in self.__g__.edges() if i not in edges],width=1,edge_color='g',style='solid',alpha=0.001)

			nx.draw_networkx_edges(self.__g__,pos,edgelist=edges,width=5,edge_color='r',style='solid',alpha=1)
			nx.draw_networkx_nodes(self.__g__,pos,nodelist=nodes,node_size=100,node_color='r',node_shape='o',alpha=1)
			plt.axis('off')

			plt.figtext(0.2,0.8,s_path)
			print 'saving figure'
			fig=plt.gcf()
			fig.set_size_inches(20,20)
			plt.savefig(os.path.join(os.getcwd(),'plots','relation-'+a+'-'+b+'.png'),dpi=100)
			#plt.show()
			print 'complete'
			plt.close()
			


if __name__=='__main__':
	test()
