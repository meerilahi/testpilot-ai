import base64
from fastapi_app.schemas.mark_subjective_answersheet import QuestionRequest, MarkSubjectiveAnswerSheetRequest
import json

with open("temp_data/d6.png", "rb") as image_file:
    d6 = base64.b64encode(image_file.read()).decode('utf-8')   
with open("temp_data/d7.png", "rb") as image_file:
    d7 = base64.b64encode(image_file.read()).decode('utf-8')    
with open("temp_data/d11.png", "rb") as image_file:
    d11 = base64.b64encode(image_file.read()).decode('utf-8')  
with open("temp_data/d14.png", "rb") as image_file:
    d14 = base64.b64encode(image_file.read()).decode('utf-8')    

question_list =  [
    QuestionRequest(
    question_number = 1,
    pages = [4],
    q_type = "rrq",
    question_text =  "Complete the organization level against each example : \n Examples Stomach \n Man \n Glucose \n Ribosome",
    answer_key = " Examples \t Organization Level \n Stomach \t Organ \n Man \t Organism \n Glucose \t Molecule \n Ribosome \t Organelles",
    rubrics = [(1,"Stomach to Organ"), (1,"Man is Organism"), (1,"Glucose is Molecule"), (1,"Ribosome is Organelles")],
    grammer_penalty =  "Low",
    question_marks =  4,
    ),   
    QuestionRequest(
        question_number = 2,
        pages = [5],
        q_type = "rrq",
        question_text =  "Briefly explain following four characteristics of kingdom Protista: a. Cell Type, b. Nuclear envelope, c. cell wall, d. mode of nutrition ",
        answer_key = " a. Cell type: Eukaryotic unicellular- colonial or simple multicellular \n b. Nuclear envelope: Present \n c. Cell wall: Present in some forms, various types \n d. Mode of nutrition: Photosynthetic or heterotrophic or combination of these.",
        rubrics = [(1,"Cell type: Eukaryotic unicellular- colonial or simple multicellular"), (1,"Nuclear envelope: Present"), (1," Cell wall: Present in some forms, various types"), (1,"Mode of nutrition: Photosynthetic or heterotrophic or combination of these")],
        grammer_penalty =  "Low",
        question_marks =  4,
    ),
    QuestionRequest(
        question_number = 3,
        pages = [6],
        q_type = "rrq",
        question_text =  "Write a short note on electron microscope keeping in view its radiation type, lenses, magnification and images.",
        answer_key = "Radiation type: Beams of electrons \n Lenses: Magnetic \n Magnification: 100 times greater than light \n Images: TEM shows 2D while SEM shows 3D images",
        rubrics = [(1,"Radiation type: Beams of electrons"), (1,"Lenses: Magnetic"), (1,"Magnification: 100 times greater than light"), (1,"Images: TEM shows 2D while SEM shows 3D images")],
        grammer_penalty =  "Low",
        question_marks =  4,
    ),
    QuestionRequest(
        question_number = 4,
        pages = [7],
        q_type = "rrq",
        question_text =  "Define turgor and write any TWO points to show its importance Textbook in plants.",
        answer_key = """ **Turgor:** The pressure which is exerted by the cytoplasm against the answer cell wall is known as turgor pressure and the phenomenon is called turgor.\n
        **Importance of turgor in plants**:\n
        i. It plays an important role in maintaining the shape of the plant.\n
        ii. It provides supports to plants especially in young tissues.\n
        iii. It helps in closing and opening of the stomata.\n
        iv. Some flowers open during the day time and close at night. This is also due to change in turgor in the cells of sepals of flowers.""",
        rubrics = [(2,"Correct definition of turgor"), (1,"Correct Importance"), (1,"Correct Importance")],
        grammer_penalty =  "Low",
        question_marks =  4,
    ),
    QuestionRequest(
        question_number = 5,
        pages = [8],
        q_type = "rrq",
        question_text =  "How is a prokaryotic cell different from a eukaryotic cell in Textbook terms of nucleus, cell membrane, cell wall and size.",
        answer_key = """
        | Component           | Prokaryotic Cell                                                                 | Eukaryotic Cell                                                       |
        |--------------------|-----------------------------------------------------------------------------------|------------------------------------------------------------------------|
        | Nucleus            | They lack membrane-bound nucleus.                                                 | The nuclear material is surrounded by a double membrane.              |
        | Membrane organelles| Membrane bounded organelles are absent.                                           | Membrane bounded organelles are present.                              |
        | Cell wall          | Cell wall is made of peptidoglycan (a singular larger polymer of amino acids and sugar). | Cell wall is made of cellulose (plants) or chitin (fungi).       |
        | Size               | Comparatively smaller in size (0.5 µm)                                             | Larger in size (10–100 µm)                                            |
        """,
        rubrics = [(1,"Correct difference in Nucleus"), (1,"Correct difference in Membrane organelles"), (1,"Correct difference in Cell wall"), (1,"Correct difference in Size")],
        grammer_penalty =  "Low",
        question_marks =  4,
    ),
    QuestionRequest(
        question_number = 6,
        pages = [9],
        q_type = "rrq",
        question_text =  "Enlist the events (and show with diagram) through which mitotic apparatus is formed in prophase in animal cells",
        answer_key = """ i. In animal cell, when two parts of centrioles reach opposite answer pole of the cell. They make a network of spindle fibers betweenthe two poles. The complete set of spindle fiber forms mitotic apparatus. """,
        diagram_key = d6,
        rubrics = [(1,"Event : two parts of centrioles reach opposite pole of the cell"), (1,"Event : They make a network of spindle fibers between the two poles"), (2,"Correct Diagram")],
        grammer_penalty =  "Low",
        question_marks =  4,
    ),
    QuestionRequest(
        question_number = 7,
        pages = [10],
        q_type = "rrq",
        question_text =  "How are enzymes specific for their substrate? Justify it with the help of diagram of shape of active site of enzyme and its specificity. Also give its TWO examples.",
        answer_key = """ Examples:\n
        Enzyme protease: Speed up the digestion of protein only.\n
        Enzyme amylase: Works for the digestion of starch only.\n
        Enzyme cellulose: Speed up the digestion of cellulose only.\n
        Enzyme lipase: Digests lipase only.""",
        diagram_key = d7,
        rubrics = [(2,"Diagram"), (1,"First correct example "), (1,"Second correct example ")],
        grammer_penalty =  "Low",
        question_marks =  4,
    ),
    QuestionRequest(
        question_number = 8,
        pages = [11],
        q_type = "rrq",
        question_text =  "How are enzymes specific for their substrate? Justify it with the help of diagram of shape of active site of enzyme and its specificity. Also give its TWO examples.",
        answer_key = """
        | Respiration | Photosynthesis |
        |-------------|----------------|
        | It is energy releasing process. | It is an energy storing process. |
        | Stored energy of food molecules is released for cellular activities. | Energy of sunlight is trapped by the chlorophyll and converted into chemical energy and stored in organic food molecules. |
        | Glucose and oxygen are the raw materials while carbon dioxide and water are the products. | Carbon dioxide and water are used as raw materials while glucose and oxygen are the products. |
        | Oxygen is required in aerobic respiration. | Oxygen is liberated as by product. |
        | It takes place in all the cells of all living organisms. | It takes place only in green cells of plants, algae and some bacteria. |
        | It is destructive (catabolic) process during which organic food molecules are broken and energy is released. | It is constructive (anabolic) process during which organic food molecules are synthesized and energy is stored. |
        | Due to respiration, loss of weight occurs. | Due to photosynthesis, plant body gains weight. |
        | It occurs round the clock, day and night. It does not require sunlight. | It occurs during the daytime when sunlight is available which is necessary for it. |
        """,
        rubrics = [(1,"One Correct Difference"), (1,"One Correct Difference "), (1,"One Correct Difference"), (1,"One Correct Difference")],
        grammer_penalty =  "Low",
        question_marks =  4,
    ),
    QuestionRequest(
        question_number = 9,
        pages = [12],
        q_type = "rrq",
        question_text =  "Write any FOUR deficiency symptoms of vitamin D.",
        answer_key = """
        Deficiency symptoms of vitamin D:
        1. Bones can become thin, brittle and soft.\n
        2. In children vitamin D deficiency leads to rickets (condition in
        which bones weaken and bow under pressure).\n
        3. In adults, vitamin D deficiency symptom causes
        osteomalacia (soft bones).\n
        4. Vitamin D deficiency symptom also causes fractures.\n
        Note: Any other related or correct deficiency symptom of vitamin D out of textbook may be considered.
        """,
        rubrics = [(1,"One Correct symptom"), (1,"One Correct symptom "), (1,"One Correct symptom"), (1,"One Correct symptom")],
        grammer_penalty =  "Low",
        question_marks =  4,
    ),
    QuestionRequest(
        question_number = 10,
        pages = [13],
        q_type = "rrq",
        question_text =  "List any FOUR functions of plasma in human body.",
        answer_key = """
        FUNCTIONS OF PLASMA IN HUMAN BODY:\n
        1. Plasma keeps all the tissues moist.\n
        2. Plasma of the blood transport nutrients, water, salt, Textbook Board hormones and waste materials.\n
        3. Plasma helps in regulating body temperature.\n
        4. Small amount of oxygen is also carried by plasma. Most of the carbon dioxide is carried by plasma.\n
        5. Plasma proteins e.g. albumins maintain the osmotic pressure of blood\n
        6. Important plasma proteins called antibodies defend the body against pathogens.\n
        7. Another plasma protein fibrinogen is responsible for blood clotting.\n
        """,
        rubrics = [(1,"One Correct Function"), (1,"One Correct Function "), (1,"One Correct Function"), (1,"One Correct Function")],
        grammer_penalty =  "Low",
        question_marks =  4,
    ),
    QuestionRequest(
        question_number = 11,
        pages = [14],
        q_type = "rrq",
        question_text =  "Why are arteries important? Draw a labelled diagram of artery.",
        answer_key = """
        IMPORTANCE OF ARTERIES.:
        All the arteries carry oxygenated blood from heart to other organ of the body except pulmonary arteries which carry deoxygenated blood to lungs.
        """,
        rubrics = [(2,"Correct explanation of importance"), (2,"Correct Diagram ")],
        grammer_penalty =  "Low",
        question_marks =  4,
    ),
    QuestionRequest(
        question_number = 12,
        pages = [15,16,17,18],
        q_type = "erq",
        question_text =  "i. Explain the applications of mathematics rules used in biology research work. ii. Define the term conservation. Write any THREE examples of the steps taken in Pakistan to conserve biodiversity.",
        answer_key = """
        i. APPLICATIONS OF MATHEMATICS RULES USED IN BIOLOGY RESEARCH WORK\n
        • Population studies\n
        • Drugs studies\n
        • Sequencing of plants and animals\n
        • DNA\n
        All the above fields of biology require mathematical knowledge rules for organizing and analyzing data.\n
        ii. CONSERVATION \n
        Conservation means to use the resources such as plants, animals, minerals and water in a sensible way.\n
        Examples of steps taken in Pakistan for conservation of biodiversity\n
        • Indus Dolphin Project (IDP) to save Indus Dolphin\n
        • Projected Areas Management Project in Machian in Azad Jammu Kashmir\n
        • Marine Turtle Conservation Project\n
        • Ban on the hunting of markhor and urial in Balochistan\n
        • Himalayan Jungle Project to protect the biodiversity in Himalayan region\n
        • Conservation of migratory birds in Chitral, Khyber Pakhtunkwa\n
        • Himalayan Wildlife Project to check the hunting of brown bears\n
        • Conservation of Chiltan Markhor\n
        • Ban on Bear-baiting in Pakistan\n
        """,
        rubrics = [(1,"one correct application of mathematics in biology"), (1,"one correct application of mathematics in biology"),(1,"one correct application of mathematics in biology"), (1,"one correct examples of steps"),(1,"one correct examples of steps"),(1,"one correct examples of steps") ],
        grammer_penalty =  "Low",
        question_marks =  7,
    ),
    QuestionRequest(
        question_number = 13,
        pages = [19,20,21,22],
        q_type = "erq",
        question_text =  "i. Briefly explain following animal tissues: a. Fibrous connective tissues, b. Smooth muscles, c. Nervous tissues, d. Epithelial tissue. ii. Define Cell Cycle and write names of its TWO main stages.",
        answer_key = """
        i. ANIMAL TISSUES\n
        a. Fibrous connective tissues: Its extracellular material contains tightly packed collagen fibers. It is the form of tendon which attaches muscles to bones and ligaments join two bones.\n
        b. Smooth muscles: These are found in the walls of hollow structures such as blood vessels, gut etc. They produce slow contractions.
        c. Nervous tissues: It is composed of nerve cells which are called neurons. Neurons are capable of transmitting nerve impulses to conduct messages in the whole body.
        d. Epithelial tissue: The skin is made of epithelial tissue, which is in the form of continuous sheets of cells. Epithelial tissue also lines the gut, lungs and urinary tract.
        ii. CELL CYCLE:\n
        The series of events that take place in a eukaryotic cell leading to its replication is called cell cycle.\n
        Main stages of cell cycle : \n
        • Interphase or resting stage \n
        • Division phase (Mitosis or Meiosis) \n
        """,
        rubrics = [(1,"one correct brief description of given tissue"), (1,"one correct brief description of given tissue"),(1,"one correct brief description of given tissue"), (1,"one correct brief description of given tissue"), (1,"correct definition of cell cycle"), (1," correct name of one stage of cell cycle"), (1," correct name of one stage of cell cycle") ],
        grammer_penalty =  "Low",
        question_marks =  7,
    ),
    QuestionRequest(
        question_number = 14,
        pages = [23,24,25,26],
        q_type = "erq",
        question_text =  "i. Why is mitochondrial enzyme called intracellular? Give justification. ii. Explain the synthesis and breaking of ATP through ATP-ADP cycle with proper diagrams",
        answer_key = """
        i. Why is mitochondrial enzyme called intracellular?
        All enzymes are synthesized inside cells. Mitochondrial enzyme also work inside the cells so it is also called intracellular enzymes.
        ii. Synthesis and breaking of ATP through ATP-ADP cycle Synthesis:
        Synthesis : ATP molecules are constantly broken by the cell into ADP and inorganic phosphate and energy is obtained.
        Breaking of ATP: ATP molecules are constantly regenerated from ADP and phosphate using energy released from the breakdown of food. This is how constant cycle of ATP breakdown and reformation goes on in the living cells.
        """,
        rubrics = [(3,"Correct description of mitochondrial enzyme as intracellular of ATP"), (1,"Correct description of Synthesis of ATP"),(1,"Correct diagram of Synthesis"), (1,"Correct description of Breaking of ATP"), (1,"Correct diagram of Breaking of ATP") ],
        diagram_key = d14,
        grammer_penalty =  "Low",
        question_marks =  7,
    ),
    QuestionRequest(
        question_number = 15,
        pages = [27,28,29,30],
        q_type = "erq",
        question_text =  "i. State symptoms, causes and preventions of the diarrhea. ii. Differentiate between Atherosclerosis and Arteriosclerosis",
        answer_key = """
        i. DIARRHEA :
        Symptoms : frequent, watery, loose bowel movement, abdominal pain, nausea and vomiting
        Causes : bacterial infection, viral or parasitic infection of the colon walls
        Prevention : can be prevented by taking sufficient amounts of clean water and food
        ii. Differentiate between Atherosclerosis and Arteriosclerosis
        Atherosclerosis : It is characterized by the deposition of fatty material e.g. cholesterol inside the arteries. Due to this, the lumen (interior) of the artery becomes narrow and blood flows with difficulty.Later, the artery may completely be blocked. Some obvious reasons of atherosclerosis are hypertension, smoking, diabetes mellitus and increased lipid level in blood
        Arteriosclerosis : It is the hardening of the arteries due to the deposition of calcium in the walls of the arteries. Such artery cannot expand when blood is pumped with pressure into it with systole. Due to this inflexibility makes the heart to work hard. This disorder occurs with increasing age. 
        """,
        rubrics = [(1, "Correct symptoms of diarrhea"), (1, "Correct causes of diarrhea"), (1, "Correct preventions of diarrhea"), (2, "Correct description (differences) of Atherosclerosis."), (2, "Correct description (differences) of Arteriosclerosis.") ],
        grammer_penalty =  "Low",
        question_marks =  7,
    ),
]    

sample_request = MarkSubjectiveAnswerSheetRequest(
    list_of_questions = question_list,
    rrq_attempts = 8,
    erq_attempts=3,
    total_paper_marks =53,
    language = "English",
    subject = "Biology"
)

with open("data.json", "w") as f:
    json.dump(sample_request.model_dump(), f, indent=2)