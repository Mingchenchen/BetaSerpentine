
from SerpentinesFunctions.SerpentinesScores import *


def overlap(list1, list2):
    """
    Takes two lists of numbers and returns list of overlapping numbers.

    Examples.
    Input.
    [1,2,3,4,5]
    [3,4,5,6,7]

    Output
    [3,4,5]
    """
    overlapping_pos = []
    if len(list2) < len(list1):
        for position in list2:
            if position in list1: overlapping_pos.append(position)
    else:
        for position in list1:
            if position in list2: overlapping_pos.append(position)
    return overlapping_pos



def check_aa_orientation(strand1, strand2):
    """
    Takes two lists of numbers of amino acids in two beta-strands and returns boolean.
    Function return True if at least one the same amino acids is inner in one strand and is outer in another.
    Amino acids in odd positions in strand is inner, in even positions - outher.

    Examples.
    Input.
    [1,2,3,4,5]
        [3,4,5,6,7]

    Output: False

    Input.
    [1,2,3,4,5]
          [4,5,6,7,8]

    Output: True
    """
    odd = []
    for i in range(len(strand1)):
        if i % 2 == 0: odd.append(strand1[i])
    even = []
    for j in range(len(strand2)):
        if j % 2 == 1: even.append(strand2[j])
    if len(overlap(odd,even)) > 0:
        return True
    else: return False



def is_compatibile(arch1, arch2):
    """
    Checks possibility of arches merging into serpentine and return boolean.
    Function takes two arches structures in list of lists from ArchCandy output.
    Lists mean [[strand], [arc], [strand]].
    Function checks overlapping of strands regions, not included in arcs regions of two arches.
    Also the function cheks orientation of same amino acids within different arches.

    Example.
    Input
[[1,2,3,4,5],[6,7,8],[9,10,11,12,13]]
  [[2,3,4,5,6],[7,8,9],[10,11,12,13,14]]
    Output
    False

    Input
[[1,2,3,4,5],[6,7,8],[9,10,11,12,13]]
                      [[10,11,12,13,14],[15,16,17],[18,19,20,21,22]]
    Output
    True
"""
    matrix = [[[] for y in range(3)] for x in range(3)]
    for element1 in range(3):
        for element2 in range(3):
            matrix[element1][element2] = overlap(arch1[element1], arch2[element2])
            #print overlap(arch1[element1], arch2[element2])

    if len(matrix[1][1]) == 0:
        if len(matrix[2][0]) >= 2:
            if (len(matrix[0][2]) + len(matrix[0][1]) + len(matrix[1][2])) == 0:
                #if len(matrix[1][0]) < len(arch1[1])/2 and len(matrix[2][1]) < len(arch2[1])/2:
                strand1 = arch2[0]
                strand2 = arch1[2]
                if check_aa_orientation(strand1, strand2):
                    return True
                else: return False
            else: return False
        else: return False
    else: return False



def create_compare_matrix(Arches, P = False):
    """
    Function takes dictionary of imported arches and check compatibility of all possible arches pairs.
    Results of this are recorded as compatibility matrix (list of lists)
    [[2],[3],[]] this mean that 1th arch is compatible with 2th, 2th - with 3rd.

    Input
    Arches = {1: [[0.63], [[1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15, 16, 17, 18]], '1', 'GBPL', '1', '18'],
          2: [[0.567], [[1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12], [13, 14, 15, 16, 17, 18, 19]], '2', '5 Res Arc', '1', '19'],
          3: [[0.432], [[1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13], [14, 15, 16, 17, 18, 19, 20]], '3', '6 Res Arc 1', '1', '20']
          ...}

    Output
    [[], [29], [], [], [], [20, 26, 27, 29], [29], []...]
    """
    n = max(Arches.keys()) + 1
    matrix = [[] for x in range(0, n)]
    for key1 in sorted(Arches.keys()):
        for key2 in Arches.keys():
            if is_compatibile(Arches[key1][1], Arches[key2][1]):
                if key2 not in matrix[key1]:
                    matrix[key1].append(key2)
                    #print key1, key2
            elif is_compatibile(Arches[key2][1], Arches[key1][1]):
                if key1 not in matrix[key2]:
                    matrix[key2].append(key1)
                    #print key2, key1
    if P:
        print 'MATRIX'
        for i in range(len(matrix)):
            if len(matrix[i]) > 0:
                print i, matrix[i]
    return matrix

