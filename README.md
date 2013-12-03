TremorTracker
=============
TremorTracker is a web-based app that uses a smartphone accelerometer to record and chart tremor movement. 


##Accelerometer data & machine learning
Tremor Tracker was inspired by my machine learning work with a 10GB dataset of passively collected smartphone data provided by the Michael J. Fox Foundation. Data was collected from 9 PD patients, at varying stages of the disease, and 7 healthy controls, resulting in over 6,000 hours of collected data (comprised of 18,000 hours of individual data-streams). I chose to focus on the accelerometer data to create a machine learning classifier to separate parkinsons from non-Parkinson's patients. 

I initially followed the methodology of another researcher by averaging the Power Spectral Density (PSD) of the signal over an hour and using a Support Vector Machine classifier to separate the data. Unfortunately the methodology outlined in the paper did not correspond to the researcher's code and the results were not accurate or reproducible.

I had greater success averaging the PSD over a minute and using a random forest classifier. I was able to achieve ~73% accuracy with cross validation, but the recall score on non-Parkinson's patients showed a lot of false positives. Next, I would like to try and clean the data using k-means clustering with the compass data to isolate windows of time where the phone was still.

The github repo for the machine learning portion of the project can be found [here.](https://github.com/stellacotton/ParkinsonsSVM)

## Realtime charting with websockets
######(app.py, static/js/websockets.js, & static/js/live_chart.js)
App.py is the main web framework. The application charts movement in real time using D3, WebSockets, and the PubSub protocol so that data collected on a cellphone can be viewed simultaneously on another web browser.

![iphone screenshot image](https://raw.github.com/stellacotton/TremorTracker/master/static/img/iphone_recording.png)
![live charting image](https://raw.github.com/stellacotton/TremorTracker/master/static/img/live_chart.png)

## Signal processing using the Fourier Transform
######(fft.py)
Because Parkinson's tremors are typically concentrated in a 3-6hz range of movement, the recorded data is also processed using the Fast Fourier Transform algorithm. From the FFT, we are able to calculate the Power Spectral Density, which allows us to distinguish a specific Parkinsons hand motion and the intensity of that motion over time.


## D3.js generated heatmap
######(static/js/heatmap.js)
A D3-generated heatmap displays the intensity of the movements at 1hz, 3hz, 6hz, and 10hz over the period of the recording. 
![heatmap image](https://raw.github.com/stellacotton/TremorTracker/master/static/img/heatmap.png)

## Track medication & tremor effects over time
######(templates/drugs.html)
Provides an interface to search medications using the RXNorm API, an API maintained by the National Institute of Health. Search with an ingredient, brand name, clinical dose form, branded dose form, clinical drug component, or branded drug component and choose the medication and dosage from the results.
![medication search image](https://raw.github.com/stellacotton/TremorTracker/master/static/img/search_medication.png)

  


####Technologies: Python, Flask, Jinja, Redis, WebSockets, JavaScript, D3.js, NumPy
  


*The FFT algorithm takes in a signal over a specific time window (in this case, 1 second) and allows us to see the type and quantities of waves that make up the signal over that time period. A great simple explanation of the FFT can be found [here.](http://betterexplained.com/articles/an-interactive-guide-to-the-fourier-transform/)