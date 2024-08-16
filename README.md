# Blender Retopology Simple Tool

This tool is a Python script for Blender that facilitates automatic retopology of selected models or grids. It supports multiple algorithms, such as `Remesh` and `Decimate`, and offers various customization options.

## Features

- Choose between retopologizing an existing model or creating a new grid.
- Set a desired polygon count.
- Select the retopology algorithm (Remesh or Decimate).
- Options for Remesh detail, UV preservation, shading smoothness, and triangulation.
- Support for multiple iterations of retopology.

## Installation

1. Copy the [script](main.py) into Blender's text editor.
2. Run it to register the operators and panel in Blender's interface.
3. Open the "Tools"(press [N]) tab in the right sidebar of the 3D View to access the retopology tool.

## Usage

1. Select the object you wish to retopologize.
2. Ensure that the object is of type **Mesh**.
3. Customize the parameters in the "Tools" tab:
    - Choose the target type (Mesh or Grid).
    - Set the desired polygon count.
    - Select the retopology algorithm (Remesh or Decimate).
    - Adjust additional options as needed.
4. Click the `Confirm` button to execute the retopology process.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Notes

Please note that the UV preservation feature is not fully implemented and may require further development. Contributions and suggestions for improvements are welcome!

## Contribution

All contributions and code suggestions are encouraged! Please feel free to create a pull request or submit an issue if you have ideas for improvements.

---
