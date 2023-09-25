from scipy.interpolate import InterpolatedUnivariateSpline as Interp
import numpy as np
import nibabel as nib



def create_smiley_with_modulated_mouth(t):
    sz = 100
    r = sz // 2
    #array = np.zeros((sz,sz, sz))
    # Create a circle 
    xx, yy, zz = np.mgrid[:sz, :sz, :sz]
    c = lambda xc, yc, zc: ((xx-xc)**2 + (yy-yc)**2 + (zz-zc)**2 )
    circle =  c(r, r, r) < r*r
    circle = circle.astype(np.uint8)

    outer_r = 25
    inner_r = 20
    center_x = 70
    mouth_r = c(center_x, r, r)
    
    spherical_bounds = np.logical_and(xx-center_x >= outer_r*np.cos(-np.pi/2), xx-center_x <= outer_r*np.cos(0))
    mouth = np.logical_and(np.logical_and(mouth_r < outer_r*outer_r, mouth_r > inner_r*inner_r), spherical_bounds).astype(int)
    mouth = mouth[:,:,50]

    circle[:,:,50][mouth.astype(bool)] = 0

    eye_r = 10
    left_eye =  ((xx-26)**2 + (yy-32)**2 + (zz-r)**2 ) < eye_r*eye_r
    right_eye =  ((xx-26)**2 + (yy-70)**2 + (zz-r)**2 ) < eye_r*eye_r

    circle[left_eye] = 0
    circle[right_eye] = 0
    
    circle[circle!=0]= t

    
    del xx,yy,zz, mouth_r, mouth, left_eye, right_eye,
    return circle

def save_array_asnib(array, save_name):
    img = nib.Nifti1Image(array.astype(np.uint8), np.eye(4))
    nib.save(img, save_name)
    
def create_all_smileys(slice_seq):
    # Creates the ground truth smiley
    modulations = list(range(0, 90, 10))
    smile_ts = np.zeros((99, 99, 40, len(modulations)))
    for i, a in enumerate(modulations):
        smile_ts[:,:,:, i] = create_smiley_with_modulated_mouth(a)[:99,:99, 31:71]   
    save_array_asnib(smile_ts, 'ground_truth_modulation.nii')
    # Creates upsampled modulations to perform the slicing afterwards
    smile_ts_up = np.zeros((99, 99, 40, len(modulations)*slice_seq.shape[0]))
    mods_up = np.linspace(0, 90, smile_ts_up.shape[3])
    for i, a in enumerate(mods_up):
        smile_ts_up[:,:,:, i] = create_smiley_with_modulated_mouth(a)[:99,:99, 31:71]
    save_array_asnib(smile_ts_up, 'ground_truth_upsampled_modulation.nii')
    # Slice the array according to the slice sequence to get the final data to slice-time correct afterwards
    smile_resampled = np.zeros((99, 99, 40, len(modulations)))
    upsampled_mod_id = 0
    for i in range(0, len(modulations)):
        for j in range(0, slice_seq.shape[0]):
            curr_slices = slice_seq[j]
            smile_resampled[:, curr_slices,:, i] = smile_ts_up[:, curr_slices, :, upsampled_mod_id]
            upsampled_mod_id += 1
    save_array_asnib(smile_resampled, 'acquired_modulation.nii')

slice_seq = np.arange(0, 99).reshape((11, - 1))

create_all_smileys(slice_seq)
