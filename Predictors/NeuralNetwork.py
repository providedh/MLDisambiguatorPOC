import itertools
from datetime import datetime

from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

from DataProcessing import PairsProcessor
from sklearn.metrics import classification_report, accuracy_score, make_scorer, confusion_matrix


def log(text: str):
    print(f"{datetime.now().strftime('%H:%M:%S')}: {text}")


class NeuralNetwork:
    def _load_pairs_w_features(self):
        log("Loading data")
        negative = PairsProcessor.load_pairs("../data/with_features_n.json")
        positive = PairsProcessor.load_pairs("../data/with_features_p.json")

        self.with_features = itertools.chain(negative, positive)

    def _convert_to_data_and_labels(self):
        data, labels = [], []
        for pair, features in self.with_features:
            data.append(features)
            labels.append(pair[2])

        self._training_data = data, labels
        return data, labels

    @staticmethod
    def classification_report_with_accuracy_score(y_true, y_pred):
        print(classification_report(y_true, y_pred))  # print classification report
        cm = confusion_matrix(y_true, y_pred)
        print(cm)
        (tn, fp), (fn, tp) = cm
        print(f"Czułość: {tp / (tp + fn)}")
        print(f"Swoistość: {tn / (tn + fp)}")

        return accuracy_score(y_true, y_pred)  # return accuracy score

    def _train_network(self):
        log("Preparing")
        dataset, labels = self._convert_to_data_and_labels()

        log("Scaling")
        scaler = StandardScaler()
        scaler.fit(dataset)

        dataset = scaler.transform(dataset)

        clf = MLPClassifier(hidden_layer_sizes=(15, 7, 2), max_iter=5000)
        log("N-cross validation")
        scores = cross_val_score(clf, dataset, labels, cv=6, n_jobs=-1,
                                 scoring=make_scorer(self.classification_report_with_accuracy_score))
        print(scores)

    def prepare_and_train(self):
        self._load_pairs_w_features()
        self._train_network()


if __name__ == "__main__":
    n = NeuralNetwork()
    n.prepare_and_train()
