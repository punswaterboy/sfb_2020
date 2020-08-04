import statistics
import scipy.stats
import random as r
import numpy as np
import pandas as pd
# playoff odds sim
# determines playoff odds, given schedule, record, odds of winning
# does not account for tiebreaker, h2h record into coin flip

# for loop for each type of roster score used
# sim multiple, average of sims

# weekly input changes:
# week, roster scores, wins for each team

# define team class
class Team:
    def __init__(self,name,wins,schedule,p_score,week_check, avg, std):

        self.name = name
        self.wins = wins
        self.schedule = schedule
        # change depending on weeks passed
        self.week_check = week_check
        if std == 0:
            zs = 1
            #print('hmm')
        else:
            zs = (p_score - avg) / std
            #print('hmm2')
        self.prob = 1-scipy.stats.norm.sf(zs)
        self.playoff_count = 0
        # print(p_score, 'p_score', name)
        # print(avg, 'avg')
        # print(std)
        # print(zs)
        # print((avg - 1))
        # print(self.prob, 'prob', name)

def multi_sim(sims,teams,week):
        sim_sum = np.zeros((sims, 6))
        playoff_sum = np.zeros((sims, 6))
        week_check_constant = [teams[0].week_check, teams[1].week_check, teams[2].week_check, teams[3].week_check, teams[4].week_check, teams[5].week_check]
        wins_constant = [teams[0].wins, teams[1].wins, teams[2].wins, teams[3].wins, teams[4].wins, teams[5].wins]
        for sim_count in range(sims):

            for n in range(week - 1, week_max - 1):
                # print(n)
                for i in teams:
                    t1 = i
                    # for j in t1.schedule:
                    j = t1.schedule[n]
                    # print(j)
                    t2 = next(x for x in teams if x.name == j)
                    # print(t1.name, t2.name)
                    # print(t1.week_check, t2.week_check)
                    if t1.week_check == n and t2.week_check == n:
                        add_wins(t1, t2)
                        #print(t1.name,t2.name, n)
            win_list_input = []
            for i in range(6):
                win_list_input.append(teams[i].wins)
                sim_sum[sim_count, i] = teams[i].wins
                teams[i].week_check = week_check_constant[i]
                teams[i].wins = wins_constant[i]
            playoff_calc(win_list_input,teams)

        avgs = np.divide([sum(x) for x in zip(*sim_sum)], sims)
        #print(sim_sum)
        playoff_avgs = []

        for i in range(6):
            playoff_avgs.append(round(100*teams[i].playoff_count/sims,1))
            teams[i].playoff_count = 0

        #return avgs
        return playoff_avgs


def add_wins(t1, t2):
    x = 100 * t1.prob / (t1.prob + t2.prob)
    # print(x)
    if x < 11:
        tie = x
        w1 = 0
        w2 = 100 - x
    elif 100 - x < 11:
        tie = 100 - x
        w1 = x
        w2 = 0
    else:
        tie = 11
        w1 = 89 * t1.prob / (t1.prob + t2.prob)
        w2 = 89 * t2.prob / (t1.prob + t2.prob)
    # print(tie, w1, w2)
    rng = r.random() * 100
    # print(rng)
    if rng < tie:
        t1.wins += 0.5
        t2.wins += 0.5
    elif rng < tie + w1:
        t1.wins += 1
    else:
        t2.wins += 1
    t1.week_check += 1
    t2.week_check += 1

def playoff_calc(win_list, teams):
    #sr = pd.Series(win_list)
    #result = sr.rank(method='min', ascending=False)
    less4 = True
    playoff_teams_left = 4
    temp = 1
    win_list_edit = win_list[:]
    while less4:
        temp = max(win_list_edit)
        res = [i for i, j in enumerate(win_list) if j == temp]
        popres = [i for i, j in enumerate(win_list_edit) if j == temp]
        #print(res)
        # have the indices of the top teams in standings in a list
        if 4 >= playoff_teams_left - len(res) >= 0:
            for idx, k in reversed(list(enumerate(res))):
                teams[k].playoff_count += 1
                playoff_teams_left -= 1
                #print(idx, 'idx')
                #print(popres,'popes')
                win_list_edit.pop(popres[idx])
        elif playoff_teams_left - len(res) < 0:
            points = playoff_teams_left / len(res)
            for k in res:
                teams[k].playoff_count += points
                playoff_teams_left -= 1

        if playoff_teams_left <= 0:
            less4 = False

    # roster score analysis
