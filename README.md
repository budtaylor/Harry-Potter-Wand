# Harry-Potter-Wand
As seen in Univeral Orlandos Wizarding World of Harry Potter! I have forked most of this code from John B Everingham. You can find his project at https://maker.pro/raspberry-pi/projects/wand-controlled-horcrux-box
I enjoyed his project but it was not exactly what I wanted. In John's code, the raspberry pi controlled everything from sounds to to the servos for the Horcrux box. I would like to deploy this to people who can do simple coding and can work with different systems. 
In my project, the camera picks up the wand movement as a spell, and sends a HIGH signal out of the Pi. I have an arduino nano connected to a neopixel ring and when the HIGH signal comes in the ring lights up and does little flickering. 

I will be uploading and revising the code periodically. 

I started this project wanting to turn on a lamp, which would either be LUMOS or INCENDIO. For this project I chose INCENDIO. 
Take three folders of pictures, Incendio, Reparo, and Wingardium and placed them into the Raspberry_Potter_1.0-main/SVM Models/Pictures folder.
Delete the svm_model_data_gen_rbpi.yml file from the Raspberry_Potter_1.0-main/SVM Model folder.
Run Model_training_final.py
I ran into an error but a new svm_model_data_gen_rbpi.yml file. Copy the file and move it to Raspberry_Potter_1.0-main/Rb_potter_files/Code/dependencies.
This will allow the main file to access the file. 

If you adjust any of the files you will need to go into Raspberry_Potter_1.0-main/Rb_potter_files/Code rb_potter_main.py and adjust the names of the spells on line 30 
scolling down to about line 146 you will see the code to set the GPIO pins high or low. adjust the labels appropriately to your spell. For instance on this first one the PIN is HIGH for 8 seconds. I wanted the lamp to turn on for 8 seconds. When the GPIO is LOW the lamp shuts off. 

To add or create new tracings you can go to Raspberry_Potter_1.0-main/SVM Model and start the trace_saving.py you can also adjust some the settings there without messing with the main code too much, such as blob detection and sensitivity. To get better accuracy you will want to add more pictures, I have about 100 of each spell. 

I will update for each new arduino sketch.
The first sketch turns on a neopixel ring. The ring is 8 LEDs and is hidden in a lamp to hopefully look realistic. The sketch simulates ramdom pixels turning to a different color and so I chose the flame to be red with an orange flicker. 
