#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <limits>
#include <cmath> // Include this header for the round function
using namespace std;

// Function to calculate total distances for each row in the distance matrix
vector<double> calculateTotalDistances(const vector<vector<double>>& distanceMatrix) {
    vector<double> totalDistances(distanceMatrix.size(), 0.0);
    for (size_t i = 0; i < distanceMatrix.size(); i++) {
        for (size_t j = 0; j < distanceMatrix[i].size(); j++) {
            totalDistances[i] += distanceMatrix[i][j];
        }
    }
    return totalDistances;
}

// Function to construct the Neighbor-Joining matrix
vector<vector<double>> constructNJMatrix(const vector<vector<double>>& distanceMatrix, const vector<double>& totalDistances) {
    size_t n = distanceMatrix.size();
    vector<vector<double>> njMatrix(n, vector<double>(n, 0.0));
    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            if (i != j) {
                njMatrix[i][j] = (n - 2) * distanceMatrix[i][j] - totalDistances[i] - totalDistances[j];
            } else {
                njMatrix[i][j] = numeric_limits<double>::infinity();
            }
        }
    }
    return njMatrix;
}

// Function to find the indices of the minimum non-diagonal element in the NJ matrix
pair<int, int> findMinNonDiagonal(const vector<vector<double>>& njMatrix) {
    double minValue = numeric_limits<double>::infinity();
    pair<int, int> minIndices = {-1, -1};
    for (size_t i = 0; i < njMatrix.size(); i++) {
        for (size_t j = 0; j < njMatrix[i].size(); j++) {
            if (i != j && njMatrix[i][j] < minValue) {
                minValue = njMatrix[i][j];
                minIndices = {static_cast<int>(i), static_cast<int>(j)};
            }
        }
    }
    return minIndices;
}

// Function to update the distance matrix with a new row/column
vector<vector<double>> updateDistanceMatrix(const vector<vector<double>>& distanceMatrix, int idx_i, int idx_j) {
    size_t n = distanceMatrix.size();
    vector<vector<double>> newMatrix;
    vector<double> newRow;

    for (size_t k = 0; k < n; k++) {
        if (k != static_cast<size_t>(idx_i) && k != static_cast<size_t>(idx_j)) {
            double newDistance = 0.5 * (distanceMatrix[idx_i][k] + distanceMatrix[idx_j][k] - distanceMatrix[idx_i][idx_j]);
            newRow.push_back(newDistance);
        }
    }

    for (size_t x = 0; x < n; x++) {
        if (x != static_cast<size_t>(idx_i) && x != static_cast<size_t>(idx_j)) {
            vector<double> updatedRow;
            for (size_t y = 0; y < n; y++) {
                if (y != static_cast<size_t>(idx_i) && y != static_cast<size_t>(idx_j)) {
                    updatedRow.push_back(distanceMatrix[x][y]);
                }
            }
            newMatrix.push_back(updatedRow);
        }
    }

    newMatrix.push_back(newRow);
    for (size_t i = 0; i < newMatrix.size(); i++) {
        if (i < newRow.size()) {
            newMatrix[i].push_back(newRow[i]);
        } else {
            newMatrix[i].push_back(0.0);
        }
    }
    return newMatrix;
}

// Neighbor-Joining algorithm implementation
vector<tuple<int, int, double>> neighborJoining(vector<vector<double>> distanceMatrix, int numLeaves) {
    vector<tuple<int, int, double>> treeEdges;
    vector<int> activeNodes(numLeaves);
    for (int i = 0; i < numLeaves; i++) {
        activeNodes[i] = i;
    }
    int nextInternalNode = numLeaves;

    while (distanceMatrix.size() > 2) {
        vector<double> totalDistances = calculateTotalDistances(distanceMatrix);
        vector<vector<double>> njMatrix = constructNJMatrix(distanceMatrix, totalDistances);
        pair<int, int> minIndices = findMinNonDiagonal(njMatrix);
        int i = minIndices.first, j = minIndices.second;

        double delta = (totalDistances[i] - totalDistances[j]) / (distanceMatrix.size() - 2);
        double limbLength_i = 0.5 * (distanceMatrix[i][j] + delta);
        double limbLength_j = 0.5 * (distanceMatrix[i][j] - delta);

        treeEdges.emplace_back(activeNodes[i], nextInternalNode, round(limbLength_i * 1000) / 1000);
        treeEdges.emplace_back(nextInternalNode, activeNodes[i], round(limbLength_i * 1000) / 1000);
        treeEdges.emplace_back(activeNodes[j], nextInternalNode, round(limbLength_j * 1000) / 1000);
        treeEdges.emplace_back(nextInternalNode, activeNodes[j], round(limbLength_j * 1000) / 1000);

        distanceMatrix = updateDistanceMatrix(distanceMatrix, i, j);

        activeNodes.push_back(nextInternalNode);
        activeNodes.erase(activeNodes.begin() + max(i, j));
        activeNodes.erase(activeNodes.begin() + min(i, j));
        nextInternalNode++;
    }

    treeEdges.emplace_back(activeNodes[0], activeNodes[1], round(distanceMatrix[0][1] * 1000) / 1000);
    treeEdges.emplace_back(activeNodes[1], activeNodes[0], round(distanceMatrix[0][1] * 1000) / 1000);

    return treeEdges;
}

// Format the adjacency list for output
void printTreeEdges(const vector<tuple<int, int, double>>& treeEdges) {
    vector<tuple<int, int, double>> sortedEdges = treeEdges;
    sort(sortedEdges.begin(), sortedEdges.end());
    for (const auto& edge : sortedEdges) {
        cout << get<0>(edge) << "->" << get<1>(edge) << ":" << fixed << setprecision(3) << get<2>(edge) << endl;
    }
}

int main() {
    int n;
    cout << "Enter the number of leaves: ";
    cin >> n;
    vector<vector<double>> distanceMatrix(n, vector<double>(n));
    cout << "Enter the distance matrix:" << endl;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> distanceMatrix[i][j];
        }
    }

    vector<tuple<int, int, double>> resultingTree = neighborJoining(distanceMatrix, n);
    printTreeEdges(resultingTree);

    return 0;
}

// g++ -o 1 1.cpp
// ./1
