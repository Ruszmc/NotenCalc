def ask():
    selection = input('Do you want to calculate your Note for the test or overall? \n').lower().strip()
    print('')

    if selection == 'overall':
        overall()
    elif selection == 'test':
        test()
    else:
        ask()


def overall(test_result=None):

    # --- Get the values ---#
    if test_result is not None:
        test = float(test_result)
        print('Your Test result was: ' + str(test_result))
    else:
        test = float(input('How many points did you get in the Test \n'))

    seminar = float(input('How many points did you get in the Seminar \n'))

    # --- check the conversion, if "true" add your total points together---#
    if test > 50:
        print('You haven`t converted your test result to Seminar points! \n')
        ask()
        return
    ue_test = seminar + test

    grade(ue_test)


def test():
    # --- Get the values ---#
    qst = input('How many questions did the test have? \n')
    poi = input('How many points did you get in the Test? \n')

    # --- convert to floats---#
    poi = float(poi)
    qst = float(qst)

    # --- calculate result ---#
    fac = 50 / qst
    result = poi * fac

    # --- use the right, number ---#
    result = round(result * 4) / 4
    print(result)

    ans = input('Do you also want to calculate your overall score? (y/n)\n').lower()
    if ans == 'y':
        overall(result)
    else:
        print('Thank you for using this Programm! \n')

def snap(x):
    return round(x*4) /4

def grade(points):
    # --- calculate result ---#
    allowed_grades = [1, 1.3, 1.7, 2, 2.3, 2.7, 3, 3.3, 3.7, 4, 5]

    result = 1 + 3 * (100 - points) / 50
    closest = min(allowed_grades, key=lambda x: abs(x - result))

    print(f'You are probably getting {closest}, because your grade is {result:.3f}')

    index = allowed_grades.index(closest)

    better = None
    worse = None

    if index > 0:
        better = allowed_grades[index - 1]
    if index < len(allowed_grades) - 1:
        worse = allowed_grades[index + 1]

    if better is not None:
        better_threshold = 100 - (better - 1) * 50 / 3
        missing = max(0, better_threshold - points)
        print(f'To get the better grade, you need to get {snap(missing)} points.')
    if worse is not None:
        worse_threshold = 100 - (worse - 1) * 50 / 3
        buffer = max(0, points - worse_threshold)
        print(f'To get a worse grade, you need to loose {snap(buffer)} points.')


print('This Programm is used to calculate your Note.')
print('')

ask()