def graph_from_matrix(matrix):
    """
    Function transforms matrix of compatibility in the list with two dictionaries:
    Ngraph consists all possible variants of compatibility in direction from N-end to C-end of protein
    Cgraph has all variants from in C-N direction

    Input
    [[], [29], [], [], [], [20, 26, 27, 29], [29], []....]

    Output
    [{1: [29], 5: [20, 26, 27, 29], 6: [29], 8: [28], 13: [29], 14: [28]},
    {28: [8, 14], 26: [5], 27: [5], 20: [5], 29: [1, 5, 6, 13]}]
    """
    Ngraph = {}
    Cgraph = {}
    for i in range(len(matrix)):
        if len(matrix[i]) > 0:
            tmp_values = []
            for j in matrix[i]:
                #if j not in keys:
                tmp_values.append(j)

            if len(tmp_values) > 0:
                Cgraph.update({i:tmp_values})
                for k in tmp_values:
                    if k not in Ngraph:
                        Ngraph.update({k:[i]})
                    else:
                        Ngraph[k] = Ngraph[k] + [i]
    #for i in Cgraph: print i, Cgraph[i]
    #print
    #for i in Ngraph: print i, Ngraph[i]
    return [Cgraph, Ngraph]


def mergeStructure(structure1, structure2):
    """
    Function merge given structures into one pseudo-arch.
    It based on the overlap inner amino acids of the last serpentine strand and out amino acid of first strand
    in the given arch. And vice versa.

    Input
    [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11], [12, 13, 14, 15, 16]]
                              [[9, 10, 11, 12, 13], [14, 15, 16], [17, 18, 19, 20, 21]]

    Output
    [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11], [12, 13], [14, 15, 16], [17, 18, 19, 20, 21]]
    """
    if structure2[2][-1] < structure1[2][0]:
        output = structure2[1:]
        newstrand = []
        for pos in range(structure2[-1][0], structure1[0][-1]):
            #print pos
            if pos not in structure1[0] and pos not in structure1[2]: newstrand.append(pos)
            elif pos in structure1[0] and pos not in structure1[1]: newstrand.append(pos)
        output = [structure2[:2]]+ [newstrand] + output
        return output
    else:

        output = structure1[:-1]
        newstrand = []
        #print 'L', len(range(structure1[-1][0], structure2[1][0]))
        for pos in range(structure1[-1][0], structure2[1][0]):
            #print pos
            if pos not in structure2[0] and pos not in structure2[2]: newstrand.append(pos)
            elif pos in structure2[0] and pos not in structure2[1]: newstrand.append(pos)
        output += [newstrand] + [structure2[1]] + [structure2[2]]
        return output


def check_ends(serpentines_structure):
    """
    Function delete terminal amino acids from strands, if they length is more than  the same opposite element in arch
    Input
    [[1, 2, 3, 4, 5], [6, 7, 8, 9], [10, 11], [12, 13, 14, 15], [16, 17, 18, 19, 20]]

    Output
    [[3, 4, 5], [6, 7, 8, 9], [10, 11], [12, 13, 14, 15], [16, 17, 18]]
    """

    if len(serpentines_structure[0]) > len(serpentines_structure[2]):
        serpentines_structure[0] = serpentines_structure[0][-(len(serpentines_structure[2]) + 1):]

    if len(serpentines_structure[-1]) > len(serpentines_structure[-3]) + 2:
        serpentines_structure[-1] = serpentines_structure[-1][:len(serpentines_structure[-3]) + 1]

    return serpentines_structure


def structure_conversion(serpentine_structure, protein_sequence):
    """
    Convert list of coordinate to list of amino acids accordingly given protein
    Input
    [[4, 5, 6], [7, 8, 9, 10], [11, 12], [13, 14, 15, 16], [17, 18, 19]]

    Output
    [['A', 'N', 'N'], ['T', 'C', 'A', 'T'], ['Q', 'L'], ['A', 'N', 'F', 'L'], ['V', 'Q', 'Q']]
    """
    serpentine_structure_aa = []
    for element in serpentine_structure:
        aa_seq = []
        for i in element:
            aa_seq.append(protein_sequence[i-1])
        serpentine_structure_aa.append(aa_seq)

    return serpentine_structure_aa


