# Stuntin' Shunt

This project was made for Cornell's Health Innocation Hack-A-Thon for Spring 2018.

It was also a part of a project for Cornell's Neurosurgery Department's Jeff Greenfield, MD, PhD


I've (Arun Ajay) written the code for this repo. 

The `FSR_ALPS_BT.ino` file contains code for the FSR and APDS sensors. 

This code analyzes inputs and sends an alert after a threshold is hit. 

Information is passed to a desktop via bluetooth while running the `Bluetooth_Data_Collection.py` code.

The `Bluetooth_Data_Collection.py` code contains a text messaging and emailing system service which notifies a physician if the shunt is blocked. 

A CSV file is sent to the email and contains flow data.  

Group Members:

Arun Ajay

Birra Taha
