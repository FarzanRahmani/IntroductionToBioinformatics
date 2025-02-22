using System;
using System.Collections.Generic;
public struct T
{
    public int start;
    public int end;

    public T(int start, int end)
    {
        this.start = start;
        this.end = end;
    }
}
public class SuffixArrayMatching
{
    public static T findOccurrences(String pattern, String text, int[] suffixArray) // PatternMatchinfWithSuffixArray
    {
        // List<int> result = new List<int>(text.Length);
        // write your code here 
        int minIdx = 0;
        int maxIdx = text.Length; // -1
        while (minIdx < maxIdx)
        {
            int midIdx = (minIdx + maxIdx) / 2;
            // if (pattern > text.Substring(midIdx))
            int suffix = suffixArray[midIdx];
            int i = 0;
            while (i < pattern.Length && suffix + i < text.Length)
            {
                if (pattern[i] > text[suffix + i])
                {
                    minIdx = midIdx + 1;
                    break;
                }
                else if (pattern[i] < text[suffix + i])
                {
                    maxIdx = midIdx;
                    break;
                }
                i++;
                if (i == pattern.Length)
                    maxIdx = midIdx;
                else if (suffix + i == text.Length)
                    minIdx = midIdx + 1;
            }
        }
        int start = minIdx;
        maxIdx = text.Length;
        while (minIdx < maxIdx)
        {
            int midIdx = (minIdx + maxIdx) / 2;
            // if (pattern > text.Substring(midIdx))
            int suffix = suffixArray[midIdx];
            int i = 0;
            while (i < pattern.Length && suffix + i < text.Length)
            {
                if (pattern[i] < text[suffix + i])
                {
                    maxIdx = midIdx;
                    break;
                }
                i++;
                if (i == pattern.Length && i <= text.Length - suffix) // if p is a prefix of the suffix, we treat p >= suffix
                {
                    minIdx = midIdx + 1;
                }
            }
        }
        int end = maxIdx - 1;
        // if (start > end)
        // {
        //     return result;
        // }
        // else
        // {
        //     for (int i = start; i <= end; i++)
        //     {
        //         result.Add(suffixArray[i]);
        //     }
        //     return result;
        // }
        return new T(start, end);
    }

    static public void Main(String[] args)
    {
        // String text = Console.ReadLine() + "$";
        // int[] suffixArray = computeSuffixArray(text);
        // int patternCount = int.Parse(Console.ReadLine());
        // bool[] occurs = new bool[text.Length];
        // string[] patterns = Console.ReadLine().Split();
        // foreach (var p in patterns)
        // {
        //     List<int> occurrences = findOccurrences(p, text, suffixArray);
        //     foreach (int x in occurrences)
        //     {
        //         occurs[x] = true;
        //     }
        // }
        // for (int i = 0; i < occurs.Length; i++)
        // {
        //     if (occurs[i])
        //         Console.Write(i + " ");
        // }
        // System.Console.WriteLine();
        // string[] patterns = Console.ReadLine().Split();
        // HashSet<int> ans = new HashSet<int>(text.Length);
        // foreach (var p in patterns)
        // {
        //     List<int> occurrences = findOccurrences(p, text, suffixArray);
        //     foreach (int x in occurrences)
        //     {
        //         ans.Add(x);
        //     }
        // }
        // foreach (int a in ans)
        // {
        //     Console.Write(a + " ");
        // }
        // System.Console.WriteLine();
        String text = Console.ReadLine() + "$";
        int patternCount = int.Parse(Console.ReadLine());
        string[] patterns = Console.ReadLine().Split();
        int[] suffixArray = computeSuffixArray(text);
        int[] res = new int[text.Length];
        foreach (var p in patterns)
        {
            T t = findOccurrences(p, text, suffixArray);
            for (int i = t.start; i < t.end + 1; i++)
            {
                int pos = suffixArray[i];
                if (res[pos] == 0)
                    Console.Write(pos + " ");
                res[pos]++;
            }
        }
        // bool[] occurs = new bool[text.Length];
        // foreach (var p in patterns)
        // {
        //     List<int> occurrences = findOccurrences(p, text, suffixArray);
        //     foreach (int x in occurrences)
        //     {
        //         occurs[x] = true;
        //     }
        // }
        // for (int i = 0; i < occurs.Length; i++)
        // {
        //     if (occurs[i])
        //         Console.Write(i + " ");
        // }
        // System.Console.WriteLine();
        // Console.ReadKey();
    }

    public static int[] computeSuffixArray(String text) // BuildSuffixArray
    {
        // int[] order = new int[text.Length];
        int[] order = SortCharacters(text); // int --> long
        int[] clas = ComputeCharClasses(text, order);
        int l = 1;
        while (l < text.Length)
        {
            order = SortDoubled(text, l, order, clas);
            clas = UpdateClasses(order, clas, l);
            l = 2 * l;
        }
        return order;
    }

    private static int[] UpdateClasses(int[] newOrder, int[] clas, int l) //
    {
        int n = newOrder.Length; // |text|
        int[] newClas = new int[n];
        newClas[newOrder[0]] = 0;
        for (int i = 1; i < n; i++)
        {
            int cur = newOrder[i], prev = newOrder[i - 1]; // Ci Cj
            int mid = (cur + l) % n, midPrev = (prev + l) % n; // Ci+l Cj+l
            if (clas[cur] != clas[prev] || clas[mid] != clas[midPrev])
            {
                newClas[cur] = newClas[prev] + 1;
            }
            else
            {
                newClas[cur] = newClas[prev];
            }
        }
        return newClas;
    }

    private static int[] SortDoubled(string text, int l, int[] order, int[] clas) //
    {
        int[] count = new int[text.Length];
        int[] newOrder = new int[text.Length];
        for (int i = 0; i < text.Length; i++)
        {
            count[clas[i]]++; // conut(Ci)
        }
        for (int j = 1; j < text.Length; j++)
        {
            count[j] = count[j] + count[j - 1];
        }
        for (int i = text.Length - 1; i > -1; i--)
        {
            int start = (order[i] - l + text.Length) % text.Length;// Ci-l
            int cl = clas[start];
            count[cl]--;
            newOrder[count[cl]] = start;
        }
        return newOrder;
    }

    private static int[] ComputeCharClasses(string text, int[] order)
    {
        int[] clas = new int[text.Length];
        clas[order[0]] = 0;
        for (int i = 1; i < text.Length; i++)
        {
            if (text[order[i]] != text[order[i - 1]])
            {
                clas[order[i]] = clas[order[i - 1]] + 1;
            }
            else
            {
                clas[order[i]] = clas[order[i - 1]];
            }
        }
        return clas;
    }

    private static int[] SortCharacters(string text) // countSort
    {
        int[] order = new int[text.Length];
        Dictionary<char, int> count = new Dictionary<char, int>(5)
            {
                {'A', 0} , {'C', 0} , {'G', 0} , {'T', 0} , {'$', 0}
            };//ACGT$
        for (int i = 0; i < text.Length; i++)
        {
            count[text[i]]++;
        }
        string alphabet = "$ACGT";
        for (int j = 1; j < 5; j++) // partial sum
        {
            count[alphabet[j]] = count[alphabet[j]] + count[alphabet[j - 1]];
        }
        for (int i = text.Length - 1; i > -1; i--)
        {
            char c = text[i];
            count[c]--;
            order[count[c]] = i;
        }
        return order;
    }

}