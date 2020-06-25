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
            plt.scatter(stat["dates"], stat["values"], s=50, label=title)
        self._fig.canvas.mpl_connect("motion_notify_event", self.hover)
        plt.setp(self._ax.get_xticklabels(), rotation=90, horizontalalignment='right')
        plt.title(country)
        plt.xlabel("Date")
        plt.ylabel("Number of Cases")
        self._ax.legend()
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

        self._annotations.set_text(text)
        self._annotations.get_bbox_patch().set_facecolor(self._cmap(self._norm(3)))
        self._annotations.get_bbox_patch().set_alpha(0.4)