def createSerpentine(path, Arches, protein_sequence):
    """
    Create serpentine by the given path
    Return dict with all description (sequence, scores, structure, type of serpentine)
    Input
    Path [14, 28]

    Output
    {'14-28': [[0.572, 0.191], [['A', 'N', 'N'], ['T', 'C', 'A', 'T'], ['Q', 'L'], ['A', 'N', 'F', 'L'], ['V', 'Q', 'Q']],
    [4, 19], 1.0, [0, 0], [[4, 5, 6], [7, 8, 9, 10], [11, 12], [13, 14, 15, 16], [17, 18, 19]], ['GBPL', 'GBPL'],
    0.9951159997383305, 0.99999594146826, [14, 28], 0.38149999999999995, 0.37963521313235765, 1, [0, 0]]}
    """
    import copy
    import math
    #print 'Path', path
    structure = copy.deepcopy(Arches[path[0]][1])
    #print structure
    scores = copy.deepcopy(Arches[path[0]][0])
    types = [Arches[path[0]][3]]
    #print path, scores, Arches[path[0]]

    for i in range(1,len(path)):

        scores += Arches[path[i]][0]
        types.append(Arches[path[i]][3])
        structure = mergeStructure(structure, Arches[path[i]][1])

    # cut ends of serpentine
    structure = check_ends(structure)

    positions = [structure[0][0], structure[-1][-1]]

    structure_aa = structure_conversion(structure, protein_sequence)

    # Perimeter score = minPerimeter/Perimeter of Serpentine
    # minPerimener = 4 * sqrt(Square); minimal perimeter - perimeter of square
    PerimeterScore = CountPerimeterScore(structure)
    TwistScore = CountTwistScore(structure)

    CScore = CountCScore(structure_aa)
    charge = CountCharges(structure_aa, types)
    prolines = CheckProlines(structure_aa)

    NArches = len(types)

    name = ''
    for n in path: name += str(n) + '-'
    name = name[:-1]


    ScoresMean = sum(scores) / NArches

    FinalScore = PerimeterScore * CScore * ScoresMean * TwistScore
    #print name, path, structure_aa
    SerpentineAmount = 1

    if sum(charge) + sum(prolines) > 0: FinalScore = 0

    #               0         1            2        3       4        5         6      7               8          9
    #               10          11          12                  13
    return {name:[scores, structure_aa, positions, CScore, charge, structure, types, PerimeterScore, TwistScore, path,
                  ScoresMean, FinalScore, SerpentineAmount, prolines]}

def EvaluateSerpentine(path, Arches, protein_sequence):
    """
    Function count all scores for given serpentine and return the final score, that depends on the scores values
    If there are proline ore uncompensated charges in strands of serpentine, FinalScore becomes 0.
    """
    import copy
    import math
    structure = copy.deepcopy(Arches[path[0]][1])
    scores = copy.deepcopy(Arches[path[0]][0])
    types = [Arches[path[0]][-1]]

    for i in range(1,len(path)):

        scores += Arches[path[i]][0]
        types.append(Arches[path[i]][-1])
        structure = mergeStructure(structure, Arches[path[i]][1])

    structure = check_ends(structure)

    structure_aa = structure_conversion(structure, protein_sequence)


    PerimeterScore = CountPerimeterScore(structure)
    TwistScore = CountTwistScore(structure)

    CScore = CountCScore(structure_aa)

    charge = CountCharges(structure_aa, types)
    prolines = CheckProlines(structure_aa)

    NArches = len(types)

    name = ''
    for n in path: name += str(n) + '-'
    name = name[:-1]


    ScoresMean = sum(scores) / NArches

    FinalScore = PerimeterScore * CScore * ScoresMean * TwistScore

    if sum(charge) + sum(prolines) > 0: FinalScore = 0

    return FinalScore

def FindSeeds(Arch, Cgraph, Ngraph):
    """
    Create the first pair of arch from which can grow serpentines

    Output
    [[1, 29]]
    []
    [[5, 20], [5, 26], [5, 27], [5, 29]]
    ...
    """
    Seeds = []
    if Arch in Cgraph:
        for i in Cgraph[Arch]:
            Seeds.append([Arch, i])
    if Arch in Ngraph:
        for j in Ngraph[Arch]:
            Seeds.append([j, Arch])
    return Seeds

def NewPaths(Seed, Cgraph, Ngraph):
    """
    Function create the serpentine from the given seed
    """
    Paths = []
    if Seed[0] in Ngraph:
        for i in Ngraph[Seed[0]]:
            if i not in Seed:
                Paths.append([i] + Seed)
    if Seed[-1] in Cgraph:
        for i in Cgraph[Seed[-1]]:
            if i not in Seed:
                Paths.append(Seed + [i])
    if Paths == []:
        return [Seed]
    return Paths

