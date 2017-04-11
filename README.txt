In order to initialize our server pi, you must do three things - first find the ip address of the pi you plan to use as your server pi,
then after finding the ip address of your pi, use the Raspbian GUI to open up Minecraft. Once Minecraft is open, you can run the 
server pi code.

All of this must be done before any client pi can connect.

On the client pi, you must wait for the server pi to be up, then once that code is running, the client pi can connect using the
ip address of the server pi. Once all the clients have been connected, the wall will begin to build

The only external library we used was argparse in order to make parsing the ip address input for the client pis simpler
