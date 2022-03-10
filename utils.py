import matplotlib.pyplot as plt


def plot_results(result_probs, vector_len):

    ticks = range(len(result_probs))
    plt.bar(ticks, height=result_probs)
    plt.xlabel("Subsets")
    plt.ylabel("Probabilities")

    # Format string for binary representation of the indexes
    f_index = "{:0" + str(vector_len) + "b}"
    labels = [f_index.format(i) for i in ticks]
    plt.xticks(ticks=ticks, labels=labels)

    plt.show()