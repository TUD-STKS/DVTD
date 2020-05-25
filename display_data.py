# Requirements:
# matplotlib==3.1.3
# numpy==1.18.1

import os.path
import numpy as np
import matplotlib.pyplot as plt
import sys


def OnKeyPressed(event):
    global currItem
    sys.stdout.flush()
    # ESC key
    if event.key == 'escape':
        plt.close()
        quit()
    # Left arrow key
    elif event.key == 'left':
        if currItem > 0:
            currItem = currItem - 1
    # Right arrow key
    elif event.key == 'right':
        if currItem < numItems - 1:
            currItem = currItem + 1


def displayItem(baseName):
    """
    Display a set of plots corresponding to a single item.
    """
    global fig, axs
    fig.clf()
    axs = np.array([[fig.add_subplot(221), fig.add_subplot(222)],
                    [fig.add_subplot(223), fig.add_subplot(224)]])
    """
    Plot the *measured* volume velocity transfer function.
    """
    fileName = baseName + '-vvtf-measured.txt'
    if os.path.isfile(fileName):
        data = np.genfromtxt(fileName, delimiter=' ', skip_header=1)
        frequencies_Hz = data[:, 0]
        magnitudes_dB = 20.0 * np.log10(data[:, 1])
        axs[0, 0].plot(frequencies_Hz, magnitudes_dB, 'k')
        axs[0, 0].set_xlim(0, 10000)
        axs[0, 0].set_title('Volume velocity transfer function \n(red=calculated, black=measured)')
        axs[0, 0].set_xlabel('Frequency in Hz')
        axs[0, 0].set_ylabel('Magnitude in dB')
        axs[0, 0].grid(True)
    else:
        axs[0, 0].plot([0, 10000], [0, 0], 'k')
        axs[0, 0].set_title('FILE NOT FOUND : ' + fileName)
    """
    Plot the *calculated* volume velocity transfer function.
    """
    fileName = baseName + '-vvtf-calculated.txt'
    if os.path.isfile(fileName):
        data = np.genfromtxt(fileName, delimiter=' ', skip_header=1)
        frequencies_Hz = data[:, 0]
        magnitudes_dB = 20.0 * np.log10(data[:, 1])
        axs[0, 0].plot(frequencies_Hz, magnitudes_dB, 'r')
        axs[0, 0].set_xlim(0, 10000)
        axs[0, 0].set_title('Volume velocity transfer function \n(red=calculated, black=measured)')
        axs[0, 0].set_xlabel('Frequency in Hz')
        axs[0, 0].set_ylabel('Magnitude in dB')
        axs[0, 0].grid(True)
    else:
        axs[0, 0].plot([0, 10000], [0, 0], 'r')
        axs[0, 0].set_title('FILE NOT FOUND : ' + fileName)
    """
    Plot the measured noise spectra.
    """
    fileName = baseName + '-noise-psd.txt'
    if os.path.isfile(fileName):
        psdData = np.genfromtxt(fileName, delimiter=' ', skip_header=4)
        freq = psdData[:, 0]
        psd500mW = psdData[:, 1]
        psd1000mW = psdData[:, 2]
        psd1500mW = psdData[:, 3]
        psd2000mW = psdData[:, 4]
        psd2500mW = psdData[:, 5]
        psd3000mW = psdData[:, 6]
        p_ref_Pa = 2e-5
        logReference = p_ref_Pa * p_ref_Pa / 1.0  # Bandwidth is 1.0 Hz.
        # Take the log10() of the power values relative to p_ref^2.
        maxIndex = 214  # Corresponds to 10 kHz.
        axs[1, 0].plot(freq[: maxIndex], 10 * np.log10(psd500mW[: maxIndex] / logReference), 'k',
                       freq[: maxIndex], 10 * np.log10(psd1000mW[: maxIndex] / logReference), 'r',
                       freq[: maxIndex], 10 * np.log10(psd1500mW[: maxIndex] / logReference), 'g',
                       freq[: maxIndex], 10 * np.log10(psd2000mW[: maxIndex] / logReference), 'b',
                       freq[: maxIndex], 10 * np.log10(psd2500mW[: maxIndex] / logReference), 'k',
                       freq[: maxIndex], 10 * np.log10(psd3000mW[: maxIndex] / logReference), 'r')
        axs[1, 0].set_title('PSDs of radiated noise\nat flow power levels of\n0.5, 1, 1.5, 2, 2.5, 3 W')
        axs[1, 0].set_xlim(0, 10000)
        axs[1, 0].set_xlabel('Frequency in Hz')
        axs[1, 0].set_ylabel('PSD in dB (re. [2*10e-5 Pa]^2/[1 Hz])')
        axs[1, 0].grid(True)
    else:
        axs[1, 0].plot([0, 10000], [0, 0], 'k')
        axs[1, 0].set_title('FILE NOT FOUND : ' + fileName)

    """
    Plot the metadata for the noise spectra.
    """
    fileName = baseName + '-noise-metadata.txt'
    if os.path.isfile(fileName):
        metaData = np.genfromtxt(fileName, delimiter=' ', skip_header=6)

        # One plot for the pressure-flow relationship.

        flowSamples = metaData[:, 1]
        pressureSamples = metaData[:, 2]
        # Plot flow in cm^3/s instead of m^3/s.
        axs[0, 1].plot(pressureSamples, flowSamples * 1000000, '-o')
        axs[0, 1].set_xlabel('Mean subglottal pressure in Pa')
        axs[0, 1].set_ylabel('Mean flow in cm^3/s')
        axs[0, 1].grid(True)
        axs[0, 1].set_title('Flow vs. subglottal pressure')

        # One plot for the flow power vs. SPL of the radiated sound.

        powerSamples = metaData[:, 0]
        splSamples = metaData[:, 3];
        axs[1, 1].plot(powerSamples, splSamples, '-o')
        axs[1, 1].set_xlabel('Flow power in W')
        axs[1, 1].set_ylabel('SPL in dB')
        axs[1, 1].grid(True)
        axs[1, 1].set_title('SPL of radiated noise vs. flow power')
        axs[1, 1].set_xlim(0, 3)  # The measured range is 0 ... 3 W.
    else:
        axs[1, 1].plot([0, 1], [0, 0], 'k')
        axs[1, 1].set_title('FILE NOT FOUND : ' + fileName)

        axs[1, 1].plot([0, 1], [0, 0], 'k')
        axs[1, 1].set_title('FILE NOT FOUND : ' + fileName)

    """
    Put a super title on top of all subplots.
    """

    # Extract the itemName as the substring after the last slash '/' in the
    # baseName.
    slashPos = baseName.rfind('/')
    if slashPos >= 0:
        itemName = baseName[slashPos + 1:]
    else:
        itemName = 'UNKNOWN'

    plt.suptitle(itemName)
    plt.subplots_adjust(top=0.86, bottom=0.16, left=0.11, right=0.9, hspace=1.0, wspace=0.7)
    plt.draw()


