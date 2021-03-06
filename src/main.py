import argparse

import numpy as np
from scipy.spatial.transform import Rotation

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


def setup_figure():
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])

    axis_equal(ax)

    return fig, ax


def axis_equal(ax):
    """
    Emulate behavior for `axis("equal")`.

    Source: https://stackoverflow.com/questions/13685386/matplotlib-equal-unit-length-with-equal-aspect-ratio-z-axis-is-not-equal-to
    """
    ax.set_box_aspect([1, 1, 1])

    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])

    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))

    ax.set_xlim3d([origin[0] - radius, origin[0] + radius])
    ax.set_ylim3d([origin[1] - radius, origin[1] + radius])
    ax.set_zlim3d([origin[2] - radius, origin[2] + radius])


def plot_rotation_axes(ax, rot, **kwargs):
    """
    
    :param rot: Rotation as scipy.spatial.transform.Rotation object.
    """
    alpha = kwargs.get("alpha", 1)
    linewidth = kwargs.get("linewidth", 1.5)
    scale = kwargs.get("scale", 1)
    axis_colors = kwargs.get("axis_colors", ("r", "g", "b"))
    
    if type(axis_colors) == str or len(axis_colors) == 1:
        axis_colors = [axis_colors[0]] * 3

    R = rot.as_matrix()

    for i in range(0, 3):
        ax.plot(
            [0, R[0, i] * scale], 
            [0, R[1, i] * scale], 
            [0, R[2, i] * scale], 
            axis_colors[i] + "-", 
            linewidth=linewidth, 
            alpha=alpha
        )


def make_argparser():
    parser = argparse.ArgumentParser(description="Visualize Euler (Tait-Bryan) angles.")
    parser.add_argument("order", type=str, help="The intrinsic or extrinsic order of the angles.")
    parser.add_argument("first", type=float, help="The first angle.")
    parser.add_argument("second", type=float, help="The second angle.")
    parser.add_argument("third", type=float, help="The third angle.")
    parser.add_argument("--radians", action="store_true", help="Set this flag if the input is given in radians.")

    return parser


def main():
    parser = make_argparser()
    args = parser.parse_args()

    fig, ax = setup_figure()

    origin = Rotation.from_quat([0, 0, 0, 1])
    plot_rotation_axes(ax, origin, alpha=0.5)

    # R_OA = Rotation.from_euler(args.order, [args.first, args.second, args.third], degrees=not args.radians)
    # plot_rotation_axes(ax, R_OA, linewidth=2)

    gtsam = Rotation.from_matrix([
        [0.171129, -0.321865,  0.931191],
        [-0.985021, -0.076226,  0.154674],
        [0.0211967, -0.943712, -0.330089]
    ])
    ceres = Rotation.from_matrix([
        [0.0441444,   0.307032,  -0.950675],
        [0.997836, -0.0599644,  0.0269681],
        [-0.0487266,  -0.949808,  -0.309014]
    ])

    plot_rotation_axes(ax, gtsam, axis_colors=["r", "g", "b"], linewidth=2)
    plot_rotation_axes(ax, ceres, axis_colors=["y", "m", "c"], linewidth=2)

    plt.show()


if __name__ == "__main__":
    main()

