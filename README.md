# Server code for a wireless pan and tilt webcam

Available at kfcams.me

## Overview

A project for EECS 395 Engineering Systems Design II. The website presents an IoT based home automation system. To this end, our goal for the class was to implement a simple webcam endpoint that can stream its images to a server for heavier processing. 

## Description

A custom designed webcam serves as the endpoint for this server. The webcam posts JPG data to our server which handles streaming data to a website, performs face detection, and responds to the webcam with face tracking movements. The website also supports manual control of the webcam.

## Architecture

Webcam: ATSAM4S8B microcontroller, HS-422 Servos, AMW004 WiFi chip, Omnivision Camera.

Server: NGINX serves static files and proxies face detection requests to Tornado (Python server)

Website: Hosted on server (HTML, CSS, JS served by NGINX), opens websocket connection to server to communicate the presence of new frames. 

Face detection: Haar Cascades with OpenCV

## TODO

Connect to a database for video storage and retrieval (Amazon S3)

Add video capture buffers to improve performance
