# BBPTimer
An automatic shot timer for the Breville Bambino Plus*

<sub>\* Should work with any Breville machine with a solenoid valve, but I have only tested on a 2024 Bambino Plus</sub>
# Demo Video
[![BBPTimer Demo](https://i.imgur.com/Ce7qzek.png)](https://youtu.be/D96JdEO-_og)
# Hardware Requirements
* You will need:
	* Any [Raspberry Pi or Raspberry Pi Zero](https://www.raspberrypi.com/products/), as long as it has Wi-Fi. You can use the [Raspberry Pi Zero  WH](https://www.adafruit.com/product/3708) which costs just $16. I use a Raspberry Pi 4.
	* A Reed switch. This should cost $4-$8. I use [this switch](https://www.microcenter.com/product/614938/nte-electronics-switch-white-magnetic-alarm-reed-spst) from Micro Center, but also successfully tested with [these switches](https://www.amazon.com/dp/B0B3D7BM4K) from Amazon.
	* A 4GB or larger microSD card. This should cost less than $10.
	* A USB-C or Micro USB cable (depending on your Raspberry Pi model), and a [compatible phone charger](https://www.raspberrypi.com/documentation/computers/getting-started.html#power-supply). If you have bought anything that charges with a USB cord in the past 5+ years, you probably already have these on hand.

If you had nothing but a charger+USB cable, a wire cutter, and a couple of wire nuts, you could buy everything needed, including a case, at my local electronics store for less than $35:
| **Product**                                                                                                                              | **Price**  |
|------------------------------------------------------------------------------------------------------------------------------------------|------------|
| [Raspberry Pi Zero WH](https://www.microcenter.com/product/502843/raspberry-pi-zero-wh-with-pre-soldered-headers)                        | $15.99     |
| [Raspberry Pi Zero Case](https://www.microcenter.com/product/486577/raspberry-pi-official-raspberry-pi-zero-case-white-red)              | $4.99      |
| [32GB microSD Card](https://www.microcenter.com/product/658457/micro-center-32gb-microsdhc-card-class-10-flash-memory-card-with-adapter) | $3.99      |
| [Reed Switch](https://www.microcenter.com/product/486577/raspberry-pi-official-raspberry-pi-zero-case-white-red)                         | $3.99      |
| [Dupont Wire](https://www.microcenter.com/product/613879/inland-dupont-jumper-wire-20cm-3-pack)                                          | $4.99      |
| **Total**                                                                                                                                | **$33.95** |
# Hardware Setup
* Remove the top lid from your Bambino Plus. To do this, remove the 2 screws at the top rear of the machine, behind the water tank. Pop open the rear of the machine to the topmost 2 tabs, and then slide the top of the machine backwards.
* [Stick your Reed switch to the solenoid valve](https://imgur.com/LNzAFQv).
* Run your Reed switch wires out of the machine. You may need to create a notch so that the wires have a little "breathing room" on their way out of the machine.
* Attach one of the Reed switch wires to a [Raspberry Pi GPIO pin](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html). Attach the other Reed switch wire to a ground pin on the Raspberry Pi. It does not matter which Reed switch wire goes to which of those pins.
	* I stripped the ends off of [2 female Dupont wires](#hardware-requirements) and used wire nuts to attach them to the Reed switch wires. This allowed me to attach the Reed switch to the GPIO pins without needing to solder or crimp. [Here is a diagram](https://imgur.com/sX9urM5) (sorry for the terrible photo editing).
# Creating an SD Card Image for your Raspberry Pi
* On a computer, use [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to [configure your SD card](https://www.raspberrypi.com/documentation/computers/getting-started.html#install-using-imager):
	* Select **Raspberry Pi OS Lite** for your operating system.
	* Click **Edit Settings** and set these custom settings:
		* Choose the username **pi** and set a unique password.
		* Configure your WiFi credentials.
		* Click the **Services** tab:
			* Check **Enable SSH**.
			* Choose the **Use password authentication** option.
# Remotely Accessing your Raspberry Pi and Running the Shot Timer
* Open a Terminal or Command Prompt on a computer, and paste the following to establish an SSH connection to your Raspberry Pi for setup:
	```
 	ssh pi@raspberrypi.local
 	```
 	* [If using an iPhone](#easy-iphone-setup), install the Termius app, download the Siri shortcut, and run the Siri shortcut.
* Once you have established an SSH connection, paste the following to download **BBPTimer.py** to the Raspberry Pi:
	```
	wget https://raw.githubusercontent.com/BBPTimer/BBPTimer/main/BBPTimer.py
 	```
* Now change the [**BBPTimer.py variables**](#bbptimerpy-variables) to your liking:
	* Paste the following to edit **BBPTimer.py**:
		```
		nano BBPTimer.py
  		```
	* Tweak the 4 variables as needed at the top of the file.
	* To save, type **control+X**, then **Y**, then **return**.
* Finally, paste the following to run the timer:
	```
	python3 BBPTimer.py
 	```
* To set the timer to automatically run when you establish an SSH connection, paste the following:
	```
	echo -e "\n\npython3 BBPTimer.py" >> .bashrc
 	```
# BBPTimer.py Variables
When the Bambino Plus pump operates, its solenoid valve produces a magnetic field. This shot timer uses a Reed switch attached to the solenoid valve to time how long it produces a magnetic field, so that we can easily measure shot time with no effort.

We will need to set the following 4 variables within **BBPTimer.py**, and then we can time espresso shots without needing to use hands or eyes:
### reedPin (required, default = 26)

The [Raspberry Pi GPIO pin number](#hardware-setup) assigned your Reed switch.
### warmup (optional, default = 0)

The timer will start as soon as you start to hold the shot button. If you want to start the timer when the pump actually begins to vibrate, set the **warmup**.

> The pump on my Bambino Plus starts to vibrate around 4 seconds after I press the shot button, so I set my **warmup** to 4. Now, the timer will begin at -4.0 seconds when I star to hold the shot button, and will reach 0 seconds approximately when the pump begins to vibrate.
### preInfuse (optional, default = 5)

You will also want to set a preInfuse time. The timer will produce an audible chime to tell you when to stop pre-infusion. When you hear the chime, release the shot button.

> I like to preInfuse for 5 seconds, so I set my **preInfuse** to 5. Now, at 5 seconds, my phone will produce an audible chime to tell me to release the shot button to stop pre-infusion.
### cooldown (required, default = 0, you will need to change this value after timing your first shot)

Stop your shot when you reach your desired yield. The solenoid valve continues to produce a magnetic field for a few seconds after the pump stops vibrating, so we will need to set a **cooldown** time, which is the time between when the pump stops vibrating and when the timer automatically stops.

> On my Bambino plus, the timer automatically stops around 8.5 seconds after the pump stops vibrating (*e.g. pump stops vibrating at 30 seconds, but timer stops at 38.5 seconds*), so I set my **cooldown** to 8.5. At the end of the timer, it will subtract those seconds to give me my real shot time (*30 seconds in the previous example*).

If you time your first shot and the pump stopped vibrating at 33 seconds and the timer stopped at 40 seconds, you would set your **cooldown** to the difference between those numbers, so 7 in this case.
# Easy iPhone Setup

If you want to operate your timer from your phone, [Termius](https://termius.com) is an excellent free SSH app for [iOS](https://apps.apple.com/us/app/termius-terminal-ssh-client/id549039908) and [Android](https://play.google.com/store/apps/details?id=com.server.auditor.ssh.client&hl=en).

* I created a [Siri shortcut](https://www.icloud.com/shortcuts/10f6172827eb40c3b5db1c6a4abbf974) that turns up the iPhone volume (to make sure the pre-infuse chime is audible), and then opens an SSH connection to the Raspberry Pi. If you don't want the shortcut to change the phone volume, just open it in the Shortcuts app and delete that step.
* If you add the shortcut to your home screen and [set the timer to automatically run when you establish an SSH connection](#remotely-accessing-your-raspberry-pi-and-running-the-shot-timer), you can just tap the "app" on your home screen to launch the timer.
* Termius offers a customizable Shake function. I [set my Shake function to Close](https://imgur.com/Tq2rGJY) so that my SSH connection closes when I shake my phone once.
