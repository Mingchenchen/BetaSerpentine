
def LenStrand(strand):
    L = float(len(strand))
    StrandStepH = 6.5
    lenght = ((L-1)/2)*StrandStepH
    return lenght


def CountPerimeter(structure):
    #constants
    ArchW = 11
    ArchH = 6.5
    ExternalLayer = 5*2

    StrandsLengths = []
    #print 'L', len(structure)
    for i in range(len(structure)):
        if i in [0,len(structure)-1] and i % 2 == 0:
            StrandsLengths.append(LenStrand(structure[i]) + ArchH + ExternalLayer + 3.25) # 3.25 - additional
        elif i % 2 == 0:
            StrandsLengths.append(LenStrand(structure[i]) + 2*ArchH + ExternalLayer)
    #print StrandsLengths

    Perimeter = StrandsLengths[0] + StrandsLengths[-1]
    import math
    for j in range(len(StrandsLengths)-1):
        Perimeter += math.fabs(StrandsLengths[j] - StrandsLengths[j+1])
    Perimeter += ((len(StrandsLengths) - 1) * 2 * ArchW) + (2 * ExternalLayer)

    #print Perimeter
    return Perimeter


def CountSquare(structure):
    ArchW = 11
    ArchH = 6.5
    ExternalLayer = 5*2

    import math

    StructuresLength = []
    for i in range(len(structure)):
        if i in [0,len(structure)-1]:
            StructuresLength.append(LenStrand(structure[i]) + ArchH + ExternalLayer + 3.25) # 3.25 - additional
        else:
            StructuresLength.append(LenStrand(structure[i]) + 2*ArchH + ExternalLayer)
    #print StructuresLength
    Square = 0

    for l in range(len(StructuresLength)):
        if l % 2 != 0:
            Square += ArchW * (min([StructuresLength[l-1],StructuresLength[l+1]]))

        if l % 2 == 0 and l != 0 and l < (len(StructuresLength) - 2):
            Square += ExternalLayer/2 * (math.fabs(StructuresLength[l] - StructuresLength[l+2]))
    Square += ExternalLayer/2 * (StructuresLength[0] + StructuresLength[-1])
    #print Square
    return Square


def TurnCoords(structure):
    """
    Count coordinate with 1.8 twist
    """
    StructuresLength = []
    ArchW = 11
    ArchH = 12
    for i in range(len(structure)):
        if i % 2 == 0:
            if i in [0,len(structure)-1]:
                StructuresLength.append(LenStrand(structure[i]) + ArchH)
            else:
                StructuresLength.append(LenStrand(structure[i]) + 2*ArchH)
        else:
            StructuresLength.append(ArchW)
    #print StructuresLength
    vectors = [[0,1],[1,0],[0,-1],[1,0]]
    coords = [[0,0]]
    C = [0,0]
    Ymin = 0
    Ymax = 0
    for i in range(len(StructuresLength)):
        j = i % 4
        V = vectors[j]
        C = [C[0] + StructuresLength[i]*V[0],C[1] + StructuresLength[i]*V[1]]
        if C[1] > Ymax: Ymax = C[1]
        if C[1] < Ymin: Ymin = C[1]
        coords.append(C)

    for j in range(len(coords)):
        coords[j][1] += -1*Ymin

    Ymax += -1*Ymin
    Ymin += -1*Ymin

    center = [coords[-1][0]/2, Ymax - ((Ymax - Ymin)/2)]

    return [coords, center]


def EuclidDist(coord, center):
    import math
    xd = math.fabs(center[0] - coord[0])
    yd = math.fabs(center[1] - coord[1])
    Dist = math.sqrt(xd**2 + yd**2)
    return Dist


def FindMaxDist(coords, center):
    """
    Count max distance of given coordinates and geometrical center
    """
    MaxD = 0
    for i in coords:
        D = EuclidDist(i, center)
        #print D
        if D > MaxD: MaxD = D
    #print
    #print MaxD
    return MaxD


