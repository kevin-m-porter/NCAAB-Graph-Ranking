import dill
import matplotlib.pyplot as plt
from tqdm import tqdm
import networkx as nx
from collections import Counter
from scipy import stats
from seaborn import kdeplot
from scipy.optimize import curve_fit
import numpy as np
import hashlib


def sigmoid(x, k, y0, h):
    return h / (1 + np.exp(-k * x)) + y0


def findPaths(G, u, n):
    if n == 0:
        return [[]]
    paths = []
    for edge in G.out_edges(u, data=True, keys=True):
        for path in findPaths(G, edge[1], n - 1):
            paths.append([edge] + path)
    return paths



def findSimplePaths(G, start, end, depth, includeSmallerPaths=False):
    # https://stackoverflow.com/questions/57661314/fastest-way-to-find-all-cycles-of-length-n-containing-a-specified-node-in-a-dire

    paths = []
    if not includeSmallerPaths:
        paths.extend(findPaths(G, start, depth-1))
    else:
        for d in range(1,depth):
            paths.extend(findPaths(G, start, d))

    cycles = []
    for path in paths:
        uids = [x[2] for x in path]
        if path[-1][1] == end and len(set(uids)) == len(uids):
            cycles.append(tuple(path))

    return cycles

def hashGame(Team, Opponent, Date):
    s = "".join(sorted(
        Team + Opponent + Date))
    uid = int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10 \
          ** 8
    return uid

def pointDifferentialWeight(Game):
    weightVar = Game.pts_rate - Game.opp_pts_rate
    inverseWeightVar = -weightVar
    return weightVar, inverseWeightVar


def buildGraph(Data, weightFunc):
    # Initializes a graph, nodes are teams and edges are games, each game will have
    # two edges one for each point of view
    outputGraph = nx.MultiDiGraph()

    # Add all nodes to graph
    for Team in Data:
        outputGraph.add_nodes_from([Team.team_name])

    # Assemble the edges, a key of the date will be added to prevent duplicate
    # games from being added, if there are two games between the same teams
    # on the same date I guess we will miss it... oh well

    for Team in Data:
        for Game in Team.PlayedGames:

            # Hash the team names and date to create a unique int so we can
            uid = hashGame(Team.team_name, Game.Opponent, Game.Date.strftime(
                '%m/%d/%Y'))

            if not outputGraph.has_edge(Team.team_name, Game.Opponent, key=uid):
                weight, invweight = weightFunc(Game)

                outputGraph.add_edge(Team.team_name, Game.Opponent,
                                     key=uid, \
                                     date=Game.Date.strftime('%m/%d/%Y'), \
                                     weight=weight)

                outputGraph.add_edge(Game.Opponent, Team.team_name,
                                     key=uid, \
                                     date=Game.Date.strftime('%m/%d/%Y'), \
                                     weight=invweight)
    return outputGraph

if __name__ == '__main__':

    FILE = 'Database_20_21.pkl'

    # Load the database
    print(f'Loading {FILE}... ', end=" ")
    with open(FILE, 'rb') as f:
        Data = dill.load(f)
    print('Loaded')

    # Build graph using whatever weight function
    PointDifferentialGraph = buildGraph(Data, pointDifferentialWeight)


    collectCycles = []
    gameCounter = Counter()
    for Team in tqdm(Data):
        paths = findSimplePaths(PointDifferentialGraph, Team.team_name,
                           Team.team_name,  3)
        for path in paths:
            pathInt = 0
            for game in path:
                gameStr = game[2]
                pathInt += gameStr

            if not gameCounter[str(pathInt)]:
                collectCycles.append(path)
                gameCounter[pathInt] += 1

    print(f'Length of collectCycles {len(collectCycles)}')

    x = []
    y = []
    z = []

    for path in collectCycles:
        scores = []
        for game in path:
            scores.append(game[3]['weight'])

        x.append(sum(scores[0:-1]))
        y.append(-scores[-1])

    x = np.array(x)
    y = np.array(y)

    popt, pcov = curve_fit(sigmoid, x, y)
    estimated_k, estimated_y0, estimated_h = popt

    print(estimated_k, estimated_y0, estimated_h)

    # Plot the fitted curve
    y_fitted = sigmoid(np.linspace(min(x), max(x), 40), k=estimated_k,
                       y0=estimated_y0, h=estimated_h)

    # Plot everything for illustration

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    print(f'Equation {slope}*x + {intercept}')

    plt.scatter(x, y, alpha=0.01, label='data')

    plt.plot([min(x), max(x)],
             [intercept + slope * min(x), intercept + slope * max(x)], 'k',
             label=f'LSR, r^2 = {r_value}')

    plt.plot(np.linspace(min(x), max(x), 40), y_fitted, '--', label='Logit')
    plt.xlabel('Predicted Margin')
    plt.ylabel('Actual Margin')
    plt.grid()
    plt.legend()
    plt.axis('equal')
    plt.show()

    plt.hist2d(x,  y - (intercept + slope * x), bins=(50, 50),
               cmap=plt.cm.Greys, label='Residuals')
    plt.xlabel('Predicted Margin')
    plt.ylabel('Error in Prediction')
    plt.title('Linear Regression Residuals')
    plt.grid()
    plt.legend()
    plt.axis('equal')
    plt.show()
