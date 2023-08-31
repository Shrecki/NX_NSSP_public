import numpy as np
def print_fmri_properties_answer(answers):
    str_answer= ""
    if len(answers) == 0:
        print("Please enter at least one answer!")
    answers = np.unique(np.sort(np.array(answers)))
    for answ in answers:
        if answ == 1:
            str_answer += "1. ✔️ Indeed, fMRI (short for functional MRI) aims to measure fluctuations in time of the MRI signal and does add time to 3D data, hence 4D."
        elif answ == 2:
            str_answer += "2. ❌ Not exactly. Look to the contrast of fMRI compared to MRI: you will immediately notice they differ!"
        elif answ == 3:
            str_answer += "3. ✔️ fMRI aims to measure the blood oxygen level dependent (BOLD) signal."
        elif answ == 4:
            str_answer += "4. ✔️ The actual sequence used depends on the desired contrast in analysis."
        else:
            str_answer += "Please input a number between 1, 2, 3 and 4!"
        str_answer += "\n"
    expected = [1, 2, 3]
    for exp in expected:
        if exp not in answers:
            str_answer += "You might be missing some answers! Check again ;) \n"
            break
    print(str_answer)


def print_answer(answer):
    if answer == 1:
        print("❌ Air does appear dark, as you can see around the brain.\nHowever, ventricles in the human brain store and produce what is called the cerebro-spinal fluid (CSF).")
    elif answer == 2:
        print("✔️ Ventricles do indeed contain liquid, called the  cerebro-spinal fluid (CSF).\nIn T1 contrast, water and CSF appear dark while fat appears white.")
    elif answer == 3:
        print("❌ Fat in T1 contrast actually appears white! Look on the left-most image (called axial view).\nOn the bottom leftmost part, you actually see the back of the neck. Notice the little white area? It is a padding of fat!")
    else:
        print("Select a number between 1, 2 or 3!")


def print_answer_contrast(answer):
    if answer == 1:
        print("❌ Check the ventricles for example")
    elif answer == 2:
        print("✔️ Correct!")
    else:
        print("Select a number between 1 and 2!")