score_list = []
descrip_list = []
# dylan, tyler, jchu, burch, chow, coach
score_list.append([43, 41, 40, 33.5, 32.5, 20])
descrip_list.append('Preseason Roster Scores')
# 50-50
#scores = [50, 50, 50, 50, 50, 50]
score_list.append([50, 50, 50, 50, 50, 50])
descrip_list.append('Coin Flips')
# 50-50 coach adj
#scores = [50, 50, 50, 50, 50, 25]
score_list.append([50, 50, 50, 50, 50, 25])
descrip_list.append('Coin Flips Coach Sucks')
# week 1 roster score
#scores = [29.5, 55, 37.5, 31, 29, 28]
score_list.append([29.5, 55, 37.5, 31, 29, 28])
descrip_list.append('Week 1 Roster Scores')
# week 1 / preseason average
#scores = [36.25, 48, 38.75, 32.25, 30.75, 24]
score_list.append([36.25, 48, 38.75, 32.25, 30.75, 24])
descrip_list.append('Average(W1,Pre) Roster Scores')

just_avg_list = []
just_avg_list.append([36.25, 48, 38.75, 32.25, 30.75, 24])

# stops for loop at 6
week_max = 7
def reg_anal(p_score_list):
    columns = ['Tyler', 'Dylan', 'Coach', 'Chow', 'Burch', 'Jchu']
    df1 = pd.DataFrame(columns=columns)
    #for score_idx, scores in enumerate(score_list):
    for score_idx, scores in enumerate(p_score_list):
        avg = statistics.mean(scores)
        std = statistics.stdev(scores)
        zs = list()
        for i in range(len(scores)):
            if std == 0:
                zs.append(1)
            else:
                zs.append((scores[i] - avg) / std)
        #print(zs)
        #print(scores)
        # print(avg, 'avg')
        # print(std, 'std')

        p_values = list()
        for i in range(len(scores)):
            p_values.append(1-scipy.stats.norm.sf(zs[i]))

        #set week
        week = 2

        team_1 = Team('Tyler', 1, ['Dylan', 'Coach', 'Jchu', 'Burch', 'Chow', 'Dylan'], scores[1], week - 1, avg, std)
        team_2 = Team('Dylan', 0, ['Tyler', 'Burch', 'Coach', 'Chow', 'Jchu', 'Tyler'], scores[0], week - 1, avg, std)
        team_3 = Team('Coach', .5, ['Chow', 'Tyler', 'Dylan', 'Jchu', 'Burch', 'Chow'], scores[5], week - 1, avg, std)
        team_4 = Team('Chow', .5, ['Coach', 'Jchu', 'Burch', 'Dylan', 'Tyler', 'Coach'], scores[4], week - 1, avg, std)
        team_5 = Team('Burch', 0, ['Jchu', 'Dylan', 'Chow', 'Tyler', 'Coach', 'Jchu'], scores[3], week - 1, avg, std)
        team_6 = Team('Jchu', 1, ['Burch', 'Chow', 'Tyler', 'Coach', 'Dylan', 'Burch'], scores[2], week - 1, avg, std)

        # preseason
        # team_1 = Team('Tyler', 0, ['Dylan', 'Coach', 'Jchu', 'Burch', 'Chow', 'Dylan'], scores[1])
        # team_2 = Team('Dylan', 0, ['Tyler', 'Burch', 'Coach', 'Chow', 'Jchu', 'Tyler'], scores[0])
        # team_3 = Team('Coach', 0, ['Chow','Tyler', 'Dylan', 'Jchu', 'Burch', 'Chow'], scores[5])
        # team_4 = Team('Chow', 0, ['Coach', 'Jchu', 'Burch', 'Dylan', 'Tyler', 'Coach'], scores[4])
        # team_5 = Team('Burch', 0, ['Jchu','Dylan', 'Chow', 'Tyler','Coach','Jchu'], scores[3])
        # team_6 = Team('Jchu', 0, ['Burch', 'Chow','Tyler','Coach','Dylan','Burch'], scores[2])

        # week 2 hypo
        # team_1 = Team('Tyler', 1, ['Dylan', 'Coach', 'Jchu', 'Burch', 'Chow', 'Dylan'], scores[1], week - 1)
        # team_2 = Team('Dylan', 0, ['Tyler', 'Burch', 'Coach', 'Chow', 'Jchu', 'Tyler'], scores[0], week - 1)
        # team_3 = Team('Coach', .5, ['Chow','Tyler', 'Dylan', 'Jchu', 'Burch', 'Chow'], scores[5], week - 1)
        # team_4 = Team('Chow', .5, ['Coach', 'Jchu', 'Burch', 'Dylan', 'Tyler', 'Coach'], scores[4], week - 1)
        # team_5 = Team('Burch', 0, ['Jchu','Dylan', 'Chow', 'Tyler','Coach','Jchu'], scores[3], week - 1)
        # team_6 = Team('Jchu', 1, ['Burch', 'Chow','Tyler','Coach','Dylan','Burch'], scores[2], week - 1)

        teams = [team_1, team_2, team_3, team_4, team_5, team_6]

        # how many sims
        sim_num = 100000

        please = multi_sim(sim_num,teams,week)

        #print(score_idx)
        print(descrip_list[score_idx])
        print(please)
        df1.loc[len(df1)] = please
        df1.rename({df1.index[-1]: descrip_list[score_idx]}, inplace=True)
    df1.to_excel("output.xlsx")
