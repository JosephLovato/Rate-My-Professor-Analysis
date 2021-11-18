import getpass 
import pg8000
import matplotlib.pyplot as plt
import numpy as np
import re
import textparser
from tabulate import tabulate

NUM_TOP_WORDS = 15

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(f"{bcolors.OKGREEN}Logging in to database...{bcolors.ENDC}")
user = 'jlovato'
secret = 'agzC<[]&7qD#B<U_'
db = pg8000.connect(user=user, password=secret, host='codd.mines.edu', port=5433, database='csci403')
cursor = db.cursor()

########################  Section 1: Ratings and Difficulty ###################################
# 1.0 Average Professor Rating (General)
print(f"{bcolors.HEADER}1.0 Average Professor Rating (General){bcolors.ENDC}")
cursor.execute("SELECT avg(student_star) FROM rate_my_professor")
results = cursor.fetchall()
print("\tAverage General Rating: " + str(results[0][0]))

# 1.1 Average Professor Rating (Chemistry)
print(f"{bcolors.HEADER}1.1 Average Professor Rating (Chemistry){bcolors.ENDC}")
cursor.execute("Select avg(student_star) FROM rate_my_professor WHERE department_name = 'Chemistry department'")
results = cursor.fetchall()
print("\tAverage Chemistry Rating: " + str(results[0][0]))

# 1.2 Average Professor Rating (Computer Science)
print(f"{bcolors.HEADER}1.2 Average Professor Rating (Computer Science){bcolors.ENDC}")
cursor.execute("Select avg(student_star) FROM rate_my_professor WHERE department_name = 'Computer Science department'")
results = cursor.fetchall()
print("\tAverage CS Rating: " + str(round(results[0][0], 3)))

# 1.3 Average Professor Difficulty (General)
print(f"{bcolors.HEADER}1.3 Average Professor Difficulty (General){bcolors.ENDC}")
cursor.execute("SELECT avg(student_difficult) FROM rate_my_professor")
results = cursor.fetchall()
print("\tAverage General Difficulty: " + str(results[0][0]))

# 1.4 Average Professor Difficulty (Chemistry)
print(f"{bcolors.HEADER}1.4 Average Professor Difficulty (Chemistry){bcolors.ENDC}")
cursor.execute("Select avg(student_difficult) FROM rate_my_professor WHERE department_name = 'Chemistry department'")
results = cursor.fetchall()
print("\tAverage Chemistry Difficulty: " + str(results[0][0]))

# 1.5 Average Professor Difficulty (Computer Science)
print(f"{bcolors.HEADER}1.5 Average Professor Difficulty (Computer Science){bcolors.ENDC}")
cursor.execute("Select avg(student_difficult) FROM rate_my_professor WHERE department_name = 'Computer Science department'")
results = cursor.fetchall()
print("\tAverage CS Difficulty: " + str(round(results[0][0], 3)))


# 1.6 Departmental Average Ratings
print(f"{bcolors.HEADER}1.6 Creating plot for Departmental Average Ratings{bcolors.ENDC}")
cursor.execute(
    """SELECT department_name, avg(student_star) FROM rate_my_professor 
    WHERE department_name like '%Engineering%'
    or department_name IN (SELECT department_name FROM rate_my_professor GROUP BY department_name HAVING count(department_name) > 400)
    GROUP BY department_name ORDER BY avg(student_star)""")
results = cursor.fetchall()
departments = list(t[0] for t in results)
departments = [re.sub("department", "", dept) for dept in departments]
ratings = list(t[1] for t in results)
plt.bar(departments, ratings)
plt.ylim([0,5])
plt.draw()
plt.xticks(rotation=45, ha='right')
plt.xlabel('Department')
plt.ylabel('Average Rating')
xlocs, xlabs = plt.xticks()
for i, v in enumerate(ratings):
    plt.text(xlocs[i] - 0.35, v + 0.05, str(round(v, 1)))
plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(9, 5)
plt.savefig("plots/Department_rating.png")
plt.clf()

# 1.7 Departmental Difficulty Ratings
print(f"{bcolors.HEADER}1.7 Creating plot for Departmental Difficulty{bcolors.ENDC}")
cursor.execute("""SELECT department_name, avg(student_difficult) FROM rate_my_professor 
    WHERE department_name like '%Engineering%'
    or department_name IN (SELECT department_name FROM rate_my_professor GROUP BY department_name HAVING count(department_name) > 400)
    GROUP BY department_name ORDER BY avg(student_difficult)""")
