from enum import Enum


def score(s, t):
    if s==t:
        return 1
    else:
        return -1

def print_alignment(s,t):
    s_align, t_align, middle, high_score = align(s,t)

    print("Alignment Score:",high_score)
    print(s_align)
    print(middle)
    print(t_align)

class MatchType(Enum):
    NORMAL = 0
    S_GAP = 1
    T_GAP = 2

def align(s, t):
    gap_penalty = -2

    #Rows
    m = len(s)

    #Cols
    n = len(t)

    dp_scores = [ [None for y in range(n+1)] for x in range(m+1)]
    dp_parent = [ [None for y in range(n+1)] for x in range(m+1)]
    
    dp_scores[0][0] = 0

    for i in range(1,m+1):
        dp_scores[i][0] = i*gap_penalty
        dp_parent[i][0] = (i-1,0,MatchType.T_GAP)

    for j in range(1, n+1):
        dp_scores[0][j] = j*gap_penalty
        dp_parent[0][j] = (0,j-1,MatchType.S_GAP)

    for i in range(1,m+1):
        for j in range(1, n+1):
            match = dp_scores[i-1][j-1]+score(s[i-1],t[j-1])
            s_gap = dp_scores[i-1][j]+gap_penalty
            t_gap = dp_scores[i][j-1]+gap_penalty

            scores = [t_gap,s_gap, match]
            max_score = max(scores)
            
            argmax = scores.index(max_score)
            
            parent = (-1,-1)

            if argmax == 2:
                parent = (i-1,j-1, MatchType.NORMAL)
            elif argmax == 1:
                parent = (i-1, j, MatchType.S_GAP)
            elif argmax == 0:
                parent = (i, j-1, MatchType.T_GAP)

            dp_scores[i][j] = max_score
            dp_parent[i][j] = parent
    

    current = dp_parent[m][n]
    high_score = dp_scores[m][n]
    s_align = ""
    t_align = ""
    middle = ""

    while current != None:
        i = current[0]
        j = current[1]
        match_type = current[2]


        if match_type == MatchType.NORMAL:
            s_align+=s[i]
            t_align+=t[j]
            if s[i]==t[j]:
                middle+="|"
            else:
                middle+=";"
            pass
        elif match_type == MatchType.S_GAP:
            s_align+=s[i]
            t_align+=" "
            middle+="-"
            pass
        elif match_type == MatchType.T_GAP:
            s_align+=" "
            t_align+=t[j]
            middle+="-"
            pass

        

        #print(current)
        
        current = dp_parent[i][j]

    s_align=s_align[::-1]
    t_align=t_align[::-1]
    middle=middle[::-1]
    return s_align,t_align,middle,high_score
    


if __name__== "__main__":
    s = "ACGTTTTGAAAGGTTATCATGTAGCATGCATCAGTATCAGTACTTCATT"
    t = "ACGTTTTGAAAGTTTATCCATGTAGCATGCATCAGTATCAGTACCTTTT"
    #s = "AAAC"
    #t = "AGC"
    print_alignment(s,t)
