# Towards Autonomous Warehousing and Delivery

Navigation/UI resources for the Fetch/Freight platform. We developed two interfaces for interacting with the Fetch.

## Speech Navigation Interface
Code for this interface is contained in the following files and directories:

- `nav.py` runs both a Flask server and a ROS node which processes incoming text locations in HTTP requests from the web interface, and converts them into new movement goals for the Fetch.
- `templates/` includes HTML templates to be served by the Flask server.
- `static/` includes CSS and JS assets used by the web interface, including the clientside libraries (`annyang` and `SpeechKITT`) which perform speech-to-text on the web interface.
- `half_lab.pgm` is a 2D obstacle map of the Fetch's environment.

## Color-following Interface
Code for this interface is contained in the following files:

- `fetch.jpeg` is an example image pulled directly from the `image_rgb` messages served by ROS aboard the Fetch.
- `selectormodule.py` masks an input image, in this case with a blue filter.
- `watch_and_follow.py` receives masked images from `selectormodule.py`, finds the largest contour, and uses the centroid of this contour to move the Fetch correspondingly via the `cmd_vel` topic.
