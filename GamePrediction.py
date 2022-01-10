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
from GraphBuilder import *
from sklearn.metrics import r2_score




if __name__ == '__main__':

    FILE = 'Database_20_21.pkl'

    # Load the database
    print(f'Loading {FILE}... ', end=" ")
    with open(FILE, 'rb') as f:
        Data = dill.load(f)
    print('Loaded')

    # Build graph using whatever weight function
    PointDifferentialGraph = buildGraph(Data, pointDifferentialWeight)


    Prediction = []
    Actual = []
    for Team in tqdm(Data):

        for Game in Team.PlayedGames:

            collectCycles = []
            gameCounter = Counter()
            uid = hashGame(Team.team_name, Game.Opponent, Game.Date.strftime(
                '%m/%d/%Y'))

            # Find all paths between team and opponent of given length
            paths = findSimplePaths(PointDifferentialGraph, Team.team_name,
                                    Game.Opponent,  5, includeSmallerPaths=True)


            for path in paths:

                pathInt = 0
                skip = False

                for game in path:
                    # Make sure that the game we are trying to predict isn't
                    # in the list of games we are using to make the prediction
                    if game[2] == uid:
                        skip = True

                    gameStr = game[2]
                    pathInt += gameStr

                # Also make sure that we don't have the same set of games
                # more than once
                if not gameCounter[str(pathInt)] and not skip:
                    collectCycles.append(path)
                    gameCounter[pathInt] += 1


            x = []

            # For every valid path we sum up the efficency margins
            for path in collectCycles:
                scores = []
                for game in path:
                    scores.append(game[3]['weight'])

                x.append(sum(scores))

            x = np.array(x)

            # Get actual game score
            game = PointDifferentialGraph.edges[Team.team_name,
                                                 Game.Opponent, uid]
            y = game['weight']

            # Average all the predicted margins to get final prediction
            averagePrediction = np.average(x)

            #print(f'Predicted:  {averagePrediction}\t Actual: {y}')
            if not len(x) == 0:
                Prediction.append(averagePrediction)
                Actual.append(y)


    Prediction = np.array(Prediction)
    Actual = np.array(Actual)



    # Logit Curve Fit
    popt, pcov = curve_fit(sigmoid, Prediction, Actual)

    estimated_k, estimated_y0, estimated_h = popt

    coefficient_logit = r2_score(Actual, sigmoid(Prediction, k=estimated_k,
                       y0=estimated_y0, h=estimated_h))


    # Plot the fitted curve
    y_fitted = sigmoid(np.linspace(min(Prediction), max(Prediction), 40), k=estimated_k,
                       y0=estimated_y0, h=estimated_h)


    # Linear Curve Fit
    slope, intercept, r, p_value, std_err = stats.linregress(
        Prediction, Actual)

    coefficient_linear = r2_score(Actual, intercept + slope * Prediction)
f
    plt.scatter(Prediction, Actual, alpha=0.01, label='data')

    plt.plot(np.linspace(min(Prediction), max(Prediction), 40), y_fitted,
             '--', label=f'Logit, r^2 = {coefficient_logit}')

    plt.plot([min(Prediction), max(Prediction)],
             [intercept + slope * min(Prediction), intercept + slope * max(Prediction)], 'k',
             label=f'LSR, r^2 = {coefficient_linear}')


    plt.xlabel('Predicted Margin')
    plt.ylabel('Actual Margin')
    plt.grid()
    plt.legend()
    plt.axis('equal')
    plt.show()



    plt.hist2d(Prediction,  Actual - sigmoid(Prediction, k=estimated_k,
                       y0=estimated_y0, h=estimated_h), bins=(50, 50),
               cmap=plt.cm.Greys, label='Residuals')

    plt.xlabel('Predicted Margin')
    plt.ylabel('Error in Prediction')
    plt.title('Linear Regression Residuals')
    plt.grid()
    plt.axis('equal')
    plt.show()

    plt.hist(Actual - sigmoid(Prediction, k=estimated_k,
                       y0=estimated_y0, h=estimated_h), label='Residuals')
    plt.grid()
    plt.axis('equal')
    plt.show()