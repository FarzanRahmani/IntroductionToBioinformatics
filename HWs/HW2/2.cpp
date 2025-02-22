#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <algorithm>
#include <climits> // For INT_MAX

using namespace std;

// Function to read k-mers and queries
void readKmersAndQueries(int &kLength, unordered_map<string, int> &kmerFrequencies, vector<string> &queries) {
    int numKmers, numQueries;
    
    // Read number of k-mers and their length
    cin >> numKmers >> kLength;
    
    // Read k-mers and count their occurrences
    for (int i = 0; i < numKmers; ++i) {
        string kmer;
        cin >> kmer;
        kmerFrequencies[kmer]++;
    }
    
    // Read number of queries
    cin >> numQueries;
    
    // Read query strings
    for (int i = 0; i < numQueries; ++i) {
        string query;
        cin >> query;
        queries.push_back(query);
    }
}

// Function to calculate the maximum repetitions for a single query
int computeMaxRepeats(const string &query, int kLength, const unordered_map<string, int> &kmerFrequencies) {
    int querySize = query.size();
    
    // If the query is shorter than k, return -1
    if (querySize < kLength) {
        return -1;
    }
    
    // Extract k-mers from the query and count their occurrences
    unordered_map<string, int> requiredKmerCounts;
    for (int i = 0; i <= querySize - kLength; ++i) {
        string subKmer = query.substr(i, kLength);
        requiredKmerCounts[subKmer]++;
    }
    
    // Calculate the maximum repetitions
    int maxPossibleRepeats = INT_MAX;
    for (const auto &entry : requiredKmerCounts) {
        const string &subKmer = entry.first;
        int neededCount = entry.second;
        
        // If k-mer is not available, the query cannot be repeated
        if (kmerFrequencies.find(subKmer) == kmerFrequencies.end()) {
            return -1;
        }
        
        // Calculate the maximum repetitions for this k-mer
        maxPossibleRepeats = min(maxPossibleRepeats, kmerFrequencies.at(subKmer) / neededCount);
    }
    
    return maxPossibleRepeats;
}

// Function to process all queries and compute their results
vector<int> processQueries(int kLength, const unordered_map<string, int> &kmerFrequencies, const vector<string> &queries) {
    vector<int> results;
    for (const string &query : queries) {
        results.push_back(computeMaxRepeats(query, kLength, kmerFrequencies));
    }
    return results;
}

// Main function
int main() {
    int kLength;
    unordered_map<string, int> kmerFrequencies;
    vector<string> queries;
    
    // Read inputs
    readKmersAndQueries(kLength, kmerFrequencies, queries);
    
    // Process queries
    vector<int> results = processQueries(kLength, kmerFrequencies, queries);
    
    // Print results
    for (int result : results) {
        cout << result << endl;
    }
    
    return 0;
}

// g++ -o 2 2.cpp
// ./2
