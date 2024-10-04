async def importFSLasync():
    #load fsl module
    import lmod
    import os
    await lmod.purge(force=True)
    await lmod.load('fsl/6.0.7.4')
    await lmod.list()

def loadFSL():
    """
    Function to load FSL 6.0.7.4 module
    Ensures proper environment variables are setup.
    This function should be called at the start of any
    notebook which relies in any capacity on FSL.
    
    If you wish to change the FSL version being used,
    you should edit within the load AND FSLDIR the version.
    Make sure it exists in the neurodocker image before changing it!
    """
    import asyncio
    import os
    # We need to do the import asynchronously, as modules rely on await within
    #asyncio.run(importFSLasync())
    os.environ["FSLDIR"]="/cvmfs/neurodesk.ardc.edu.au/containers/fsl_6.0.7.4_20231005/fsl_6.0.7.4_20231005.simg/opt/fsl-6.0.7.4/"
    os.environ["FSLOUTPUTTYPE"]="NIFTI_GZ"
    os.environ["SINGULARITY_BINDPATH"]="/data,/neurodesktop-storage,/tmp,/cvmfs"


def mkdir_no_exist(path):
    """
    Function to create a directory if it does not exist already.

    Parameters
    ----------
    path: string
        Path to create
    """
    import os
    import os.path as op
    if not op.isdir(path):
        os.makedirs(path)

class FSLeyesServer:
    """
    An FSL eyes class to manipulate frame and context across notebook.
    
    
    Attributes
    ----------
    overlayList: object
        List of overlays, the images displayed within FSLeyes. Each image is a separate overlay
    displayCtx: object
        Display context
    frame: object
        Frame used to display and interact with FSLeyes
    ortho: object
        View panel in orthographic mode
        
    Examples
    --------
    >>>> %gui wx # Do not forget to use this in a notebook!
    >>>> from utils import FSLeyesServer
    >>>> fsleyesDisplay = FSLeyesServer()
    >>>> fsleyesDisplay.show()
    
    It is not a server in the most proper sense, but merely a convenience wrapper.
    Before initializing this class, always make sure you call %gui wx in a cell of the notebook
    to enable GUI integration.
    """
    def __init__(self):
        import fsleyes
        from fsleyes.views.orthopanel import OrthoPanel
        overlayList, displayCtx, frame = fsleyes.embed()
        ortho = frame.addViewPanel(OrthoPanel)
        self.overlayList = overlayList
        self.displayCtx = displayCtx
        self.frame = frame
        self.ortho = ortho
    def show(self):
        """
        Show the current frame interactively.
        """
        self.frame.Show()

    def setOverlayCmap(self,overlayNbr,cmap):
        self.displayCtx.getOpts(self.overlayList[overlayNbr]).cmap = 'Render3'
    
    def resetOverlays(self):
        """
        Remove all overlays from the current frame
        """
        from fsleyes.views.orthopanel import OrthoPanel
    
        while len(self.overlayList) > 0:
            del self.overlayList[0]

        self.frame.removeViewPanel(self.frame.viewPanels[0])
        # Put back an ortho panel in our viz for future displays
        self.frame.addViewPanel(OrthoPanel)
    
    def load(self,image_path):
        """
        Add a Nifti image to the current frame as a new overlay

        Parameters
        ----------
        image_path:  string
            Path to the Nifti image to add to the frame.
            
        Example
        -------
        >>>> %gui wx # Do not forget to use this in a notebook!
        >>>> from utils import FSLeyesServer
        >>>> fsleyesDisplay = FSLeyesServer() 
        >>>> fsleyesDisplay.load(op.expandvars('$FSLDIR/data/standard/MNI152_T1_0.5mm'))
        >>>> fsleyesDisplay.show()
        """
        from fsl.data.image import Image
        import fsleyes.data.tractogram as trk
        if ".trk" in image_path:
            trk_overlay = trk.Tractogram(image_path)
            self.overlayList.append(trk_overlay)
        else:
            self.overlayList.append(Image(image_path))
    def close(self):
        """
        Closes the server and free up resources.
        """
        import fsleyes
    
        self.frame.Close()
        fsleyes.shutdown()

def fsleyes_thread():
    """
    Function to run the FSLeyesServer in a separate thread.
    This function keeps the server running indefinitely.
    """
    fsleyesDisplay = FSLeyesServer()
    fsleyesDisplay.show()
    
    # Keep the thread alive
    while True:
        time.sleep(1)

