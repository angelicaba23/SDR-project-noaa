#Hi

import streamlit as st
import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pydub import AudioSegment
import os
import os, os.path


encoding="utf8"

st.title("Reciving & Decoding APT 🛰️💻🌎🌦️")
#st.text("Coded by: Angélica Barranco")

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1)
w = 12
h = 16
fig = plt.figure(figsize=(w,h)) # create a figure object

ax1 = fig.add_subplot(3,1,1) # create an axes object in the figure
plt.minorticks_on()
ax2 = fig.add_subplot(3,1,2)
plt.minorticks_on()
ax3 = fig.add_subplot(3,1,3)
plt.minorticks_on()

st.empty()

#photo--------------------------------------------------------------------
imagesc = Image.open('nst.png')
imagesc_r = Image.open('sc_r.jpeg')

#B&W----------------------------------------------------------------------
imgs = []
caption_all = []
path = "imgs/imgsbw"
valid_images = [".jpg",".png"]
for f in os.listdir(path):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    imgs.append(Image.open(os.path.join(path,f)))
    #caption(i) = os.path.splitext(f)[0]
    caption_all.append(f)
l = len(imgs)

#Colored-------------------------------------------------------------------

imgsc = []
caption_allc = []
path = "imgs/imgsc"
valid_images = [".jpg",".png"]
for f in os.listdir(path):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    imgsc.append(Image.open(os.path.join(path,f)))
    caption_allc.append(f)
lc = len(imgsc)

#audio--------------------------------------------------------------------

audio_file = open('202105131227.wav', 'rb')
audio_bytes = audio_file.read()


menu = ["Home","About the challenge", "Decode", "Galery"]
choice = st.selectbox("Menu",menu)
if choice == "Home":
    st.write("")
    st.write("")
    st.write("")
    #st.markdown("![Alt Text](https://i.gifer.com/F4kC.gif)")
    #st.markdown("![Alt Text](https://i.gifer.com/4gh7.gif)")
    #st.markdown("![Alt Text](https://i.gifer.com/P1dz.gif)")
    st.markdown("![Alt Text](https://i.gifer.com/QXma.gif)")
    #st.markdown("![Alt Text](https://media.giphy.com/media/xjc98z5UU4YE0Tvbjn/giphy.gif)")
    #st.markdown("![Alt Text](https://img.culturacolectiva.com/content/2016/05/ideas-cientificas-gif-tierra-redonda-medium.gif)")

if choice == "About the challenge":
    st.header("Hello👋🏻, here you'll find more about this amazing and challenging experience 👩🏻‍💻🛰️👨🏻‍💻")
    st.write("The challenge is to create a satellite image interception system using a homemade antenna and Software Define Radio. The first step to materialize this project was the construction of the antenna, which must receive the signal at the frequency transmitted by the satellites, then pass the analog signal to SDR for proper treatment, and decode the digital signal to present a gallery with different images of Colombia from space.")
    st.image(imagesc, caption='Desing of reception system.')

    st.markdown("### 📍Objective")
    st.write("Implement a radio communication system with SDR to receive signals from the meteorological satellites for proper processing and visualization of the images in the cloud.")
    st.write("✔️ Investigate and define the concept of Software Defined Radio.")
    st.write("✔️ Characterize the communications system: the source of information, the transmitter, channel, receiver, and user.")
    st.write("✔️ Design and build the NOAA satellite signal receiver.")
    st.write("✔️ Design a web page to show the obtained images .")

    st.markdown("### 📍Materials")
    st.write("✔️Antenna (dipole v).")
    st.write("✔️RG-6 coaxial cable.")
    st.write("✔️Adapter (coaxial to MCX).") 
    st.write("✔️SDR and driver")
    st.write("✔️Computer.")
    st.write("✔️Cubic SDR software.")
    st.write("✔️WxtoImg software.")

    st.image(imagesc_r, caption='Reception system')
    