results = cursor.fetchall()
departments = list(t[0] for t in results)
departments = [re.sub("department", "", dept) for dept in departments]
ratings = list(t[1] for t in results)
plt.bar(departments, ratings)
plt.ylim([0,5])
plt.draw()
plt.xticks(rotation=45, ha='right')
plt.xlabel('Department')
plt.ylabel('Average Difficulty')
xlocs, xlabs = plt.xticks()
for i, v in enumerate(ratings):
    plt.text(xlocs[i] - 0.35, float(v) + 0.05, str(round(v, 1)))
plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(9, 5)
plt.savefig("plots/Department_difficulty.png")
plt.clf()

########################  Section 2: Most Common Department Comment Words ###################################

# 2.0 Word frequency in all comments
print(f"{bcolors.OKCYAN}2.0 Most Common Words Comment Words (General){bcolors.ENDC}")
cursor.execute("SELECT comments FROM rate_my_professor")
results = cursor.fetchall()
cursor.execute("SELECT count(*) FROM rate_my_professor")
num_students = cursor.fetchall()[0][0]
all_comments = ""
for comment in results:
    try: 
        all_comments += comment[0] + " "
    except:
        pass      
tp = textparser.textparser(all_comments)
words = tp.most_freq_words(NUM_TOP_WORDS, True)
words_more = [(e[0], e[1], e[1] / num_students) for e in words.items()]
print(tabulate(words_more, headers=['Word', 'Freq', "# Word / Comment"], tablefmt='orgtbl'))

# 2.1 Word frequency in Chemistry department comments
print(f"{bcolors.OKCYAN}2.1 Most Common Words Comment Words (Chemistry){bcolors.ENDC}")
cursor.execute("SELECT comments FROM rate_my_professor WHERE department_name = 'Chemistry department'")
results = cursor.fetchall()
cursor.execute("SELECT count(*) FROM rate_my_professor WHERE department_name = 'Chemistry department'")
num_chem_students = cursor.fetchall()[0][0]
all_chemistry_comments = ""
for comment in results:
    all_chemistry_comments += comment[0] + " "
tp_chem = textparser.textparser(all_chemistry_comments)
words = tp_chem.most_freq_words(NUM_TOP_WORDS, True)
words_more = [(e[0], e[1], e[1] / num_chem_students) for e in words.items()]
print(tabulate(words_more, headers=['Word', 'Freq', "# Word / Comment"], tablefmt='orgtbl'))

# 2.2 Word frequency in Computer Science department comments
print(f"{bcolors.OKCYAN}2.2 Most Common Words Comment Words (Computer Science){bcolors.ENDC}")
cursor.execute("SELECT comments FROM rate_my_professor WHERE department_name = 'Computer Science department'")
results = cursor.fetchall()
cursor.execute("SELECT count(*) FROM rate_my_professor WHERE department_name = 'Computer Science department'")
num_cs_students = cursor.fetchall()[0][0]
all_cs_comments = ""
for comment in results:
    all_cs_comments += comment[0] + " "
tp_cs = textparser.textparser(all_cs_comments)
words = tp_cs.most_freq_words(NUM_TOP_WORDS, True)
words_more = [(e[0], e[1], e[1] / num_cs_students) for e in words.items()]
print(tabulate(words_more, headers=['Word', 'Freq', "# Word / Comment"], tablefmt='orgtbl'))

########################  Section 3: Most Common Rating Comment Words ###################################

# 3.0 Word frequency 1-1.5 star ratings
print(f"{bcolors.FAIL}3.0 Most Common 1-1.5 Star Rating Comment Words {bcolors.ENDC}")
cursor.execute("SELECT comments FROM rate_my_professor WHERE student_star = 1.0 or student_star = 1.5")
results = cursor.fetchall()
cursor.execute("SELECT count(*) FROM rate_my_professor WHERE student_star = 1.0 or student_star = 1.5")
num_onestar_students = cursor.fetchall()[0][0]
print("Number of Ratings: ", num_onestar_students)
all_comments = ""
for comment in results:
    try: 
        all_comments += comment[0] + " "
    except:
        pass      
tp = textparser.textparser(all_comments)
words = tp.most_freq_words(NUM_TOP_WORDS, True)
print(tabulate(words.items(), headers=['Word', 'Freq'], tablefmt='orgtbl'))

