# Your own personal cameraman #
A webcam that tracks and follows your face in the room. Powered by OpenCV and microcontrollers.


https://user-images.githubusercontent.com/100111224/165949008-5640b943-f781-46d1-9660-30f3ad849b28.mp4


## Background ##
I'm a student at the moment whose school does hybrid teaching meaning students are both in-person and online. However, many of my teachers would forget about their online students and continue teaching without adjusting their computers to their position. Online students would have to ask them to move the camera, interrupting the lesson. To make hybrid education more seamless, I designed and programmed a "Personal Cameraman" that would follow a teacher as they moved around the classroom.


## The details ##
The system has two separate components: software and hardware. As I'm more familiar with software, I'll go into it first.

### Software ###
I used OpenCV-Python's DNN module for incredibly accurate tracking and fairly low CPU overhead (the software is to be deployed on Macbooks without a dedicated GPU). I also used the PySerial library for communication with the hardware. 

The software looks through the video feed of a laptop's webcam for any faces in each frame. A bouding box is drawn for each face detected within the frame. When multiple people are in frame, a "most important face" algorithm is used to determine the face the cameraman should track. Once the most important face is decided, the center coordinates of the bounding box is calculated by halving its width and height. The X and Y coordinates are formatted and separated by a colon ":" (for example coordinates X = 500 and Y = 420 would be "500:420"). 

Before being sent, the data is check to ensure it's valid. Any widths or heights greater than 150 are immediately discounted to fix a bug where the entire body is detected rather than just the face. Additionally, negative values or data with multiple separator characters are ignored. If the data passes those checks, it is serialised into byte data and sent to the microcontroller. The microcontroller itself has code to receive and parse serial data, taking data up to the separator and after it. Since the laptop's webcam has a field view of 60°, the received serial data needs to be scaled to fit that range. Parsed data is multipled against a scaling constant to fit the field of view and the data is written to two motors for X and Y respectively.

#### Important Face Algorithm ####
In the event multiple people are in frame, the largest bounding box is chosen as the most important face; the face the cameraman should track. A simple area calculation of each box is used and the box with the largest area is selected as most important. Boxes with width or height of above 150 are ignored from comparisons. 


### Hardware ###
The microcontroller I used was an ATmega328p 14 pin IC. Due to the design constrains of the project I used a "barebones" arduino circuit for more flexibility on component positions on the PCB. This was also to keep costs down as I want to make this ecnomically feasible and affordable to build. 

#### Components Used ####
- ATmega328p microcontroller
- 16Mhz crystal oscillator
- 2x 22pf ceramic capacitors
- 10KΩ resistor
- 14 pin DIL IC socket
- 2x 470uf electrolytic capacitors
- _2x 2 AA battery holder wired in series*_
- 2x 3 pin long pin headers
- 1 pin long pin header
- 4 pin long pin header
- 2x MG 996R servo motors
- 3D printed webcam Y servo mount
- 3D printed X servo mount
- 3D printed case half 1 and 2
- 22 gauge wire of ideally different colours (I used stranded but you use solid core)
- Perfboard
- Logitech C270 webcam
- _USB drive size USB hub (what a mouthful)**_
- USB to TLL
- USB male to female cable


*Due to size constraints you need to wire two double AA holders in series for 6V to power motors

**Here is the [one](https://www.lazada.com.my/products/t-wolf-hb008-usb-30-hub-3-ports-high-speed-hub-2usb20-1usb30-hub-i3010272117-s14854735681.html?c=&channelLpJumpArgs=&clickTrackInfo=query%253Ausb%252Bhub%253Bnid%253A3010272117%253Bsrc%253ALazadaMainSrp%253Brn%253A21b09352de8e359d0426d17d291d59cb%253Bregion%253Amy%253Bsku%253A3010272117_MY%253Bprice%253A19.94%253Bclient%253Adesktop%253Bsupplier_id%253A300152529585%253Bbiz_source%253Ah5_hp%253Bslot%253A38%253Butlog_bucket_id%253A461009%253Basc_category_id%253A10002883%253Bitem_id%253A3010272117%253Bsku_id%253A14854735681%253Bshop_id%253A1775213&fastshipping=0&freeshipping=1&fs_ab=2&fuse_fs=&lang=en&location=Johor&price=19.94&priceCompare=skuId%3A14854735681%3Bsource%3Alazada-search-voucher%3Bsn%3A21b09352de8e359d0426d17d291d59cb%3BoriginPrice%3A1994%3BdisplayPrice%3A1994%3BsinglePromotionId%3A-1%3BsingleToolCode%3A-1%3BvoucherPricePlugin%3A0%3Btimestamp%3A1698558413357&ratingscore=5.0&request_id=21b09352de8e359d0426d17d291d59cb&review=1&sale=9&search=1&source=search&spm=a2o4k.searchlist.list.148&stock=1) I used but check your own country's stores to ensure fastest delivery.
