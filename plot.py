import json
import matplotlib.pyplot as plt
import numpy as np
np.random.seed(1)


class PlotGraphics:
    def __init__(self, virus_country_results, date_sentence):
        self._virus_country_results = virus_country_results
        self._date_sentence = date_sentence
        self._main_scatter = None
        self._current_country = None
        self._main_x = None
        self._main_y = None
        # Annotation setups
        self._norm = plt.Normalize(1, 4)
        self._cmap = plt.cm.RdYlGn
        self._fig, self._ax = plt.subplots()
        self._annotations = self._ax.annotate(
            "",
            xy=(0, 0),
            xytext=(20, 20),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->")
        )
        self._annotations.set_visible(False)

    def plot_page_statistics(self, country):
        self._current_country = country
        stats = self._virus_country_results.get(country)
        self._main_scatter = plt.scatter(stats['Total Coronavirus Cases']["dates"], stats['Total Coronavirus Cases']["values"], s=50)
        self._main_x = stats['Total Coronavirus Cases']["dates"]
        self._main_y = stats['Total Coronavirus Cases']["values"]
        for title, stat in stats.items():
            plt.scatter(stat["dates"], stat["values"], s=50)
        self._fig.canvas.mpl_connect("motion_notify_event", self.hover)
        plt.setp(self._ax.get_xticklabels(), rotation=90, horizontalalignment='right')
        plt.title(country)
        plt.xlabel("Date")
        plt.ylabel("Number of Cases")
        plt.show()

    def hover(self, event):
        vis = self._annotations.get_visible()
        if event.inaxes == self._ax:
            cont, index = self._main_scatter.contains(event)
            if cont:
                self.update_annotation(index)
                self._annotations.set_visible(True)
                self._fig.canvas.draw_idle()
            else:
                if vis:
                    self._annotations.set_visible(False)
                    self._fig.canvas.draw_idle()

    def update_annotation(self, index):
        pos = self._main_scatter.get_offsets()[index["ind"][0]]
        self._annotations.xy = pos
        content = self._date_sentence[f"2020 coronavirus pandemic in {self._current_country}"]
        text = "{}".format(" ".join(content[self._main_x[n]] for n in index["ind"]))
        # plt.title(title)
        # text = "{}".format(" ".join(list(map(str, ind["ind"]))))

        self._annotations.set_text(text)
        self._annotations.get_bbox_patch().set_facecolor(self._cmap(self._norm(3)))
        self._annotations.get_bbox_patch().set_alpha(0.4)