# 3.1 Word frequency 2-2.5 star ratings
print(f"{bcolors.FAIL}3.1 Most Common 2-2.5 Star Rating Comment Words {bcolors.ENDC}")
cursor.execute("SELECT comments FROM rate_my_professor WHERE student_star = 2.0 or student_star = 2.5")
results = cursor.fetchall()
cursor.execute("SELECT count(*) FROM rate_my_professor WHERE student_star = 2.0 or student_star = 2.5")
num_twostar_students = cursor.fetchall()[0][0]
print("Number of Ratings: ", num_twostar_students)
all_comments = ""
for comment in results:
    try: 
        all_comments += comment[0] + " "
    except:
        pass      
tp = textparser.textparser(all_comments)
words = tp.most_freq_words(NUM_TOP_WORDS, True)
print(tabulate(words.items(), headers=['Word', 'Freq'], tablefmt='orgtbl'))

# 3.2 Word frequency 3-3.5 star ratings
print(f"{bcolors.FAIL}3.2 Most Common 3-3.5 Star Rating Comment Words {bcolors.ENDC}")
cursor.execute("SELECT comments FROM rate_my_professor WHERE student_star = 3.0 or student_star = 3.5")
results = cursor.fetchall()
cursor.execute("SELECT count(*) FROM rate_my_professor WHERE student_star = 3.0 or student_star = 3.5")
num_threestar_students = cursor.fetchall()[0][0]
print("Number of Ratings: ", num_threestar_students)
all_comments = ""
for comment in results:
    try: 
        all_comments += comment[0] + " "
    except:
        pass      
tp = textparser.textparser(all_comments)
words = tp.most_freq_words(NUM_TOP_WORDS, True)
print(tabulate(words.items(), headers=['Word', 'Freq'], tablefmt='orgtbl'))

# 3.3 Word frequency 4-4.5 star ratings
print(f"{bcolors.FAIL}3.3 Most Common 4-4.5 Star Rating Comment Words {bcolors.ENDC}")
cursor.execute("SELECT comments FROM rate_my_professor WHERE student_star = 4.0 or student_star = 4.5")
results = cursor.fetchall()
cursor.execute("SELECT count(*) FROM rate_my_professor WHERE student_star = 4.0 or student_star = 4.5")
num_fourstar_students = cursor.fetchall()[0][0]
print("Number of Ratings: ", num_fourstar_students)
all_comments = ""
for comment in results:
    try: 
        all_comments += comment[0] + " "
    except:
        pass      
tp = textparser.textparser(all_comments)
words = tp.most_freq_words(NUM_TOP_WORDS, True)
print(tabulate(words.items(), headers=['Word', 'Freq'], tablefmt='orgtbl'))

# 3.4 Word frequency 5 star ratings
print(f"{bcolors.FAIL}3.4 Most Common 5 Star Rating Comment Words {bcolors.ENDC}")
cursor.execute("SELECT comments FROM rate_my_professor WHERE student_star = 5.0")
results = cursor.fetchall()
cursor.execute("SELECT count(*) FROM rate_my_professor WHERE student_star = 5.0")
num_fivestar_students = cursor.fetchall()[0][0]
print("Number of Ratings: ", num_fivestar_students)
all_comments = ""
for comment in results:
    try: 
        all_comments += comment[0] + " "
    except:
        pass      
tp = textparser.textparser(all_comments)
words = tp.most_freq_words(NUM_TOP_WORDS, True)
print(tabulate(words.items(), headers=['Word', 'Freq'], tablefmt='orgtbl'))

########################  Section 4: Curse Words ###################################

# 4.0 
print(f"{bcolors.WARNING}4.0 Average Rating for Comments with Curse Words {bcolors.ENDC}")
cursor.execute("SELECT avg(student_star) FROM rate_my_professor WHERE comments LIKE '%****%'")
results = cursor.fetchall()
print("\tAverage Curse Word Comment Rating: " + str(results[0][0]))


print(f"{bcolors.WARNING}4.0 Average Rating for Comments with Curse Words {bcolors.ENDC}")
cursor.execute("SELECT department_name, count(*) FROM rate_my_professor WHERE comments LIKE '%****%' GROUP BY department_name ORDER BY count(*) DESC")
results = cursor.fetchall()
cursor.execute("SELECT department_name, count(*) FROM rate_my_professor GROUP BY department_name")
totals = cursor.fetchall()
total_dict = dict(totals)
percent_curse = {}
for result in results:
    percent_curse[result[0]] = 100.0 * ( result[1] / total_dict[result[0]] )
sorted_tuples = sorted(percent_curse.items(), key=lambda item: item[1], reverse=True)
for i in range(5):
    print("\t", sorted_tuples[i][0], ': ', round(sorted_tuples[i][1], 3), "% comments with curse words")



