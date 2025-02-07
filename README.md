# NAO USER INTERFACE (NAOUI)
Easy real-time user interface for controlling the humanoid robot NAO, suitable for non-programmers.

## Interface description
When you start your UI as detailed in next section, you will see the following setup:

![ui](https://github.com/user-attachments/assets/d54b50b8-1588-40ed-bc8e-1fa8e399aaed)

There are 3 columns: camera, controls, and mix.
1. CAMERA
   
   ![camera](https://github.com/user-attachments/assets/99b0d571-6f7a-40c0-9aee-190e50dd1832)

   By clicking on 'Start Camera', you will start seeing what NAO is looking at. You can start and stop at any time.

3. CONTROLS
   
   ![controls](https://github.com/user-attachments/assets/91ca1598-39d4-4b7f-ad0d-0cd862d869ae)
   
   In this column you can control NAO in real-time.
   The Volume frame controls the volume at which NAO speaks.
   The Artificial Life flag, when checked, enables automatic head movement (NAO rotates his head when detecting sounds/movements around him)
   The Speech frame is for making NAO speak: you need to type the sentence you want him to say and then click on 'Make NAO speak'. The gestures flag enables a slight random movement of hands while talking.
   The Movement frame makes NAO perform the selected movement when clicking on 'Execute movement'. The list of movement can be modified as described in the last section of this document (Developer guide).

5. MIX
   
   ![mix](https://github.com/user-attachments/assets/6325f739-c015-453c-87a9-4c9a4d6a96f7)
   
   When needed, the user can click on the question button on top right of the page, which will pop the sentence at the bottom of the image: "A Mix consists of speech and movement actions. First, set the       parameters for the action in the adjacent column. Once you're satisfied with the settings, select the type of action and click 'Add to Mix' to add it to your list. You can then remove, reorder, or execute the list."
   To add actions to the mix, you need to set up the action in the controls column, then select the type of action in the mix column (speech or movement) and finally click on 'add to mix'. Do this as many times as needed. To move or remove an action from the list, click on it and then on the button in the right part of the column.
   When everything is correctly set up, click on 'execute mix' to make NAO perform all of the actions in the list one after the other. Please note that once you click on 'execute mix', you won't be able to stop or modify the mix until it is done.
   
   ![mix2](https://github.com/user-attachments/assets/bdc0dfb6-888b-4ca4-95f0-378cf9888ea9)



## Installation guide
1. Download naoqi (API for NAO) at this link: https://aldebaran.com/support/kb/nao6/downloads/nao6-software-downloads/ , under SDK (at the bottom of the web page). Choose the option suitable for your operative system.
2. Unzip and add the folder 'lib' to your system variables, under the name 'PYTHONPATH'. Now the library naoqi should be able to be imported.
3. Download miniconda and create an environment using the requirements in the 'environment.yml' file. Note that the python version must be 2.7.18.
4. Connect to the same Wi-Fi to which the robot is connected.
5. Turn on the NAO by pressing the button on his chest for a couple of seconds. Wait a couple of minutes until it's awake.
6. Download the naoui.py file and insert the ip address and port of your NAO in lines 17 and 18 (you can discover it by pressing its chest once).
7. From the terminal, activate the miniconda environment, then navigate to the folder where you have the 'naoui.py' file and execute it.

## Developer guide
To add movements, just add an 'else' statement in 'execute_movements' function and describe them in terms of junctions roll. (line 140)

![move-code](https://github.com/user-attachments/assets/be920539-b51a-4259-90e3-e12fb1d56667)

To make them appear on the movement list on the UI, add the name of your new movement in line 372.