elif choice == "Decode":
    st.empty()
    #Step 1.
    # Let’s load the WAV file using scipy library.
    # I only display a fragment from 20 to 21 seconds,
    # otherwise rendering will be too long.

    def decode(wav_file, ud):
        st.write("This is the "+ ud +" .wav that is about to decode ⤵️")
        st.audio(wav_file)
        fs, data = wav.read(wav_file)

        data_crop = data[20*fs:21*fs]
        #plt.figure(figsize=(12,4))
        ax1.plot(data_crop)
        ax1.set_xlabel("Samples")
        ax1.set_ylabel("Amplitude")
        ax1.set_title("Signal")

        #Step 2.
        # To speed up decoding, let’s reduce the sampling rate by 4 times,
        # discarding unnecessary values: 
        resample = 4
        data = data[::resample]
        fs = fs//resample

        #Step 3. The image is transmitting in amplitude modulation,
        # for conversion to AM let’s apply the Hilbert transform:#

        def hilbert(data):
            analytical_signal = signal.hilbert(data)
            amplitude_envelope = np.abs(analytical_signal)
            return amplitude_envelope
        data_am = hilbert(data)

        #resampling by /4 reduces the quality ALOT, IMHO.
        #applying a high pass filter to reduce the DC offset
        # (generated by the doppler effect / lack of doppler correction on reception?)
        # creates a waaaay better image with less to zero noise

        #def hpf(data, fs):
        #    firw = signal.firwin(101, cutoff=1200, fs=fs, pass_zero=False)
        #    return signal.lfilter(firw, [1.0], data)

        #data_am = hilbert(hpf(data,fs))

        ax2.plot(data_am)
        ax2.set_xlabel("Samples")
        ax2.set_ylabel("Amplitude")
        ax2.set_title("AM Signal")


        #Step 4. The final step. Actually, the decoding was already finished.
        # The data itself is transmitted in analogue format, so the color of
        # each pixel depends on the signal level. We can “reshape” the data into a 2D image,
        # from the format description it is known that one line is transmitted in 0.5 s:


        from PIL import Image
        frame_width = int(0.5*fs)
        w, h = frame_width, data_am.shape[0]//frame_width
        image = Image.new('RGB', (w, h))
        px, py = 0, 0
        for p in range(data_am.shape[0]):
            lum = int(data_am[p]//32 - 32)
            if lum < 0: lum = 0
            if lum > 255: lum = 255
            image.putpixel((px, py), (0, lum, 0))
            px += 1
            if px >= w:
                if (py % 50) == 0:
                    print(f"Line saved {py} of {h}")
                px = 0
                py += 1
                if py >= h:
                    break

        image = image.resize((w*8,h*8))
        #grc ueyscale_image = image.convert('L')
        ax3.imshow(image)
        plt.show()
        st.pyplot(fig)
        st.text("NOTE: this a simple proof of concept, no sync, no telemetry decoding.")

    uploaded_file  = st.file_uploader("Insert the .wav file you want to decode", type="wav",accept_multiple_files=False)
    ud = "**default**"
    wav_file = '202105131227.wav'
    if uploaded_file is not None:
        ud = "**uploaded**" 
        #wav_file = AudioSegment.from_ogg(uploaded_file) 
        wav_file = uploaded_file
    
    decode(wav_file,ud)  


elif choice == "Galery":
    #image = Image.open('C:\Users\angel\OneDrive\Escritorio\NOAA\web\202105061448.jpg')
    menu2 = ["ALL", "NOAA 19", "NOAA 18", "NOAA 15"]
    galery = st.selectbox("Filer the images by satellites",menu2)
    w = None 
    c = st.checkbox('Change the size of the images?')
    if c:
        w = st.slider("", min_value=300, max_value=600, value=450)


    if galery == "ALL":
        st.info("**Here you can see _all_ decoded images of _NOAA satellites_** ⤵️")
                #sorted by the newest.** ⤵️")
        st.text("NOAA satellites do not transmit colored images  or  with county lines.")
        st.text("Map overlay feature is applied by default.")
        color = st.checkbox('Add False color')
        if not color:
            for i in range(l):
                n = l-i-1
                if caption_all[n][16] == "o":
                    name = "NOAA " + caption_all[n][14:16] + " - " + caption_all[n][0:4] + "/" + caption_all[n][4:6] + "/" + caption_all[n][6:8] + " - " + caption_all[n][8:10] + ":" + caption_all[n][10:12] + " UTC"
                    st.image(imgs[n], caption=name, width=w)
        if color: 
            for i in range(lc):
                n = lc-i-1
                if caption_allc[n][17] == "o":
                    name = "NOAA " + caption_allc[n][14:16] + " - " + caption_allc[n][0:4] + "/" + caption_allc[n][4:6] + "/" + caption_allc[n][6:8] + " - " + caption_allc[n][8:10] + ":" + caption_allc[n][10:12] + " UTC"
                    st.image(imgsc[n],caption=name, width=w)
    elif galery == "NOAA 19":
        st.success("**Here you can see all decoded images of _NOAA 19 satellite_** ⤵️")
                   #sorted by the newest.** ⤵️")
        st.text("NOAA satellites do not transmit images with county lines or colored.")
        st.text("By default map overlay feature is applied")
        color = st.checkbox('Add False color')
        if not color:
            for i in range(l):
                n = l-i-1
                if caption_all[n][15] == "9" and caption_all[n][16] == "o":
                    name = "NOAA " + caption_all[n][14:16] + " - " + caption_all[n][0:4] + "/" + caption_all[n][4:6] + "/" + caption_all[n][6:8] + " - " + caption_all[n][8:10] + ":" + caption_all[n][10:12] + " UTC"
                    st.image(imgs[n], caption=name, width=w)
        if color: 
            for i in range(lc):
                n = lc-i-1
                if caption_allc[n][15] == "9" and caption_allc[n][17] == "o":
                    name = "NOAA " + caption_allc[n][14:16] + " - " + caption_allc[n][0:4] + "/" + caption_allc[n][4:6] + "/" + caption_allc[n][6:8] + " - " + caption_allc[n][8:10] + ":" + caption_allc[n][10:12] + " UTC"
                    st.image(imgsc[n],caption=name, width=w)

    elif galery == "NOAA 18":
        st.warning("**Here you can see all decoded images of _NOAA 18 satellite_** ⤵️")
                   #sorted by the newest.** ⤵️")
        st.text("NOAA satellites do not transmit images with county lines or colored.")
        st.text("By default map overlay feature is applied")
        color = st.checkbox('Add False color')
        if not color:
            for i in range(l):
                n = l-i-1
                if caption_all[n][15] == "8" and caption_all[n][16] == "o":
                    name = "NOAA " + caption_all[n][14:16] + " - " + caption_all[n][0:4] + "/" + caption_all[n][4:6] + "/" + caption_all[n][6:8] + " - " + caption_all[n][8:10] + ":" + caption_all[n][10:12] + " UTC"
                    st.image(imgs[n], caption=name, width=w)
        if color: 
            for i in range(lc):
                n = lc-i-1
                if caption_allc[n][15] == "8" and caption_allc[n][17] == "o":
                    name = "NOAA " + caption_allc[n][14:16] + " - " + caption_allc[n][0:4] + "/" + caption_allc[n][4:6] + "/" + caption_allc[n][6:8] + " - " + caption_allc[n][8:10] + ":" + caption_allc[n][10:12] + " UTC"
                    st.image(imgsc[n],caption=name, width=w)

    elif galery == "NOAA 15":
        st.error("**Here you can see all decoded images of _NOAA 15 satellite_** ⤵️")
        #sorted by the newest.** ⤵️")
        st.text("NOAA satellites do not transmit images with county lines or colored.")
        st.text("By default map overlay feature is applied")
        color = st.checkbox('Add False color')
        if not color:
            for i in range(l):
                n = l-i-1
                if caption_all[n][15] == "5" and caption_all[n][16] == "o":
                    name = "NOAA " + caption_all[n][14:16] + " - " + caption_all[n][0:4] + "/" + caption_all[n][4:6] + "/" + caption_all[n][6:8] + " - " + caption_all[n][8:10] + ":" + caption_all[n][10:12] + " UTC"
                    st.image(imgs[n], caption=name, width=w)
        if color: 
            for i in range(lc):
                n = lc-i-1
                if caption_allc[n][15] == "5" and caption_allc[n][17] == "o":
                    name = "NOAA " + caption_allc[n][14:16] + " - " + caption_allc[n][0:4] + "/" + caption_allc[n][4:6] + "/" + caption_allc[n][6:8] + " - " + caption_allc[n][8:10] + ":" + caption_allc[n][10:12] + " UTC"
                    st.image(imgsc[n],caption=name, width=w)
    
    
    #im.show() 
            
