TremorTracker
=============

TremorTracker is a web-based app that uses a smartphone accelerometer to record and chart tremor movement.


## Realtime charting with websockets
The application charts movement in real time using D3, WebSockets, and the PubSub protocol so that data collected on a cellphone can be viewed simultaneously on another web browser.


## Signal processing using the Fourier Transform
Because Parkinson's tremors are typically concentrated in a 3-6hz range of movement, the recorded data is also processed using the Fast Fourier Transform algorithm. From the FFT, we are able to calculate the Power Spectral Density, which allows us to distinguish a specific Parkinsonian hand motion and the intensity of that motion over time.


## D3.js Auto-generated heatmap
A D3-generated heatmap displays the intensity of the movements at 1hz, 3hz, 6hz, and 10hz over the period of the recording.
  

####Technologies####: Python, Flask, Jinja, Redis, WebSockets, JavaScript, D3.js, NumPy
  


*The FFT algorithm takes in a signal over a specific time window (in this case, 1 second) and allows us to see the type and quantities of waves that make up the signal over that time period. A great simple explanation of the FFT can be found [here.](http://betterexplained.com/articles/an-interactive-guide-to-the-fourier-transform/)