import numpy as np


class Plotter:
    @staticmethod
    def plot_results(results, figure):
        """
        Plot the performance results
        :param results: table of time dependence on the number of processes
        :param figure: window for rendering
        :return: None
        """
        figure.clear()
        ax = figure.add_subplot(111)

        processes = [r[0] for r in results]
        times = [r[1] for r in results]

        bars = ax.bar(processes, times, color="skyblue")
        ax.set_xlabel("Number of Processes")
        ax.set_ylabel("Time (seconds)")
        ax.set_title("Performance vs Number of Processes")
        ax.set_xticks(processes)

        min_idx = np.argmin(times)
        bars[min_idx].set_color("green")

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.2f}s",
                ha="center",
                va="bottom",
            )

        figure.tight_layout()
