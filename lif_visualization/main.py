from lif_visualizer import LIF_Visualizer


def main() -> None:
    visualizer = LIF_Visualizer()
    visualizer.load_from_file("test.json")
    selected_layout_id = visualizer.layout_selection()
    visualizer.visualize_layout(selected_layout_id)


if __name__ == "__main__":
    main()
