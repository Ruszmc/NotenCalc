


def ask():
    selection = input('Do you want to calculate your Note for the test or overall? \n').lower().strip()
    print('')


    if selection == 'overall':
        #--- Get the values ---#
        seminar = input('How many points did you get in the Seminar \n')
        test = input('How many points did you get in the Test \n')

        #--- convert to floats---#
        seminar = float(seminar)
        test = float(test)

        #--- check the conversion, if "true" add your total points together---#
        if test > 50:
            print('You haven`t converted your test result to Seminar points! \n')
            ask()
            return
        ue_test = seminar + test

        #--- calculate result ---#
        allowed_grades = [1, 1.3, 1.7, 2, 2.3, 2.7, 3, 3.3, 3.7, 4, 5]

        result = 1 + 3 * (100 - ue_test) / 50
        closest = min(allowed_grades, key=lambda x: abs(x - result))
        if closest == result:
            print('Your Note is: ' + str(result))
        else:
            print(f'You will probably be getting {closest}, because your grade is {result}')
    elif selection == 'test':
        #--- Get the values ---#
        qst = input('How many questions did the test have? \n')
        poi = input('How many points did you get in the Test? \n')

        #--- convert to floats---#
        poi = float(poi)
        qst = float(qst)

        #--- calculate result ---#
        fac = 50 / qst
        result = poi * fac

        #--- use the right, number ---#
        result = round(result * 4) / 4
        print(result)

        ans = input('Do you also want to calculate more? (y/n)\n').lower()
        if ans == 'y':
            ask()
        else:
            print('Thank you for using this Programm! \n')
    else:
        ask()

print('This Programm is used to calculate your Note.')
print('')

ask()