# bg_dict = {'Total Coronavirus Deaths': {'dates': ['Feb 15', 'Feb 16', 'Feb 17', 'Feb 18', 'Feb 19', 'Feb 20', 'Feb 21', 'Feb 22', 'Feb 23', 'Feb 24', 'Feb 25', 'Feb 26', 'Feb 27', 'Feb 28', 'Feb 29', 'Mar 01', 'Mar 02', 'Mar 03', 'Mar 04', 'Mar 05', 'Mar 06', 'Mar 07', 'Mar 08', 'Mar 09', 'Mar 10', 'Mar 11', 'Mar 12', 'Mar 13', 'Mar 14', 'Mar 15', 'Mar 16', 'Mar 17', 'Mar 18', 'Mar 19', 'Mar 20', 'Mar 21', 'Mar 22', 'Mar 23', 'Mar 24', 'Mar 25', 'Mar 26', 'Mar 27', 'Mar 28', 'Mar 29', 'Mar 30', 'Mar 31', 'Apr 01', 'Apr 02', 'Apr 03', 'Apr 04', 'Apr 05', 'Apr 06', 'Apr 07', 'Apr 08', 'Apr 09', 'Apr 10', 'Apr 11', 'Apr 12', 'Apr 13', 'Apr 14', 'Apr 15', 'Apr 16', 'Apr 17', 'Apr 18', 'Apr 19', 'Apr 20', 'Apr 21', 'Apr 22', 'Apr 23', 'Apr 24', 'Apr 25', 'Apr 26', 'Apr 27', 'Apr 28', 'Apr 29', 'Apr 30', 'May 01', 'May 02', 'May 03', 'May 04', 'May 05', 'May 06', 'May 07', 'May 08', 'May 09', 'May 10', 'May 11', 'May 12', 'May 13', 'May 14', 'May 15', 'May 16', 'May 17'], 'values': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 7, 8, 8, 8, 10, 10, 14, 17, 20, 22, 23, 24, 24, 25, 28, 29, 32, 35, 36, 38, 41, 41, 42, 43, 45, 49, 52, 54, 55, 56, 58, 58, 64, 66, 68, 72, 73, 78, 80, 84, 84, 86, 90, 91, 93, 95, 96, 99, 102, 105, 108]}, 'Total Coronavirus Currently Infected': {'dates': ['Feb 15', 'Feb 16', 'Feb 17', 'Feb 18', 'Feb 19', 'Feb 20', 'Feb 21', 'Feb 22', 'Feb 23', 'Feb 24', 'Feb 25', 'Feb 26', 'Feb 27', 'Feb 28', 'Feb 29', 'Mar 01', 'Mar 02', 'Mar 03', 'Mar 04', 'Mar 05', 'Mar 06', 'Mar 07', 'Mar 08', 'Mar 09', 'Mar 10', 'Mar 11', 'Mar 12', 'Mar 13', 'Mar 14', 'Mar 15', 'Mar 16', 'Mar 17', 'Mar 18', 'Mar 19', 'Mar 20', 'Mar 21', 'Mar 22', 'Mar 23', 'Mar 24', 'Mar 25', 'Mar 26', 'Mar 27', 'Mar 28', 'Mar 29', 'Mar 30', 'Mar 31', 'Apr 01', 'Apr 02', 'Apr 03', 'Apr 04', 'Apr 05', 'Apr 06', 'Apr 07', 'Apr 08', 'Apr 09', 'Apr 10', 'Apr 11', 'Apr 12', 'Apr 13', 'Apr 14', 'Apr 15', 'Apr 16', 'Apr 17', 'Apr 18', 'Apr 19', 'Apr 20', 'Apr 21', 'Apr 22', 'Apr 23', 'Apr 24', 'Apr 25', 'Apr 26', 'Apr 27', 'Apr 28', 'Apr 29', 'Apr 30', 'May 01', 'May 02', 'May 03', 'May 04', 'May 05', 'May 06', 'May 07', 'May 08', 'May 09', 'May 10', 'May 11', 'May 12', 'May 13', 'May 14', 'May 15', 'May 16', 'May 17'], 'values': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 6, 6, 22, 30, 39, 49, 60, 79, 90, 104, 123, 157, 181, 195, 212, 235, 253, 281, 313, 324, 334, 374, 392, 422, 441, 452, 474, 488, 512, 527, 546, 556, 571, 578, 582, 597, 606, 640, 664, 684, 691, 719, 760, 801, 855, 941, 995, 1039, 1099, 1119, 1140, 1174, 1211, 1235, 1237, 1253, 1282, 1334, 1361, 1385, 1409, 1430, 1436, 1452, 1474, 1470, 1491, 1497, 1505]}, 'Total Coronavirus Cases': {'dates': ['Feb 15', 'Feb 16', 'Feb 17', 'Feb 18', 'Feb 19', 'Feb 20', 'Feb 21', 'Feb 22', 'Feb 23', 'Feb 24', 'Feb 25', 'Feb 26', 'Feb 27', 'Feb 28', 'Feb 29', 'Mar 01', 'Mar 02', 'Mar 03', 'Mar 04', 'Mar 05', 'Mar 06', 'Mar 07', 'Mar 08', 'Mar 09', 'Mar 10', 'Mar 11', 'Mar 12', 'Mar 13', 'Mar 14', 'Mar 15', 'Mar 16', 'Mar 17', 'Mar 18', 'Mar 19', 'Mar 20', 'Mar 21', 'Mar 22', 'Mar 23', 'Mar 24', 'Mar 25', 'Mar 26', 'Mar 27', 'Mar 28', 'Mar 29', 'Mar 30', 'Mar 31', 'Apr 01', 'Apr 02', 'Apr 03', 'Apr 04', 'Apr 05', 'Apr 06', 'Apr 07', 'Apr 08', 'Apr 09', 'Apr 10', 'Apr 11', 'Apr 12', 'Apr 13', 'Apr 14', 'Apr 15', 'Apr 16', 'Apr 17', 'Apr 18', 'Apr 19', 'Apr 20', 'Apr 21', 'Apr 22', 'Apr 23', 'Apr 24', 'Apr 25', 'Apr 26', 'Apr 27', 'Apr 28', 'Apr 29', 'Apr 30', 'May 01', 'May 02', 'May 03', 'May 04', 'May 05', 'May 06', 'May 07', 'May 08', 'May 09', 'May 10', 'May 11', 'May 12', 'May 13', 'May 14', 'May 15', 'May 16', 'May 17'], 'values': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 6, 7, 23, 31, 41, 51, 62, 81, 92, 107, 127, 163, 187, 201, 218, 242, 264, 293, 331, 346, 359, 399, 422, 457, 485, 503, 531, 549, 577, 593, 618, 635, 661, 675, 685, 713, 747, 800, 846, 878, 894, 929, 975, 1024, 1097, 1188, 1247, 1300, 1363, 1399, 1447, 1506, 1555, 1594, 1618, 1652, 1704, 1778, 1829, 1872, 1921, 1965, 1990, 2023, 2069, 2100, 2138, 2175, 2211]}, 'Novel Coronavirus Daily Deaths': {'dates': ['Feb 15', 'Feb 16', 'Feb 17', 'Feb 18', 'Feb 19', 'Feb 20', 'Feb 21', 'Feb 22', 'Feb 23', 'Feb 24', 'Feb 25', 'Feb 26', 'Feb 27', 'Feb 28', 'Feb 29', 'Mar 01', 'Mar 02', 'Mar 03', 'Mar 04', 'Mar 05', 'Mar 06', 'Mar 07', 'Mar 08', 'Mar 09', 'Mar 10', 'Mar 11', 'Mar 12', 'Mar 13', 'Mar 14', 'Mar 15', 'Mar 16', 'Mar 17', 'Mar 18', 'Mar 19', 'Mar 20', 'Mar 21', 'Mar 22', 'Mar 23', 'Mar 24', 'Mar 25', 'Mar 26', 'Mar 27', 'Mar 28', 'Mar 29', 'Mar 30', 'Mar 31', 'Apr 01', 'Apr 02', 'Apr 03', 'Apr 04', 'Apr 05', 'Apr 06', 'Apr 07', 'Apr 08', 'Apr 09', 'Apr 10', 'Apr 11', 'Apr 12', 'Apr 13', 'Apr 14', 'Apr 15', 'Apr 16', 'Apr 17', 'Apr 18', 'Apr 19', 'Apr 20', 'Apr 21', 'Apr 22', 'Apr 23', 'Apr 24', 'Apr 25', 'Apr 26', 'Apr 27', 'Apr 28', 'Apr 29', 'Apr 30', 'May 01', 'May 02', 'May 03', 'May 04', 'May 05', 'May 06', 'May 07', 'May 08', 'May 09', 'May 10', 'May 11', 'May 12', 'May 13', 'May 14', 'May 15', 'May 16', 'May 17'], 'values': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 0, 0, 2, 0, 4, 3, 3, 2, 1, 1, 0, 1, 3, 1, 3, 3, 1, 2, 3, 0, 1, 1, 2, 4, 3, 2, 1, 1, 2, 0, 6, 2, 2, 4, 1, 5, 2, 4, 0, 2, 4, 1, 2, 2, 1, 3, 3, 3, 3]}, 'Novel Coronavirus Daily Cases': {'dates': ['Feb 15', 'Feb 16', 'Feb 17', 'Feb 18', 'Feb 19', 'Feb 20', 'Feb 21', 'Feb 22', 'Feb 23', 'Feb 24', 'Feb 25', 'Feb 26', 'Feb 27', 'Feb 28', 'Feb 29', 'Mar 01', 'Mar 02', 'Mar 03', 'Mar 04', 'Mar 05', 'Mar 06', 'Mar 07', 'Mar 08', 'Mar 09', 'Mar 10', 'Mar 11', 'Mar 12', 'Mar 13', 'Mar 14', 'Mar 15', 'Mar 16', 'Mar 17', 'Mar 18', 'Mar 19', 'Mar 20', 'Mar 21', 'Mar 22', 'Mar 23', 'Mar 24', 'Mar 25', 'Mar 26', 'Mar 27', 'Mar 28', 'Mar 29', 'Mar 30', 'Mar 31', 'Apr 01', 'Apr 02', 'Apr 03', 'Apr 04', 'Apr 05', 'Apr 06', 'Apr 07', 'Apr 08', 'Apr 09', 'Apr 10', 'Apr 11', 'Apr 12', 'Apr 13', 'Apr 14', 'Apr 15', 'Apr 16', 'Apr 17', 'Apr 18', 'Apr 19', 'Apr 20', 'Apr 21', 'Apr 22', 'Apr 23', 'Apr 24', 'Apr 25', 'Apr 26', 'Apr 27', 'Apr 28', 'Apr 29', 'Apr 30', 'May 01', 'May 02', 'May 03', 'May 04', 'May 05', 'May 06', 'May 07', 'May 08', 'May 09', 'May 10', 'May 11', 'May 12', 'May 13', 'May 14', 'May 15', 'May 16', 'May 17'], 'values': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 1, 16, 8, 10, 10, 11, 19, 11, 15, 20, 36, 24, 14, 17, 24, 22, 29, 38, 15, 13, 40, 23, 35, 28, 18, 28, 18, 28, 16, 25, 17, 26, 14, 10, 28, 34, 53, 46, 32, 16, 35, 46, 49, 73, 91, 59, 53, 63, 36, 48, 59, 49, 39, 24, 34, 52, 74, 51, 43, 49, 44, 25, 33, 46, 31, 38, 37, 36]}}
# with open('dates_sentences.json') as json_file:
#     date_sentence = json.load(json_file)
# # date_sentence = json.loads(".dates_sentences.json")
# x = bg_dict["Total Coronavirus Cases"]["dates"]
# y = bg_dict["Total Coronavirus Cases"]["values"]
# x1 = bg_dict["Total Coronavirus Deaths"]["dates"]
# y1 = bg_dict["Total Coronavirus Deaths"]["values"]
# # x = np.random.rand(15)
# # y = np.random.rand(15)
# names = np.array(list("ABCDEFGHIJKLMNO"))
# c = np.random.randint(1, 5, size=93)
#
# norm = plt.Normalize(1, 4)
# cmap = plt.cm.RdYlGn
#
# fig, ax = plt.subplots()
# sc = plt.scatter(x, y, s=50)
# sc1 = plt.scatter(x1, y1, s=50)
#
# annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot.set_visible(False)
#
#
# def update_annot(ind):
#
#     pos = sc.get_offsets()[ind["ind"][0]]
#     annot.xy = pos
#     content = date_sentence["2020 coronavirus pandemic in Bulgaria"]
#     text = "{}".format(" ".join(content[x[n]] for n in ind["ind"]))
#     # plt.title(title)
#     # text = "{}".format(" ".join(list(map(str, ind["ind"]))))
#
#     annot.set_text(text)
#     annot.get_bbox_patch().set_facecolor(cmap(norm(3)))
#     annot.get_bbox_patch().set_alpha(0.4)
#
#
# def hover(event):
#     vis = annot.get_visible()
#     if event.inaxes == ax:
#         cont, ind = sc.contains(event)
#         if cont:
#             update_annot(ind)
#             annot.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot.set_visible(False)
#                 fig.canvas.draw_idle()
#
#
# fig.canvas.mpl_connect("motion_notify_event", hover)
# plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
# plt.xlabel("Date")
# plt.ylabel("Number of Cases")
# plt.show()