if __name__ == '__main__':
    baseNames = [
        '../subject-1/s1-01-bahn-tense-a/s1-01-bahn-tense-a',
        '../subject-1/s1-02-beet-tense-e/s1-02-beet-tense-e',
        '../subject-1/s1-03-tiere-tense-i/s1-03-tiere-tense-i',
        '../subject-1/s1-04-boote-tense-o/s1-04-boote-tense-o',
        '../subject-1/s1-05-bude-tense-u/s1-05-bude-tense-u',
        '../subject-1/s1-06-laehmung-tense-ae/s1-06-laehmung-tense-ae',
        '../subject-1/s1-07-hoehle-tense-oe/s1-07-hoehle-tense-oe',
        '../subject-1/s1-08-guete-tense-y/s1-08-guete-tense-y',
        '../subject-1/s1-09-los-l/s1-09-los-l',
        '../subject-1/s1-10-fahrt-f/s1-10-fahrt-f',
        '../subject-1/s1-11-bass-s/s1-11-bass-s',
        '../subject-1/s1-12-schoen-sh/s1-12-schoen-sh',
        '../subject-1/s1-13-ich-c/s1-13-ich-c',
        '../subject-1/s1-14-ach-x/s1-14-ach-x',
        '../subject-1/s1-15-bass-lax-a/s1-15-bass-lax-a',
        '../subject-1/s1-16-bett-lax-ae/s1-16-bett-lax-ae',
        '../subject-1/s1-17-mit-lax-i/s1-17-mit-lax-i',
        '../subject-1/s1-18-offen-lax-o/s1-18-offen-lax-o',
        '../subject-1/s1-19-butter-lax-u/s1-19-butter-lax-u',
        '../subject-1/s1-20-muetter-lax-y/s1-20-muetter-lax-y',
        '../subject-1/s1-21-goetter-lax-oe/s1-21-goetter-lax-oe',
        '../subject-1/s1-22-ehe-schwa/s1-22-ehe-schwa',
        '../subject-2/s2-01-bahn-tense-a/s2-01-bahn-tense-a',
        '../subject-2/s2-02-beet-tense-e/s2-02-beet-tense-e',
        '../subject-2/s2-03-tiere-tense-i/s2-03-tiere-tense-i',
        '../subject-2/s2-04-boote-tense-o/s2-04-boote-tense-o',
        '../subject-2/s2-05-bude-tense-u/s2-05-bude-tense-u',
        '../subject-2/s2-06-laehmung-tense-ae/s2-06-laehmung-tense-ae',
        '../subject-2/s2-07-hoehle-tense-oe/s2-07-hoehle-tense-oe',
        '../subject-2/s2-08-guete-tense-y/s2-08-guete-tense-y',
        '../subject-2/s2-09-los-l/s2-09-los-l',
        '../subject-2/s2-10-fahrt-f/s2-10-fahrt-f',
        '../subject-2/s2-11-bass-s/s2-11-bass-s',
        '../subject-2/s2-12-schoen-sh/s2-12-schoen-sh',
        '../subject-2/s2-13-ich-c/s2-13-ich-c',
        '../subject-2/s2-14-ach-x/s2-14-ach-x',
        '../subject-2/s2-15-bass-lax-a/s2-15-bass-lax-a',
        '../subject-2/s2-16-bett-lax-ae/s2-16-bett-lax-ae',
        '../subject-2/s2-17-mit-lax-i/s2-17-mit-lax-i',
        '../subject-2/s2-18-offen-lax-o/s2-18-offen-lax-o',
        '../subject-2/s2-19-butter-lax-u/s2-19-butter-lax-u',
        '../subject-2/s2-20-muetter-lax-y/s2-20-muetter-lax-y',
        '../subject-2/s2-21-goetter-lax-oe/s2-21-goetter-lax-oe',
        '../subject-2/s2-22-ehe-schwa/s2-22-ehe-schwa'
    ]
    numItems = len(baseNames)
    currItem = 0
    # plt.rcParams['toolbar'] = 'None'
    fig, axs = plt.subplots(2, 2)
    plt.ion()
    fig.canvas.mpl_connect('key_press_event', OnKeyPressed)
    print('Use the keys <Arrow Left> and <Arrow Right> to change the displayed item. Use ESC to exit.')

    # ****************************************************************************************************
    # ****************************************************************************************************

    while True:
        displayItem(baseNames[currItem])
        plt.waitforbuttonpress(timeout=-1)
        # Changing the current item or quitting is handled in OnKeyPress()
