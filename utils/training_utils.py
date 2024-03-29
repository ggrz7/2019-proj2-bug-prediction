from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn import tree, svm
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

from utils.misc import indent

T_LOOPS = 70
DEF_TR_DIR = 'res/trainings'

CLASSIFIERS = {
		'Decision Tree': tree.DecisionTreeClassifier(criterion="gini", min_impurity_decrease=0.01, max_depth=2),
		'Naive Bayes Gaussian': GaussianNB(),
		'Linear SVC': svm.LinearSVC(dual=False),
		'MLP Classifier': MLPClassifier(hidden_layer_sizes=[100, 100, 100, 100], activation='tanh', max_iter=300),
		'Random Forest': RandomForestClassifier(criterion="gini", min_impurity_decrease=0.0001, n_estimators=500)
	}


# separate classes, data and buggies
def split_labeled_fv(fv):
	buggies = fv['buggy'].values
	classes = fv['class'].values
	data = fv.drop(['class', 'buggy'], axis=1)
	
	return classes, data, buggies


def print_averages(df):
	averages = df[['accuracy', 'precision', 'recall', 'fscore']].mean(axis=0)

	print(indent('\nPrinting averages:', spaces=10))

	for label, avg in averages.iteritems():
		print(indent('* Average %s: %s' % (label, str(avg)), spaces=14))


def produce_trainings_and_tests(data, labels):
	x_trains, x_tests, y_trains, y_tests, r_num = [], [], [], [], []
	
	r = 0
	for i in range(0, T_LOOPS):
		x_train, x_test, y_train, y_test = train_test_split(data, labels, train_size=0.8, test_size=0.2, random_state=i)
		
		x_trains.append(x_train)
		x_tests.append(x_test)
		y_trains.append(y_train)
		y_tests.append(y_test)
		r_num.append(r)
		r += 1
	
	return {'x_trains': x_trains, 'x_tests': x_tests, 'y_trains': y_trains, 'y_tests': y_tests}, r_num


def make_plot(x, data, title, folder):
	plt.figure(figsize=(26, 10))
	plt.title(title)
	
	plt.xlabel('Run')
	plt.ylabel('Metrics')
	for col in data.columns:
		plt.plot(x, data[col].values,	marker='o', markersize=4, label=col)
	
	plt.legend()
	plt.grid(True)
	path = folder + '/' + title.replace(" ", "") + '.png'
	plt.savefig(path)
	plt.clf()
	
	print(indent('\nPlot saved to "%s"' % path, spaces=10))


def get_prec_recall_fscore(y_test, p_labels):
	prec, rec, f1, sup = precision_recall_fscore_support(y_test, p_labels, average='binary')
	
	return prec, rec, f1
