import numpy as np
from IPython.display import display

def print_fmri_properties_answer(answers):
    if len(answers) == 0:
        display("Please enter at least one answer!")
    answers = np.unique(np.sort(np.array(answers)))
    for answ in answers:
        if answ == 1:
            display("1. ✔️ Indeed, fMRI (short for functional MRI) aims to measure fluctuations in time of the MRI signal and does add time to 3D data, hence 4D.")
        elif answ == 2:
            display("2. ❌ Not exactly. Look to the contrast of fMRI compared to MRI: you will immediately notice they differ!")
        elif answ == 3:
            display("3. ✔️ fMRI aims to measure the blood oxygen level dependent (BOLD) signal.")
        elif answ == 4:
            display("4. ✔️ The actual sequence used depends on the desired contrast in analysis.")
        else:
            display("Please input a number between 1, 2, 3 and 4!")
    expected = [1,3,4]
    for exp in expected:
        if exp not in answers and len(answers) > 0:
            display("You might be missing some answers! Check again ;)")
            break

def print_answer(answer):
    if answer == 1:
        display("❌ Air does appear dark, as you can see around the brain.\nHowever, ventricles in the human brain store and produce what is called the cerebro-spinal fluid (CSF).")
    elif answer == 2:
        display("✔️ Ventricles do indeed contain liquid, called the  cerebro-spinal fluid (CSF).\nIn T1 contrast, water and CSF appear dark while fat appears white.")
    elif answer == 3:
        display("❌ Fat in T1 contrast actually appears white! Look on the left-most image (called axial view).\nOn the bottom leftmost part, you actually see the back of the neck. Notice the little white area? It is a padding of fat!")
    else:
        display("Select a number between 1, 2 or 3!")


def print_answer_contrast(answer):
    if answer == 1:
        display("❌ Check the ventricles for example")
    elif answer == 2:
        display("✔️ Correct!")
    else:
        display("Select a number between 1 and 2!")
