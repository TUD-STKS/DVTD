global baseName;

baseName = {
    '../subject-1/s1-01-bahn-tense-a/s1-01-bahn-tense-a';
    '../subject-1/s1-02-beet-tense-e/s1-02-beet-tense-e';
    '../subject-1/s1-03-tiere-tense-i/s1-03-tiere-tense-i';
    '../subject-1/s1-04-boote-tense-o/s1-04-boote-tense-o';
    '../subject-1/s1-05-bude-tense-u/s1-05-bude-tense-u';
    '../subject-1/s1-06-laehmung-tense-ae/s1-06-laehmung-tense-ae';
    '../subject-1/s1-07-hoehle-tense-oe/s1-07-hoehle-tense-oe';
    '../subject-1/s1-08-guete-tense-y/s1-08-guete-tense-y';
    '../subject-1/s1-09-los-l/s1-09-los-l';
    '../subject-1/s1-10-fahrt-f/s1-10-fahrt-f';
    '../subject-1/s1-11-bass-s/s1-11-bass-s';
    '../subject-1/s1-12-schoen-sh/s1-12-schoen-sh';
    '../subject-1/s1-13-ich-c/s1-13-ich-c';
    '../subject-1/s1-14-ach-x/s1-14-ach-x';
    '../subject-1/s1-15-bass-lax-a/s1-15-bass-lax-a';
    '../subject-1/s1-16-bett-lax-ae/s1-16-bett-lax-ae';
    '../subject-1/s1-17-mit-lax-i/s1-17-mit-lax-i';
    '../subject-1/s1-18-offen-lax-o/s1-18-offen-lax-o';
    '../subject-1/s1-19-butter-lax-u/s1-19-butter-lax-u';
    '../subject-1/s1-20-muetter-lax-y/s1-20-muetter-lax-y';
    '../subject-1/s1-21-goetter-lax-oe/s1-21-goetter-lax-oe';
    '../subject-1/s1-22-ehe-schwa/s1-22-ehe-schwa';
    '../subject-2/s2-01-bahn-tense-a/s2-01-bahn-tense-a';
    '../subject-2/s2-02-beet-tense-e/s2-02-beet-tense-e';
    '../subject-2/s2-03-tiere-tense-i/s2-03-tiere-tense-i';
    '../subject-2/s2-04-boote-tense-o/s2-04-boote-tense-o';
    '../subject-2/s2-05-bude-tense-u/s2-05-bude-tense-u';
    '../subject-2/s2-06-laehmung-tense-ae/s2-06-laehmung-tense-ae';
    '../subject-2/s2-07-hoehle-tense-oe/s2-07-hoehle-tense-oe';
    '../subject-2/s2-08-guete-tense-y/s2-08-guete-tense-y';
    '../subject-2/s2-09-los-l/s2-09-los-l';
    '../subject-2/s2-10-fahrt-f/s2-10-fahrt-f';
    '../subject-2/s2-11-bass-s/s2-11-bass-s';
    '../subject-2/s2-12-schoen-sh/s2-12-schoen-sh';
    '../subject-2/s2-13-ich-c/s2-13-ich-c';
    '../subject-2/s2-14-ach-x/s2-14-ach-x';
    '../subject-2/s2-15-bass-lax-a/s2-15-bass-lax-a';
    '../subject-2/s2-16-bett-lax-ae/s2-16-bett-lax-ae';
    '../subject-2/s2-17-mit-lax-i/s2-17-mit-lax-i';
    '../subject-2/s2-18-offen-lax-o/s2-18-offen-lax-o';
    '../subject-2/s2-19-butter-lax-u/s2-19-butter-lax-u';
    '../subject-2/s2-20-muetter-lax-y/s2-20-muetter-lax-y';
    '../subject-2/s2-21-goetter-lax-oe/s2-21-goetter-lax-oe';
    '../subject-2/s2-22-ehe-schwa/s2-22-ehe-schwa';
};

numItems = length(baseName);

currItem = 1;

disp('Use the keys <Arrow Left> and <Arrow Right> to change the displayed item. Use ESC to exit.');

% *******************************************************************
% *******************************************************************

while 1
    displayItem(baseName{currItem});
    
    waitforbuttonpress;
    lastKey = double(get(gcf,'CurrentCharacter'));

    % ESC key.
    if (lastKey == 27)
        close;
        return;     % Stop execution of this script.
    % Left arrow key.
    elseif (lastKey == 28)
        if (currItem > 1)
            currItem = currItem - 1;
        end
    % Right arrow key.
    elseif (lastKey == 29)
        if (currItem < numItems)
            currItem = currItem + 1;
        end
    end
end

% *******************************************************************
% *******************************************************************

