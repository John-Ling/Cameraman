# Your own personal cameraman #
A webcam that tracks and follows your face in the room. Powered by OpenCV and microcontrollers.

## Background ##
I'm a student at the moment whose school does hybrid teaching meaning students are both in-person and online. However, many of my teachers would forget about their online students and continue teaching without adjusting their computers to their position. Online students would have to ask them to move the camera, interrupting the lesson. To make hybrid education more seamless, I designed and programmed a "Personal Cameraman" that would follow a teacher as they moved around the classroom.


## The details ##
The system has two separate components: software and hardware. As I'm more familiar with software, I'll go into it first.

### Software ###
I used OpenCV-Python's DNN module for incredibly accurate tracking and fairly low CPU overhead (the software is to be deployed on Macbooks without a dedicated GPU). I also used the PySerial library for communication with the hardware. 
#### Face Tracking ####
The software looks through the video feed of a laptop's webcam for any faces in each frame. A bouding box is drawn for each face detected within the frame. When multiple people are in frame, a "most important face" algorithm is used to determine the face the cameraman should track. Once the most important face is decided, the center coordinates of the bounding box is calculated by halving its width and height. The X and Y coordinates are formatted and separated by a colon ":" (for example coordinates X = 500 and Y = 420 would be "500:420"). Before being sent, the data is check to ensure it's valid. Any widths or heights greater than 150 are immediately discounted to fix a bug where the entire body is detected rather than just the face. Additionally, negative values or data with multiple separator characters are ignored. If the data passes those checks, it is serialised into byte data and sent to the microcontroller. The microcontroller itself has code to receive and parse serial data, taking data up to the separator and after it. Since the laptop's webcam has a field view of 60°, the received serial data needs to be scaled to fit that range. Parsed data is multipled against a scaling constant to fit the field of view and the data is written to two motors for X and Y respectively.

##### Important Face Algorithm #####
In the event multiple people are in frame, the largest bounding box is chosen as the most important face. This can be done with a simple area calculation