def CountTwistScore(structure):
    """
    Score mean max discrepancy by 1.8 tern comparing with geometrical center
    """
    tmp = TurnCoords(structure)
    d = FindMaxDist(tmp[0], tmp[1]) * 0.031410759078128 # sin(1^ 48' = 1.8^)
    TwistScore = 1 / (1 + 2.7 **((1.05 - d)/-0.04))

    return TwistScore


def StrandsLength(structure):
    L = 0
    for i in range(len(structure)):
        if i % 2 == 0:
            L += len(structure[i])
    #print L
    return L


def CountCScore(structure):
    """
    Count score of compactness, that based on the min difference between adjacent strands lengths
    """
    #constants
    ArchW = 11
    ArchH = 6.5

    Lengths = []
    #print 'L', len(structure)
    for i in range(len(structure)):
        if i in [0, len(structure)-1] and i % 2 == 0:
            Lengths.append(LenStrand(structure[i]) + ArchH + 3.25) # 3.25 - addition
        elif i % 2 == 0:
            Lengths.append(LenStrand(structure[i]) + 2*ArchH)

    #print Lengths
    lengths_differences = 0
    sum_length = 0
    for i in range(len(Lengths) - 1):
        if Lengths[i] > Lengths[i+1]:
            lengths_differences += Lengths[i] - Lengths[i+1]
        else: lengths_differences += Lengths[i+1] - Lengths[i]

        #print lengths_differences
        sum_length += Lengths[i]

    sum_length += Lengths[-1]
    #print sum_length

    return 1 - lengths_differences/sum_length

def CountPerimeterScore(structure):
    """
    The score is based on comparison of given serpentine perimeter with foursquare perimeter the same square
    """
    import math
    Perimeter = CountPerimeter(structure)
    Square = CountSquare(structure)
    PerimeterScore = 4*math.sqrt(Square)/Perimeter

    MaxL = 0
    for i in range(len(structure)):
        if i % 2 == 0:
            L = len(structure[i])
            if L > MaxL: MaxL = L

    return PerimeterScore



def subsetOdd(list):
    output = ''
    for i in range(len(list)):
        if i % 2 == 0:
            output += list[i]
    return  output

def AAtoCharge(string):
    output = ''
    for s in string:
        if s in ['K','R']:
            output += '+'
        elif s in ['D','E']:
            output += '-'
        else: output += '0'
    return output

def ConvertInnerAAsToCharge(structure_aa, types, N):
    """
    Count charge of inner amino acids of serpentine
    N - number of Arc from 2 to Last Arc - 1
    """
    #print structure_aa
    #chosing AA radical which will be inside Arc according Arc type
    Arc = structure_aa[2*N+1]
    if types[N] == '5 Res Arc':
        InArcAA = Arc[2]
    elif types[N] == '6 Res Arc 1':
        InArcAA = Arc[3]
    elif types[N] == '6 Res Arc 2':
        InArcAA = Arc[2]
    elif types[N] == 'GBPL':
        InArcAA = Arc[1]
    else: InArcAA = 'N'


    PrevInStrand = subsetOdd(structure_aa[2*N][::-1])
    NextInStrand = subsetOdd(structure_aa[2*N+2])

    AdditionalAAs = ''

    if len(PrevInStrand) == len(NextInStrand):
        AdditionalAAs = structure_aa[2*N-1][-1] + structure_aa[2*N+3][0]
    elif len(PrevInStrand) > len(NextInStrand):
        AdditionalAAs = PrevInStrand[len(NextInStrand)] + structure_aa[2*N+3][0]
        PrevInStrand = PrevInStrand[:len(NextInStrand)]
    elif len(PrevInStrand) < len(NextInStrand):
        AdditionalAAs = structure_aa[2*N-1][-1] + NextInStrand[len(PrevInStrand)]
        NextInStrand = NextInStrand[:len(PrevInStrand)]

    #print [AAtoCharge(InArcAA), AAtoCharge(PrevInStrand), AAtoCharge(NextInStrand),AAtoCharge(AdditionalAAs)]
    return [AAtoCharge(InArcAA), AAtoCharge(PrevInStrand), AAtoCharge(NextInStrand),AAtoCharge(AdditionalAAs)]