function displayItem(baseName)

    % ***************************************************************
    % Plot the *measured* volume velocity transfer function.
    % ***************************************************************

    fileName = [baseName '-vvtf-measured.txt'];
    if exist(fileName, 'file')
        data = dlmread(fileName, ' ', 1, 0);    % Skip the first row.
        frequencies_Hz = data(:, 1);
        magnitudes_dB = 20.0*log10(data(:, 2));

        subplot(2, 2, 1);
        plot(frequencies_Hz, magnitudes_dB, 'k');

        xlim([0, 10000]);
        title('Volume velocity transfer function (red=calculated, black=measured)');
        xlabel('Frequency in Hz');
        ylabel('Magnitude in dB');
        grid on;
    else
        plot([0, 10000], [0, 0], 'k');
        title(['FILE NOT FOUND : ' fileName]);
    end

    % ***************************************************************
    % Plot the *calculated* volume velocity transfer function.
    % ***************************************************************

    fileName = [baseName '-vvtf-calculated.txt'];
    if exist(fileName, 'file')
        data = dlmread(fileName, ' ', 1, 0);    % Skip the first row.
        frequencies_Hz = data(:, 1);
        magnitudes_dB = 20.0*log10(data(:, 2));

        subplot(2, 2, 1);
        hold on;
        plot(frequencies_Hz, magnitudes_dB, 'r');
        hold off;

        title('Volume velocity transfer function (red=calculated, black=measured)');
        xlabel('Frequency in Hz');
        ylabel('Magnitude in dB');
        grid on;
    else
        hold on;
        plot([0, 10000], [0, 0], 'r');
        hold off;
        title(['FILE NOT FOUND : ' fileName]);
    end

    % ***************************************************************
    % Plot the measured noise spectra.
    % ***************************************************************

    subplot(2, 2, 3);

    fileName = [baseName '-noise-psd.txt'];

    if exist(fileName, 'file')
        psdData = dlmread(fileName, ' ', 4, 0);
        freq = psdData(:, 1);
        psd500mW = psdData(:, 2);
        psd1000mW = psdData(:, 3);
        psd1500mW = psdData(:, 4);
        psd2000mW = psdData(:, 5);
        psd2500mW = psdData(:, 6);
        psd3000mW = psdData(:, 7);

        p_ref_Pa = 2e-5;
        logReference = p_ref_Pa * p_ref_Pa / 1.0;   % Bandwidth is 1.0 Hz.

        % Take the log10() of the power values relative to p_ref^2.
        maxIndex = 214;     % Corresponds to 10 kHz.
        plot(freq(1:maxIndex), 10*log10(psd500mW(1:maxIndex) / logReference), 'k', ...
            freq(1:maxIndex), 10*log10(psd1000mW(1:maxIndex) / logReference), 'r', ...
            freq(1:maxIndex), 10*log10(psd1500mW(1:maxIndex) / logReference), 'g', ...
            freq(1:maxIndex), 10*log10(psd2000mW(1:maxIndex) / logReference), 'b', ...
            freq(1:maxIndex), 10*log10(psd2500mW(1:maxIndex) / logReference), 'k', ...
            freq(1:maxIndex), 10*log10(psd3000mW(1:maxIndex) / logReference), 'r');

        title('PSDs of radiated noise at flow power levels of 0.5, 1, 1.5, 2, 2.5, 3 W');
        xlim([0, 10000]);
        xlabel('Frequency in Hz');
        ylabel('PSD in dB (re. [2*10^-5 Pa]^2/[1 Hz])');
        grid on;
    else
        plot([0, 10000], [0, 0], 'k');
        title(['FILE NOT FOUND : ' fileName]);
    end
    
    % ***************************************************************
    % Plot the metadata for the noise spectra.
    % ***************************************************************
    
    fileName = [baseName '-noise-metadata.txt'];
    
    if exist(fileName, 'file')
        metaData = dlmread(fileName, ' ', 6, 0);

        % One plot for the pressure-flow relationship.

        subplot(2, 2, 2);
        flowSamples = metaData(:, 2);
        pressureSamples = metaData(:, 3);
        % Plot flow in cm^3/s instead of m^3/s.
        plot(pressureSamples, flowSamples*1000000, '-o');
        xlabel('Mean subglottal pressure in Pa');
        ylabel('Mean flow in cm^3/s');
        grid on;
        title('Flow vs. subglottal pressure');
        
        % One plot for the flow power vs. SPL of the radiated sound.

        subplot(2, 2, 4);
        powerSamples = metaData(:, 1);
        splSamples = metaData(:, 4);
        plot(powerSamples, splSamples, '-o');
        xlabel('Flow power in W');
        ylabel('SPL in dB');
        grid on;
        title('SPL of radiated noise vs. flow power');
        xlim([0, 3]);       % The measured range is 0 ... 3 W.
        
    else
        subplot(2, 2, 2);
        plot([0, 1], [0, 0], 'k');
        title(['FILE NOT FOUND : ' fileName]);

        subplot(2, 2, 4);
        plot([0, 1], [0, 0], 'k');
        title(['FILE NOT FOUND : ' fileName]);
    end
    
    % ***************************************************************
    % Put a super title on top of all subplots.
    % ***************************************************************

    % Extract the itemName as the substring after the last shlash '/' in the
    % baseName.
    slashPos = strfind(baseName, '/');
    if (length(slashPos) > 0)
        itemName = extractAfter(baseName, slashPos(length(slashPos)));
    else
        itemName = 'UNKNOWN';
    end
        
    suptitle(itemName);
end

% *******************************************************************
