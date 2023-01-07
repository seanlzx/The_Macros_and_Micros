dict = {"nae": "great", "grief": "green", "smiles": "great"}
required = {"grief", "smiles"}
# turn this into a requsable function?

all(item in dict for item in required)