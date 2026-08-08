# Set up 

```
 conda create --name kr-env
 
 conda activate kr-env
 
 conda install pip
 conda install python=3.12
 pip install clipspy
```

If packages such as json are not included in your python distribution, you might need to install them, too. But it 
worked for me with `conda install python=3.12`.

In case you want to re-download the data: 

```
 python3 get_data.py
 python3 make_facts.py
```

# Start program

```
 python3 clips_main.py
```

And then follow the instructions. 

If you need module or course numbers to copy, simply choose the option to display the list and then copy or choose 
from `all_data.json`.

"Continue" generally means "Stay in the program and ask another question".


# Run tests

```
python3 test.py
```