# hypothetical
def hypothetical(p_score_list):
    columns = ['Tyler', 'Dylan', 'Coach', 'Chow', 'Burch', 'Jchu']
    df1 = pd.DataFrame(columns=columns)
    for score_idx, scores in enumerate(p_score_list):
        avg = statistics.mean(scores)
        std = statistics.stdev(scores)
        zs = list()
        for i in range(len(scores)):
            if std == 0:
                zs.append(1)
            else:
                zs.append((scores[i] - avg) / std)
        # print(zs)

        p_values = list()
        for i in range(len(scores)):
            p_values.append(1 - scipy.stats.norm.sf(zs[i]))

        # set week
        week = 2

        team_1 = Team('Tyler', 1, ['Dylan', 'Coach', 'Jchu', 'Burch', 'Chow', 'Dylan'], scores[1], week - 1, avg, std)
        team_2 = Team('Dylan', 0, ['Tyler', 'Burch', 'Coach', 'Chow', 'Jchu', 'Tyler'], scores[0], week - 1, avg, std)
        team_3 = Team('Coach', .5, ['Chow', 'Tyler', 'Dylan', 'Jchu', 'Burch', 'Chow'], scores[5], week - 1, avg, std)
        team_4 = Team('Chow', .5, ['Coach', 'Jchu', 'Burch', 'Dylan', 'Tyler', 'Coach'], scores[4], week - 1, avg, std)
        team_5 = Team('Burch', 0, ['Jchu', 'Dylan', 'Chow', 'Tyler', 'Coach', 'Jchu'], scores[3], week - 1, avg, std)
        team_6 = Team('Jchu', 1, ['Burch', 'Chow', 'Tyler', 'Coach', 'Dylan', 'Burch'], scores[2], week - 1, avg, std)

        teams = [team_1, team_2, team_3, team_4, team_5, team_6]

        # how many sims
        sim_num = 100000

        please = multi_sim(sim_num, teams, week)
        df1.loc[len(df1)] = please
        df1.rename({df1.index[-1]: 'baseline'}, inplace=True)

        # print(score_idx)
        #print(descrip_list[score_idx])
        print(please)
        for team_num in range(6):
            for posneg in range(3):

                avg = statistics.mean(scores)
                std = statistics.stdev(scores)
                zs = list()
                for i in range(len(scores)):
                    if std == 0:
                        zs.append(1)
                    else:
                        zs.append((scores[i] - avg) / std)

                p_values = list()
                for i in range(len(scores)):
                    p_values.append(1-scipy.stats.norm.sf(zs[i]))

                #set week
                week = 2

                team_1 = Team('Tyler', 1, ['Dylan', 'Coach', 'Jchu', 'Burch', 'Chow', 'Dylan'], scores[1], week - 1, avg, std)
                team_2 = Team('Dylan', 0, ['Tyler', 'Burch', 'Coach', 'Chow', 'Jchu', 'Tyler'], scores[0], week - 1, avg, std)
                team_3 = Team('Coach', .5, ['Chow','Tyler', 'Dylan', 'Jchu', 'Burch', 'Chow'], scores[5], week - 1, avg, std)
                team_4 = Team('Chow', .5, ['Coach', 'Jchu', 'Burch', 'Dylan', 'Tyler', 'Coach'], scores[4], week - 1, avg, std)
                team_5 = Team('Burch', 0, ['Jchu','Dylan', 'Chow', 'Tyler','Coach','Jchu'], scores[3], week - 1, avg, std)
                team_6 = Team('Jchu', 1, ['Burch', 'Chow','Tyler','Coach','Dylan','Burch'], scores[2], week - 1, avg, std)


                teams = [team_1, team_2, team_3, team_4, team_5, team_6]

                # modify teams
                # wins
                if posneg == 0:
                    teams[team_num].wins += 1
                    t2_name = teams[team_num].schedule[teams[team_num].week_check]
                    teams[team_num].week_check += 1
                    t2_posneg = next(x for x in teams if x.name == t2_name)
                    t2_posneg.week_check += 1
                elif posneg == 1:
                    #loss
                    #teams[team_num].wins += 1
                    t2_name = teams[team_num].schedule[teams[team_num].week_check]
                    teams[team_num].week_check += 1
                    t2_posneg = next(x for x in teams if x.name == t2_name)
                    t2_posneg.week_check += 1
                    t2_posneg.wins += 1
                else:
                    # tie
                    teams[team_num].wins += 0.5
                    t2_name = teams[team_num].schedule[teams[team_num].week_check]
                    teams[team_num].week_check += 1
                    t2_posneg = next(x for x in teams if x.name == t2_name)
                    t2_posneg.week_check += 1
                    t2_posneg.wins += 0.5
                # how many sims
                sim_num = 100000

                please = multi_sim(sim_num, teams, week)
                df1.loc[len(df1)] = please
                #print(please)
                #print(df1)
                #print(score_idx)
                #print(teams[team_num].name)
                if posneg == 0:
                    prnt_this = teams[team_num].name, ' win'
                    print(prnt_this)
                    df1.rename({df1.index[-1]: prnt_this}, inplace=True)
                    # print(teams[team_num].name, ' win')
                elif posneg == 1:
                    prnt_this = teams[team_num].name, ' lose'
                    print(prnt_this)
                    df1.rename({df1.index[-1]: prnt_this}, inplace=True)
                else:
                    prnt_this = teams[team_num].name, ' tie'
                    print(prnt_this)
                    df1.rename({df1.index[-1]: prnt_this}, inplace=True)
                print(please)
                #print(df1)
        df1.to_excel("output.xlsx")

#print(just_avg_list)
# run hypothetical
#hypothetical(just_avg_list)
# run regular
reg_anal(score_list)
#print(team_1.wins, team_2.wins, team_3.wins,team_4.wins, team_5.wins, team_6.wins )
print('Tyler, Dylan, Coach, Chow, Burch, Jchu')



#print(std)
#for i in teams:
    #print(i.name, i.wins, i.prob)

# finding tie chance
# 6 ties, 66 total
# ties = 0
# total = 0
# for i in range(11):
#     for j in range(11-i):
#         k = 10-j-i
#         total += 1
#         if j == k:
#             ties += 1
#         print(i,j,k)
#
# print(ties,' ties')
# print(total, ' total')