def extract_question_week(weekNbr, qNbr):
    """
    Function to extract a question for a given week from the companion mca.json of the given week.
    For example, Week01/.answers/mca.json is where you should put the companion mca.json file for Week01 of the labs.

    To create such a document, look at the example below.

    Parameters
    ----------
    weekNbr: int
        Week number (starts at 1)
    qNbr: int
        Question number (starts at 1) in the JSON file to extract

    Example
    -------
    >>> import json
    >>> qus = [
    >>>     {
    >>>     "question": "Select all which apply",
    >>>     "options": {
    >>>         "Tissues high in fat are bright in T1 contrast, which is why white matter is brighter than grey matter": (True, "Correct! Remember: fat appears bright in T1, water appears dark. White matter crucially contains myelin, which is absent from grey matter and thus white matter contains more fat than grey matter."),
    >>>         "Tissues high in fibers are bright in T1 contrast, which is why white matter is brighter than grey matter": (False, "Incorrect!"),
    >>>         "None of the above": (False, "Incorrect!"),
    >>>     },
    >>>     "multi-choice":False
    >>>     },
    >>>     {
    >>>     "question": "",
    >>>     "options": {
    >>>         "Region 1 is likely high in fibers and might be tendons and ligaments, which are dense connective tissues full of fibers.": (False, "Nope"),
    >>>         "Region 1 is likely high in fat, and is probably subcutaneous fat.": (True, "Indeed"),
    >>>         "None of the above": (False, ""),
    >>>     },
    >>>     "multi-choice":False
    >>>     },
    >>>     {
    >>>     "question": "",
    >>>     "options": {
    >>>         "Region 2 contains a mix of fat and water, hence the slightly darker color. Given its location, it is probably bone marrow.": (False, "Incorrect! We can make out the skull around the brain. Note that while it is greyer, it does not imply that it is a mixture of fat and water. It simply means that its relaxation time is *slower* that fat, but higher than water."),
    >>>         "Region 2 contains a mix of fibers and water, hence the slightly darker color.\nGiven its location, it may be dura mater, connective tissues making up the outer-most layer of the meninges.": (False, "Incorrect! The dura mater is in fact visible just outside the brain."),
    >>>         "None of the above": (True, "Correct."),
    >>>     },
    >>>     "multi-choice":False
    >>>     },
    >>>     {
    >>>     "question": "",
    >>>     "options": {
    >>>         "Region 3 contains air, which is why we do not see it in T1.": (False, "Incorrect! Neurons exposed to the air directly would be in a bit of a dangerous situation."),
    >>>         "Region 3 contains mostly water, which appears dark in T1.": (True, "Correct! This liquid is in fact called cerebro-spinal fluid (CSF) and is essential to a healthy brain."),
    >>>         "None of the above": (False, "Incorrect!"),
    >>>     },
    >>>     "multi-choice":False
    >>>     },
    >>>     {
    >>>     "question": "",
    >>>     "options": {"pve_0 is white matter, pve_1 is grey matter, pve_2 is CSF": (False, "Hi"),
    >>>                 "pve_0 is grey matter, pve_1 is white matter, pve_2 is CSF": (False, "No"),
    >>>                 "pve_0 is grey matter, pve_1 is CSF, pve_2 is white matter": (False, "Maybe"),
    >>>                 "pve_0 is CSF, pve_1 is grey matter, pve_2 is white matter": (False, "Perhaps"),},
    >>>     "multi-choice": True
    >>>     },{
    >>>     "question": "Which type volume should we use to perform fMRI motion-correction?",
    >>>     "options": {"Choosing as reference a volume of the fMRI timeserie": (True, "Indeed, this is what is typically done in practice."),
    >>>                 "Averaging the fMRI timeserie and using the mean volume as reference": (True, "This can also be done, in general to avoid the issue of choice of a given volume in the time-serie, although the difference in quality is often negligible compared to using a volume instead of the average."),
    >>>                 "Choosing as reference an anatomical volume, preferably of T1 contrast": (False, "To correct within a modality, this is a bad idea due to the difference in resolution and contrast between BOLD and T1."),
    >>>                  "Choosing as reference an fMRI standard space volume, derived from a cohort of participants": (False, "While this sounds reasonable, deriving and mapping to an average fMRI brain is tricky, given the resolution."),},
    >>>      "multi-choice": True
    >>>      },
    >>>     {
    >>>     "question": "Which volume im the fMRI timeserie CAN we use to perform motion-correction?",
    >>>     "options": {"The first volume of the timeserie": (False, "In older acquisitions, MRI field needed time to stabilize, leading to contrast differences in the first few volumes which had to be thrown away. While recent systems automatically discard these volumes, we usually avoid them still, as participants are stiffer at the start of a recording."),
    >>>                 "The last volume of the timeserie": (False, "In general participants might move at the end of an acquisition, by getting impatient. Avoid these volumes as references."),
    >>>                 "The middle volume of the timeserie": (True, "We typically employ the middle volume, as participants tend to be settled in the acquisition and the field is stable."),
    >>>                 "Any volume such that the BOLD had the time to settle down": (True, "Indeed, we could employ in fact any volume, provided the field is stable and the participant is unlikely to move too much."),},
    >>>     "multi-choice": True
    >>>     },
    >>>       ]
    >>> 
    >>> with open('/home/jovyan/Labs/Week02/.answers/mca.json', 'w+') as f:
    >>>     json.dump(qus, f, indent=4)
    >>> question_title, question_items, is_mcq = extract_question_week(2, 1)
    """
    import json
    with open("/home/jovyan/Labs/Week{}/.answers/mca.json".format(str(weekNbr).zfill(2))) as f:
        loaded_data = json.load(f)
    question = loaded_data[qNbr - 1]
    return question["question"], question["options"], question["multi-choice"]
    