def SeedGrowht(Seed, Cgraph, Ngraph, protein_sequence, Arches):
    """
    Create the sequence of arch, that can combine into one serpentine and count all
    scores to evaluate created serpentine
    """
    NewPath = NewPaths(Seed, Cgraph, Ngraph)
    #print NewPath
    SeedScore = EvaluateSerpentine(Seed, Arches, protein_sequence)
    #print 'SeedScore', SeedScore
    GrowingPaths = []
    if NewPath == []:
        return Seed
    else:
        for path in NewPath:
            Score = EvaluateSerpentine(path, Arches, protein_sequence)
            #print Score, path
            if Score > SeedScore:
                GrowingPaths.append(path)
        if GrowingPaths == []: return [Seed]
        return GrowingPaths

def AllPathsFromSeed(Seed, Cgraph, Ngraph, protein_sequence, Arches):
    """
    Create all possible variants of serpentines from given the first arch
    """
    Old = [Seed]
    New = SeedGrowht(Seed, Cgraph, Ngraph, protein_sequence, Arches)
    #print 'New', New
    #count = 0
    while New != Old:
        #print count
        #count += 1
        Old = New
        New = []
        for seed in Old:
            #print 'seed', seed
            tmp = SeedGrowht(seed, Cgraph, Ngraph, protein_sequence, Arches)
            #print tmp
            New += tmp
        #print
    return New

def AllPathFromGraph(Cgraph, Ngraph, protein_sequence, Arches):
    """
    Create list of lists with all possible arch, that can organise serpentine

    Output
    [[1, 29], [5, 20], [5, 26], [5, 27], [5, 29], [6, 29], [8, 28], [13, 29], [14, 28]]
    """
    Seeds = []
    for Arch in Arches:
        tmpSeeds = []
        if Arches[Arch][0][0] >= 0.0:
            tmpSeeds = FindSeeds(Arch, Cgraph, Ngraph)
        for tmpSeed in tmpSeeds:
            if tmpSeed not in Seeds: Seeds.append(tmpSeed)
    output = []
    for Seed in Seeds:
        Paths = AllPathsFromSeed(Seed, Cgraph, Ngraph, protein_sequence, Arches)
        for Path in Paths:
            if Path not in output: output.append(Path)
    return output

def AllSerpentines(Cgraph, Ngraph, Arches, protein_sequence, OutputThreshold):
    """
    Create serpentines from given arch and return all serpentines with higher Score that OutputThreshold and all
    information about it (scores, coordinates in protein, amino acid sequence...)

    Output
    [{'6-29': [[0.479, 0.502], [['T', 'A', 'N'], ['N', 'T', 'C', 'A', 'T', 'Q'], ['L', 'A'], ['N', 'F', 'L'], ['V', 'Q', 'Q']],
     [3, 19], 1.0, [0, 0], [[3, 4, 5], [6, 7, 8, 9, 10, 11], [12, 13], [14, 15, 16], [17, 18, 19]], ['6 Res Arc 1', 'PPL'],
     0.9951159997383305, 0.99999594146826, [6, 29], 0.4905, 0.4881024168844599, 1, [0, 0]],
     ....}]

    """
    import copy
    SerpentinesPaths = AllPathFromGraph(Cgraph, Ngraph, protein_sequence, Arches)
    Serpentines = {}

    DeltaStrandArc = [0] * (len(protein_sequence) + 1) # vector with length equal to protein length
    #DeltaStrandArc_Scores = [0] * (len(protein_sequence) + 1)
    Nstrands = [0] * (len(protein_sequence) + 1)
    Narcs = [0] * (len(protein_sequence) + 1)
    for path in SerpentinesPaths:
        Serpentine = createSerpentine(path, Arches, protein_sequence)
        name = Serpentine.keys()[0]
        if Serpentine[name][11] >= OutputThreshold:
            Serpentines.update(Serpentine)
            for i in range(len(Serpentine[name][5])):
                if i % 2 == 0:
                    d = 1
                else: d = -1
                for j in Serpentine[name][5][i]:
                    DeltaStrandArc[j] = DeltaStrandArc[j] + d
                    #DeltaStrandArc_Scores[j] = round(DeltaStrandArc_Scores[j] + d*Serpentine[name][11],3)
                    if d == 1:
                        Nstrands[j] = Nstrands[j] + 1
                    if d == -1:
                        Narcs[j] = Narcs[j] + 1

    return [Serpentines,Nstrands[1:], Narcs[1:]]

