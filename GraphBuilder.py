import BuildDataBase
import dill
import GraphTraverse
import matplotlib.pyplot as plt

with open('trest.pkl', 'rb') as f:
	Data = dill.load(f)
	f.close()

school_list = []
for team in Data:
	school_list.append(team.team_name)
	
point_diff_graph = Graph()

for school in school_list:
	point_diff_graph.add_vertex(school)

for team in Data:
	for game in team.PlayedGames:
			
		if game.Opponent in school_list:
			pointdiff = game.pts - game.opp_pts
			
			point_diff_graph.vert_dict[team.team_name].add_neighbor(
			point_diff_graph.vert_dict[game.Opponent],pointdiff)

				
del Data
i=1
outpath = []
outweight = []
print('Begin Traverse')
for v in point_diff_graph:
	outpath,cpath,outweight,cweight = GraphTraverse.search_target(v, v.get_id(), 3, outpath, [], outweight, [])
x = []
y = []
for i in range(0,len(outpath)):
	x.append(sum(outweight[i][0:1]))
	y.append(-outweight[i][2])

fig, ax = plt.subplots()
ax.scatter(x, y)

ax.set_xlabel(r'x', fontsize=15)
ax.set_ylabel(r'y', fontsize=15)
ax.set_title('Volume and percent change')

ax.grid(True)
fig.tight_layout()

plt.show()