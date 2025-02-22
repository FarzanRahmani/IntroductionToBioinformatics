using System;
using System.Collections.Generic;

class OverlapAlignment
{
    public static (int, string, string) PerformOverlapAlignment(string sequence1, string sequence2, int matchScore = 1, int mismatchPenalty = -2, int gapPenalty = -2)
    {
        int length1 = sequence1.Length;
        int length2 = sequence2.Length;

        // Initialize DP table and backtracking direction table
        int[,] scoreMatrix = new int[length1 + 1, length2 + 1];
        char[,] backtrackMatrix = new char[length1 + 1, length2 + 1];

        int maxAlignmentScore = int.MinValue;
        int endPositionSequence1 = 0, endPositionSequence2 = 0;

        // Fill DP table and backtrack table
        for (int i = 1; i <= length1; i++)
        {
            for (int j = 1; j <= length2; j++)
            {
                // Calculate scores for match, insert, and delete
                int match = (sequence1[i - 1] == sequence2[j - 1]) ? scoreMatrix[i - 1, j - 1] + matchScore : scoreMatrix[i - 1, j - 1] + mismatchPenalty;
                int insert = scoreMatrix[i, j - 1] + gapPenalty; // Gap in sequence1
                int delete = scoreMatrix[i - 1, j] + gapPenalty; // Gap in sequence2

                // Determine the maximum score and update backtrack direction
                if (match >= insert && match >= delete)
                {
                    scoreMatrix[i, j] = match;
                    backtrackMatrix[i, j] = 'D'; // Diagonal (match/mismatch)
                }
                else if (insert >= delete)
                {
                    scoreMatrix[i, j] = insert;
                    backtrackMatrix[i, j] = 'L'; // Left (gap in sequence1)
                }
                else
                {
                    scoreMatrix[i, j] = delete;
                    backtrackMatrix[i, j] = 'U'; // Up (gap in sequence2)
                }

                // Update maximum score if at the end of either sequence
                if (i == length1 || j == length2)
                {
                    if (scoreMatrix[i, j] > maxAlignmentScore || (scoreMatrix[i, j] == maxAlignmentScore && (i > endPositionSequence1 || j > endPositionSequence2)))
                    {
                        maxAlignmentScore = scoreMatrix[i, j];
                        endPositionSequence1 = i;
                        endPositionSequence2 = j;
                    }
                }
            }
        }

        // Backtracking to find the optimal alignment
        List<char> alignedSequence1 = new List<char>();
        List<char> alignedSequence2 = new List<char>();
        int currentPosition1 = endPositionSequence1;
        int currentPosition2 = endPositionSequence2;

        while (currentPosition1 > 0 && currentPosition2 > 0)
        {
            if (backtrackMatrix[currentPosition1, currentPosition2] == 'D')
            {
                alignedSequence1.Add(sequence1[currentPosition1 - 1]);
                alignedSequence2.Add(sequence2[currentPosition2 - 1]);
                currentPosition1--;
                currentPosition2--;
            }
            else if (backtrackMatrix[currentPosition1, currentPosition2] == 'L')
            {
                alignedSequence1.Add('-');
                alignedSequence2.Add(sequence2[currentPosition2 - 1]);
                currentPosition2--;
            }
            else // 'U'
            {
                alignedSequence1.Add(sequence1[currentPosition1 - 1]);
                alignedSequence2.Add('-');
                currentPosition1--;
            }
        }

        // Reverse the aligned sequences since we built them from end to start
        alignedSequence1.Reverse();
        alignedSequence2.Reverse();

        string alignedSequence1Str = new string(alignedSequence1.ToArray());
        string alignedSequence2Str = new string(alignedSequence2.ToArray());

        // Trim the aligned sequences to find the actual overlap
        int startIndex = Math.Max(alignedSequence1Str.IndexOf(alignedSequence1Str.Trim('-')), alignedSequence2Str.IndexOf(alignedSequence2Str.Trim('-')));
        int endIndex = Math.Min(alignedSequence1Str.TrimEnd('-').Length, alignedSequence2Str.TrimEnd('-').Length);

        // Extract the final aligned sequences
        alignedSequence1Str = alignedSequence1Str.Substring(startIndex, endIndex - startIndex);
        alignedSequence2Str = alignedSequence2Str.Substring(startIndex, endIndex - startIndex);

        return (maxAlignmentScore, alignedSequence1Str, alignedSequence2Str);
    }

    // Main function to read input and display output
    static void Main(string[] args)
    {
        // Console.Write("Enter first sequence: ");
        string sequence1 = Console.ReadLine().Trim();

        // Console.Write("Enter second sequence: ");
        string sequence2 = Console.ReadLine().Trim();

        // Run overlap alignment
        var (alignmentScore, alignedSequence1, alignedSequence2) = PerformOverlapAlignment(sequence1, sequence2);

        // Display results
        // Console.WriteLine("Max Alignment Score: " + alignmentScore);
        // Console.WriteLine("Aligned Sequence 1: " + alignedSequence1);
        // Console.WriteLine("Aligned Sequence 2: " + alignedSequence2);
        Console.WriteLine(alignmentScore);
        Console.WriteLine(alignedSequence1);
        Console.WriteLine(alignedSequence2);
    }
}