def CompensateStrandCharges(strand1, strand2):
    """
    Function counts compensation of charges in the serpentine strands
    """
    oppositeCharge = {'+':'-', '-':'+'}
    for i in range(1,len(strand1)-1):
        if strand1[i] in '+-':
            Charge = strand1[i]
            if oppositeCharge[Charge] in strand1[i-1]:
                strand1 = strand1[:i-1] + '00' + strand1[i+1:]
            elif oppositeCharge[Charge] in strand2[i-1:i+2]:
                for j in range(i-1,i+2):
                    if oppositeCharge[Charge] == strand2[j]:
                        strand1 = strand1[:i] + '0' + strand1[i+1:]
                        strand2 = strand2[:j] + '0' + strand2[j+1:]
                        break
            elif oppositeCharge[Charge] in strand1[i+1]:
                strand1 = strand1[:i] + '00' + strand1[i+2:]

    return [strand1, strand2]

def FindUncompensatedCharges(InArcCharge, PrevStrandCharges, NextStrandCharges, AdditionalCharges):
    """
    Look for uncompensated charges in serpentine
    """
    oppositeCharge = {'+': '-', '-': '+', '0': '0'}
    if InArcCharge in '+-':
        if PrevStrandCharges[0] == oppositeCharge[InArcCharge]:
            PrevStrandCharges = '0' + PrevStrandCharges[1:]

        elif NextStrandCharges[0] == oppositeCharge[InArcCharge]:
            NextStrandCharges = '0' + NextStrandCharges[1:]

    strands = [PrevStrandCharges, NextStrandCharges]
    #for s in strands: print s
    #print
    strands = CompensateStrandCharges(strands[0], strands[1])
    strands = CompensateStrandCharges(strands[1], strands[0])
    if strands[0][-1] in '+-':
        if oppositeCharge[strands[0][-1]] in strands[1][-1]:
            strands[1] = strands[1][:-1] + '0'
            strands[0] = strands[0][:-1] + '0'
        elif oppositeCharge[strands[0][-1]] in AdditionalCharges:
            AdditionalCharges = AdditionalCharges.replace(oppositeCharge[strands[0][-1]],'0',1)
            strands[0] = strands[0][:-1] + '0'

    #for s in strands: print s
    #print

    if strands[1][-1] in '+-':
        if oppositeCharge[strands[1][-1]] in strands[0][-1]:
            strands[1] = strands[1][:-1] + '0'
            strands[0] = strands[0][:-1] + '0'
        elif oppositeCharge[strands[1][-1]] in AdditionalCharges:
            AdditionalCharges = AdditionalCharges.replace(oppositeCharge[strands[1][-1]],'0',1)
            strands[1] = strands[1][:-1] + '0'


    count = strands[0].count('+') + strands[0].count('-') + strands[1].count('+') + strands[1].count('-')
    #print count
    return count

def CountCharges(structure_aa, types):
    """
    Check for uncompensated charges in serpentine
    If internal charged amino acid have near amino acid with opposite charge (D and E opposite K and R),
    charge is considered compensated.
    """
    NCharges = [0]
    for N in range(1,len(types)-1):
        charges = ConvertInnerAAsToCharge(structure_aa, types, N)
        NCharge = FindUncompensatedCharges(charges[0], charges[1], charges[2], charges[3])
        NCharges.append(NCharge)
    NCharges.append(0)

    return NCharges


def CheckProlines(structure_aa):
    """
    Count prolines residues among inner amino acids in strands of serpentine
    """
    NProlines = []
    for i in range(len(structure_aa)):
        if i % 2 != 0:
            PrevInStrand = subsetOdd(structure_aa[i-1][::-1])
            NextInStrand = subsetOdd(structure_aa[i+1])
            NProlines.append(PrevInStrand.count('P') + NextInStrand.count('P'))
    return NProlines
