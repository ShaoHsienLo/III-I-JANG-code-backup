from datatransformation import get_fft_values, get_psd_values, get_autocorr_values
import matplotlib.pyplot as plt
import numpy as np
import os

self_labels = [
    ["NG", "NG", "NG", "NG"], ["NG", "NG", "NG", "NG"], ["NG", "OK", "NG", "NG"], ["NG", "NG", "NG", "OK"],
    ["NG", "NG", "NG", "NG"], ["NG", "NG", "NG", "OK"], ["NG", "OK", "NG", "NG"], ["NG", "NG", "NG", "NG"],
    ["NG", "OK", "NG", "NG"]
]
label_lst = []
for _, lst in enumerate(self_labels):
    for label in lst:
        label_lst.append(label)
label_lst = np.array(label_lst)

data = np.load("data.npy")
data = data.reshape(data.shape[0], data.shape[1])
N = 1500
t_n = 1
T = t_n / N
f_s = 1000
for i, lst in enumerate(data):

    # autocorr
    x_val, y_val = get_autocorr_values(lst, T, N)
    plt.plot(x_val, y_val, linestyle="-", color="blue", label=label_lst[i])
    plt.xlabel('Time delay [s]')
    plt.ylabel('Autocorrelation amplitude')
    plt.legend()
    plt.savefig(os.path.join(r"C:\Users\samuello\Downloads\III\2022專案\韌性\code\graph\autocorr",
                             "autocorr_{}_{}".format(i, label_lst[i])))
    plt.close()

    # psd
    # x_val, y_val = get_psd_values(lst, f_s)
    # plt.plot(x_val, y_val, linestyle="-", color="blue", label=label_lst[i])
    # plt.xlabel('Frequency [Hz]')
    # plt.ylabel('PSD [V**2 / Hz]')
    # plt.legend()
    # plt.savefig(os.path.join(r"C:\Users\samuello\Downloads\III\2022專案\韌性\code\graph\psd",
    #                          "psd_{}_{}".format(i, label_lst[i])))
    # plt.close()

    # fft
    # x_val, y_val = get_fft_values(lst, T, N)
    # plt.plot(x_val, y_val, linestyle="-", color="blue", label=label_lst[i])
    # plt.xlabel("Frequency [Hz]", fontsize=16)
    # plt.ylabel("Amplitude", fontsize=16)
    # plt.title("Frequency domain of the signal", fontsize=16)
    # plt.legend()
    # plt.savefig(os.path.join(r"C:\Users\samuello\Downloads\III\2022專案\韌性\code\graph\fft",
    #                          "fft_{}_{}".format(i, label_lst[i])))
    # plt.close()



