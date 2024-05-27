from lif_visualizer import LIF_Visualizer


def main() -> None:
    visualizer = LIF_Visualizer()
    visualizer.load_from_file("test.json")
    visualizer.visualize_layout("Layout_Ground_Level")


if __name__ == "__main__":
    main()
