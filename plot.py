import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import ticker
from matplotlib.colors import ListedColormap
from matplotlib.dates import date2num
from scipy import stats as sps
from scipy.interpolate import interp1d
np.random.seed(1)


class PlotGraphics:
    def __init__(self, virus_country_results, date_sentence):
        self._virus_country_results = virus_country_results
        self._date_sentence = date_sentence
        self._main_scatter = None
        self._current_country = None
        self._main_x = None
        self._main_y = None

        # Rt setup
        self._R_T_MAX = 12
        self._r_t_range = np.linspace(0, self._R_T_MAX, self._R_T_MAX * 100 + 1)
        self._GAMMA = 1 / 7

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

    def rt_stats(self, country):
        # We create an array for every possible value of Rt

        year = "2019-20" if country == "mainland China" else "2020"
        cases_raw = self._virus_country_results[country]["Total Coronavirus Cases"]
        cases = dict(zip(cases_raw["dates"], cases_raw["values"]))
        original, smoothed = self.prepare_cases(cases)

        original.plot(title=f"Total Coronavirus Cases per Day in {country}",
                      c='k',
                      linestyle=':',
                      alpha=.5,
                      label='Actual',
                      legend=True,
                      figsize=(500 / 72, 300 / 72))

        ax = smoothed.plot(label='Smoothed',
                           legend=True)

        ax.get_figure().set_facecolor('w')

        posteriors, log_likelihood = self.get_posteriors(smoothed)

        ax = posteriors.plot(title=f'{country} - Daily Posterior for $R_t$',
                             legend=False,
                             lw=1,
                             c='k',
                             alpha=.3,
                             xlim=(0.4, 6))

        ax.set_xlabel('$R_t$')

        hdi = self.highest_density_interval(posteriors)
        print(hdi.tail())

        # Note that this takes a while to execute - it's not the most efficient algorithm
        hdis = self.highest_density_interval(posteriors, p=.9)

        most_likely = posteriors.idxmax().rename('ML')

        # Look into why you shift -1
        result = pd.concat([most_likely, hdis], axis=1)

        print(result.tail())

        fig, ax = plt.subplots(figsize=(2000 / 72, 500 / 72))

        self.plot_rt(result, ax, country, fig)
        ax.set_title(f'Real-time $R_t$ for {country}')
        plt.show()

    def prepare_cases(self, cases, cutoff=25):
        cases_series = pd.Series(cases, index=cases.keys())
        new_cases = cases_series.diff()
        smoothed = new_cases.rolling(7,
                                     win_type='gaussian',
                                     min_periods=1,
                                     center=True).mean(std=2).round()

        idx_start = np.searchsorted(smoothed, cutoff)

        smoothed = smoothed.iloc[idx_start:]
        original = new_cases.loc[smoothed.index]

        return original, smoothed

    def get_posteriors(self, sr, sigma=0.15):
        # (1) Calculate Lambda
        lam = sr[:-1].values * np.exp(self._GAMMA * (self._r_t_range[:, None] - 1))

        # (2) Calculate each day's likelihood
        likelihoods = pd.DataFrame(
            data=sps.poisson.pmf(sr[1:].values, lam),
            index=self._r_t_range,
            columns=sr.index[1:])

        # (3) Create the Gaussian Matrix
        process_matrix = sps.norm(loc=self._r_t_range,
                                  scale=sigma
                                  ).pdf(self._r_t_range[:, None])

        # (3a) Normalize all rows to sum to 1
        process_matrix /= process_matrix.sum(axis=0)

        # (4) Calculate the initial prior
        # prior0 = sps.gamma(a=4).pdf(r_t_range)
        prior0 = np.ones_like(self._r_t_range) / len(self._r_t_range)
        prior0 /= prior0.sum()

        # Create a DataFrame that will hold our posteriors for each day
        # Insert our prior as the first posterior.
        posteriors = pd.DataFrame(
            index=self._r_t_range,
            columns=sr.index,
            data={sr.index[0]: prior0}
        )

        # We said we'd keep track of the sum of the log of the probability
        # of the data for maximum likelihood calculation.
        log_likelihood = 0.0

        # (5) Iteratively apply Bayes' rule
        for previous_day, current_day in zip(sr.index[:-1], sr.index[1:]):
            # (5a) Calculate the new prior
            current_prior = process_matrix @ posteriors[previous_day]

            # (5b) Calculate the numerator of Bayes' Rule: P(k|R_t)P(R_t)
            numerator = likelihoods[current_day] * current_prior

            # (5c) Calcluate the denominator of Bayes' Rule P(k)
            denominator = np.sum(numerator)

            # Execute full Bayes' Rule
            posteriors[current_day] = numerator / denominator

            # Add to the running sum of log likelihoods
            log_likelihood += np.log(denominator)

        return posteriors, log_likelihood

    def highest_density_interval(self, pmf, p=.9):
        # If we pass a DataFrame, just call this recursively on the columns
        if isinstance(pmf, pd.DataFrame):
            return pd.DataFrame([self.highest_density_interval(pmf[col], p=p) for col in pmf],
                                index=pmf.columns)

        cumsum = np.cumsum(pmf.values)

        # N x N matrix of total probability mass for each low, high
        total_p = cumsum - cumsum[:, None]

        # Return all indices with total_p > p
        lows, highs = (total_p > p).nonzero()

        # Find the smallest range (highest density)
        best = (highs - lows).argmin()

        low = pmf.index[lows[best]]
        high = pmf.index[highs[best]]

        return pd.Series([low, high],
                         index=[f'Low_{p * 100:.0f}',
                                f'High_{p * 100:.0f}'])

    def plot_rt(self, result, ax, country, fig):
        ax.set_title(f"{country}")

        # Colors
        ABOVE = [1, 0, 0]
        MIDDLE = [1, 1, 1]
        BELOW = [0, 0, 0]
        cmap = ListedColormap(np.r_[
                                  np.linspace(BELOW, MIDDLE, 25),
                                  np.linspace(MIDDLE, ABOVE, 25)
                              ])
        color_mapped = lambda y: np.clip(y, .5, 1.5) - .5

        index = result['ML'].index
        values = result['ML'].values

        # Plot dots and line
        ax.plot(index, values, c='k', zorder=1, alpha=.25)
        ax.scatter(index,
                   values,
                   s=40,
                   lw=.5,
                   c=cmap(color_mapped(values)),
                   edgecolors='k', zorder=2)

        # Aesthetically, extrapolate credible interval by 1 day either side
        datetime_index = [pd.to_datetime(i + " 2020") for i in index]

        lowfn = interp1d(date2num(datetime_index),
                         result['Low_90'].values,
                         bounds_error=False,
                         fill_value='extrapolate')

        highfn = interp1d(date2num(datetime_index),
                          result['High_90'].values,
                          bounds_error=False,
                          fill_value='extrapolate')

        start_date = pd.to_datetime(index[1] + " 2020")
        end_date = pd.to_datetime(index[-1] + " 2020")
        extended = pd.date_range(start=datetime_index[0],
                                 end=datetime_index[-1] + pd.Timedelta(days=1))

        ax.fill_between([pd.to_datetime(e).strftime("%b %d") for e in extended],
                        lowfn(date2num(extended)),
                        highfn(date2num(extended)),
                        color='k',
                        alpha=.1,
                        lw=0,
                        zorder=3)

        ax.axhline(1.0, c='k', lw=1, label='$R_t=1.0$', alpha=.25)

        # Formatting
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.1f}"))
        ax.yaxis.tick_right()
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.margins(0)
        ax.grid(which='major', axis='y', c='k', alpha=.1, zorder=-2)
        ax.margins(0)
        ax.set_ylim(0.0, 5.0)
        ax.set_xlim(0, len(result.index))
        fig.set_facecolor('w')
        fig.autofmt_xdate(rotation=45)