def interactive_MCQ(weekNbr, qNbr):
    """
    Function to create an interactive multiple-choice-questionnaire within Jupyter.
    The purpose is purely educational. Provided a week number and a question number, construct specifically this question corresponding MCQ.
    It is assumed that questions are placed in an mca.json file, as a simple list.

    Parameters
    ----------
    weekNbr: int
        The week number (starts at 1)
    qNbr: int
        The question number of that week (also starts at 1)
    """
    import ipywidgets as widgets
    from IPython.display import display, clear_output, HTML

    question, options, is_mul_choice = extract_question_week(weekNbr, qNbr)
    
    
    custom_css = """
    <style>
    .widget-radio-box label {
        white-space: normal !important;
    }
    </style>
    """

    display(HTML(custom_css))
    # Display the question
    display(widgets.HTML(f"<h3>{question}</h3>"))

    if is_mul_choice:
        # Create checkboxes for the options

        option_widgets = []

        for option_text, (is_correct, feedback_message) in options.items():
            checkbox = widgets.Checkbox(description=option_text, value=False, layout=widgets.Layout(width='99%'))
            feedback = widgets.HTML()
            
            def on_change(change, is_correct=is_correct, feedback_message=feedback_message, feedback=feedback):
                if change['new']:
                    if is_correct:
                        feedback.value = f"<span style='color: green;'>✔️ {feedback_message}</span>"
                    else:
                        feedback.value = f"<span style='color: red;'>❌ {feedback_message}</span>"
                else:
                    feedback.value = ""
            
            checkbox.observe(on_change, names='value')
            option_widgets.append(widgets.VBox([checkbox, feedback]))
        
        # Display everything
        display(widgets.VBox(option_widgets))
    else:
        # Create the radio buttons
        radio_buttons = widgets.RadioButtons(
            options=options.keys(),
            description='Choose:',
            disabled=False,
            layout=widgets.Layout(width='100%'),
            value=None
        )
        
        # Create an output area for feedback
        output = widgets.Output()
        
        def on_value_change(change):
            selected_option = change['new']
            is_correct, feedback_message = options[selected_option]
            
            with output:
                clear_output()
                feedback_color = 'green' if is_correct else 'red'
                if is_correct:
                    display(widgets.HTML(f"<span style='color: {feedback_color};'>✔️ {feedback_message}</span>"))
                else:
                    display(widgets.HTML(f"<span style='color: {feedback_color};'>❌ {feedback_message}</span>"))
        
        # Attach the change handler to the radio buttons
        radio_buttons.observe(on_value_change, names='value')
        
        # Display the question and the radio buttons
        display(radio_buttons)
        display(output)


def get_json_from_file(fname):
    """
    Given a filename pointing to a json, returns the json's content.

    Parameters
    ----------
    fname: string
        The filename of the json file

    Returns
    -------
    The data of the json file
    """
    import json
    f = open(fname)
    data = json.load(f)
    f.close()
    return data
