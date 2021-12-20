def losersSameNextZeroJSON(winners, bracket):
    #print("samenext zero")
    for i in range(len(winners)-1):
        for j in range(len(winners[i])):
            if bracket["winners"][i]["seeds"][j]["teams"] != [{'name': '', 'game': -1}, {'name': '', 'game': -1}]:
                if i == 0:
                    winners[i][j][1][1] = 0
                    winners[i][j][1][2] = j//2
                    winners[i][j][1][3] = 1
                    cur = winners[i][j][1]
                    bracket[cur[0]][cur[1]]["seeds"][cur[2]]["teams"][cur[3]]["name"] = [i,j]
                elif i == 1:
                    #print(len(bracket[0][0]), (len(bracket[0][0])//2-j-1)*2+1)
                    if bracket["winners"][0]["seeds"][(len(bracket["winners"][0]["seeds"])//2-j-1)*2+1]["teams"] != [{'name': '', 'game': -1}, {'name': '', 'game': -1}]:
                        #print("stuff")
                        winners[i][j][1][1] = 0
                        winners[i][j][1][2] = len(bracket["winners"][0]["seeds"])//2-j-1
                        winners[i][j][1][3] = 0
                        cur = winners[i][j][1]
                        bracket[cur[0]][cur[1]]["seeds"][cur[2]]["teams"][cur[3]]["name"] = [i,j]
                    else:
                        base_pos = (len(bracket["winners"][0]["seeds"])//2-j-1)
                        #print(len(bracket[0][0])//2-j-1)
                        winners[i][j][1][1] = 1
                        winners[i][j][1][2] = base_pos//2
                        winners[i][j][1][3] = base_pos%2
                        if base_pos%2 == 1 and bracket["losers"][0]["seeds"][base_pos-1]["teams"] != [{'name': '', 'game': -1}, {'name': '', 'game': -1}]:
                            #print(bracket[1][0][base_pos-1])
                            winners[i][j][1][3] = 0
                        cur = winners[i][j][1]
                        bracket[cur[0]][cur[1]]["seeds"][cur[2]]["teams"][cur[3]]["name"] = [i,j]
                elif i == 2:
                    #if is_pow:
                    #    winners[i][j][1][1] = (2 * (i+1)) - 3
                    #else:
                    l = len(bracket["losers"][(2 * (i+1)) - 4]["seeds"])
                    #print(l)
                    mid = (l-1)/2
                    q1 = mid - l//4
                    q2 = mid + l//4
                    #print(mid, q1, q2)
                    winners[i][j][1][1] = 2
                    if j < mid:
                        if j < q1:
                            winners[i][j][1][2] = int(q1 + abs(q1-j))
                        else: #means j is greater
                            winners[i][j][1][2] = int(q1 - abs(q1-j))
                    else: #means j is greater
                        if j < q2:
                            winners[i][j][1][2] = int(q2 + abs(q2-j))
                        else:
                            winners[i][j][1][2] = int(q2 - abs(q2-j))
                    winners[i][j][1][3] = 0
                    cur = winners[i][j][1]
                    bracket[cur[0]][cur[1]]["seeds"][cur[2]]["teams"][cur[3]]["name"] = [i,j]
                elif i > 2:
                    #if is_pow:
                    #    winners[i][j][1][1] = (2 * (i+1)) - 3
                    #else:
                    midindex = len(bracket["losers"][(2 * (i+1)) - 4]["seeds"])//2
                    winners[i][j][1][1] = (2 * (i+1)) - 4
                    if i % 2 == 1:
                        if j < midindex:
                            winners[i][j][1][2] = midindex + j
                        else:
                            winners[i][j][1][2] = j - midindex
                    else:
                        winners[i][j][1][2] = j
                    winners[i][j][1][3] = 0
                    cur = winners[i][j][1]
                    bracket[cur[0]][cur[1]]["seeds"][cur[2]]["teams"][cur[3]]["name"] = [i,j]
    return winners

def losersSameNextOneJSON(winners, bracket):
    for i in range(len(winners)-1):
        for j in range(len(winners[i])):
            if bracket["winners"][i]["seeds"][j]["teams"] != [{'name': '', 'game': -1}, {'name': '', 'game': -1}]:
                if i == 0:
                    # if the match has a neighbor, put it in the appropriate slot
                    # in LR1, else do same in LR2
                    if (j%2 == 1 and bracket["winners"][i]["seeds"][j-1]["teams"] != [{'name': '', 'game': -1}, {'name': '', 'game': -1}]) \
                    or (j%2 == 0 and bracket["winners"][i]["seeds"][j+1]["teams"] != [{'name': '', 'game': -1}, {'name': '', 'game': -1}]):
                        winners[i][j][1][1] = 0
                    else:
                        winners[i][j][1][1] = 1
                    winners[i][j][1][2] = j//2
                    winners[i][j][1][3] = j%2
                    cur = winners[i][j][1]
                    bracket[cur[0]][cur[1]]["seeds"][cur[2]]["teams"][cur[3]]["name"] = [i,j]
                elif i == 1:
                    # LR2 in this case just reverses the matches
                    winners[i][j][1][1] = 1
                    winners[i][j][1][2] = len(bracket["losers"][1]["seeds"])-j-1
                    winners[i][j][1][3] = 0
                    cur = winners[i][j][1]
                    bracket[cur[0]][cur[1]]["seeds"][cur[2]]["teams"][cur[3]]["name"] = [i,j]
                elif i > 1:
                    midindex = len(bracket["losers"][(2 * (i+1)) - 3]["seeds"])//2
                    winners[i][j][1][1] = (2 * (i+1)) - 3
                    if i % 2 == 1:
                        if j < midindex:
                            winners[i][j][1][2] = midindex + j
                        else:
                            winners[i][j][1][2] = j - midindex
                    else:
                        winners[i][j][1][2] = j
                    winners[i][j][1][3] = 0
                    cur = winners[i][j][1]
                    bracket[cur[0]][cur[1]]["seeds"][cur[2]]["teams"][cur[3]]["name"] = [i,j]
    #print(bracket)
    return winners

# This takes in a bracket made by makeBracketFromEntrants and the number of people in that bracket and returns a schema.
# A schema is a set of instructions for where to send the winners and losers of each match in the bracket.
def makeSchemaJSON(bracket2, e):
    bracket = copy.deepcopy(bracket2)
    winners = [[[["winners",j+1,None,None],["losers",None,None,None]] for k in range(len(bracket["winners"][j]["seeds"]))] for j in range(len(bracket["winners"]))]
    losers = [[[["losers",j+1,None,None],"OUT"] for k in range(len(bracket["losers"][j]["seeds"]))] for j in range(len(bracket["losers"]))]
    # Whether or not there are the same number of matches in LR1 and LR2
    # affects how the losers are handled.
    same_next = 0
    if len(bracket["losers"][0]["seeds"]) == len(bracket["losers"][1]["seeds"]):
        #print(len(bracket["losers"][1]["seeds"]))
        same_next = 1
    for i in range(len(winners)-1):
        for j in range(len(winners[i])):
            #print(i, j, bracket["winners"][i], winners[i])
            if bracket["winners"][i]["seeds"][j]["teams"] != [{'name': '', 'game': -1}, {'name': '', 'game': -1}]:
                #print(bracket["winners"][i]["seeds"][j]["teams"])
                if len(winners[i+1]) == len(winners[i]) and i == 0:
                    winners[i][j][0][2] = j
                    winners[i][j][0][3] = 1
                    #print(winners[i][j], "HERE")
                    cur = winners[i][j][0]
                    #print(bracket[cur[0]][cur[1]]["seeds"][cur[2]]["teams"][cur[3]])
                    bracket[cur[0]][cur[1]]["seeds"][cur[2]]["teams"][cur[3]]["name"] = [i,j]
                else:
                    winners[i][j][0][2] = j//2
                    winners[i][j][0][3] = j%2
                    #print(winners[i][j], "HERE")
                    cur = winners[i][j][0]
                    bracket[cur[0]][cur[1]]["seeds"][cur[2]]["teams"][cur[3]]["name"] = [i,j]
    if same_next == 0:
        winners = losersSameNextZeroJSON(winners, bracket)
    else:
        winners = losersSameNextOneJSON(winners, bracket)
    #for row in bracket[0]:
    #    print(row)
    #for row in bracket[1]:
    #    print(row)
    #winners[len(winners)-2][0][0][3] = 0
    for i in range(len(losers)-1):
        #print("losers' round")
        for j in range(len(losers[i])):
            if len(losers[i+1]) == len(losers[i]):
                losers[i][j][0][2] = j
                losers[i][j][0][3] = 1
            else:
                losers[i][j][0][2] = j//2
                losers[i][j][0][3] = j%2
                if j%2 == 0 and bracket["losers"][i]["seeds"][j+1]["teams"] == ["",""]:
                    #print("override", bracket[1][i][j], bracket[1][i][j+1])
                    losers[i][j][0][3] = 1
    schema = [winners, losers]
    return schema