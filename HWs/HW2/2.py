from collections import Counter, defaultdict

def read_kmers_and_queries():
    """
    Reads the number of k-mers, their length, and the k-mers themselves.
    Also reads the number of queries and the query strings.
    Returns k-mer data and query data as separate outputs.
    """
    # Read n and k values
    num_kmers, k_length = map(int, input().split())
    
    # Read k-mers and count their occurrences
    kmers = [input().strip() for _ in range(num_kmers)]
    kmer_frequencies = Counter(kmers)
    
    # Read number of queries
    num_queries = int(input())
    query_strings = [input().strip() for _ in range(num_queries)]
    
    return k_length, kmer_frequencies, query_strings

def compute_max_repeats(query, k_length, kmer_frequencies):
    """
    Calculates the maximum number of times a query string can repeat,
    given the available k-mers and their counts.
    """
    query_size = len(query)
    
    # If the query is shorter than k, return -1
    if query_size < k_length:
        return -1
    
    # Extract k-mers from the query
    query_sub_kmers = [query[i:i + k_length] for i in range(query_size - k_length + 1)]
    required_kmer_counts = Counter(query_sub_kmers)
    
    # Initialize maximum repetitions and a flag for unrestricted repeats
    max_possible_repeats = float('inf')
    unlimited_repeats = False
    
    # Check each k-mer in the query against available k-mers
    for substring, needed_count in required_kmer_counts.items():
        if substring in kmer_frequencies:
            max_possible_repeats = min(max_possible_repeats, kmer_frequencies[substring] // needed_count)
        else:
            unlimited_repeats = True
            break
    
    # If any k-mer is missing, return -1
    if unlimited_repeats:
        return -1
    
    return max_possible_repeats

def process_queries(k_length, kmer_frequencies, query_strings):
    """
    Processes each query to compute the maximum number of repetitions.
    """
    results = []
    for current_query in query_strings:
        results.append(compute_max_repeats(current_query, k_length, kmer_frequencies))
    return results

def main():
    """
    Main function to handle input, processing, and output.
    """
    # Read inputs
    k_length, kmer_frequencies, query_strings = read_kmers_and_queries()
    
    # Process the queries
    results = process_queries(k_length, kmer_frequencies, query_strings)
    
    # Print the results
    for res in results:
        print(res)

# Run the main function when executed
if __name__ == "__main__":
    main()
