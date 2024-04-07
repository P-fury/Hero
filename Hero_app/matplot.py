import matplotlib.pyplot as plt
import base64
from io import BytesIO


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot(lists):
    plt.switch_backend('agg')
    fig, ax1 = plt.subplots()
    ax1.plot(lists[0], lists[1], color='red', marker='.', ls=':')
    ax1.set_ylabel('mood', color='red')
    ax1.set_yticks([i for i in range(0, 6)])

    ax2 = ax1.twinx()
    ax2.plot(lists[0], lists[2])
    ax2.set_ylabel('amount of workouts', color='blue')
    ax2.set_yticks([i for i in range(0, 6)])

    plt.tight_layout()
    plt.gcf().set_size_inches(8, 3)
    graph = get_graph()
    return graph
