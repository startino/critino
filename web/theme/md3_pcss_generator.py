# Helper function to convert hex color to RGB format
import re
import argparse
import json


# Helper function to convert hex color to RGB format
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 6:
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    elif len(hex_color) == 3:
        return tuple(int(hex_color[i] * 2, 16) for i in range(3))
    else:
        raise ValueError(f"Invalid hex color: {hex_color}")


# Function to convert camelCase to kebab-case, special handling for "on" fields
def camel_to_kebab_case(name):
    # If the key starts with 'on', process differently
    if name.startswith("on"):
        # Example: onPrimary becomes primary-on
        base_name = name[2:]  # Strip "on" from the start
        s1 = re.sub(
            "([a-z])([A-Z])", r"\1-\2", base_name
        )  # Insert dash between camel case words
        return s1.lower() + "-on"
    else:
        # Normal camelCase to kebab-case conversion
        s1 = re.sub(
            "([a-z])([A-Z])", r"\1-\2", name
        )  # Insert dash between camel case words
        return s1.lower().replace(
            "_", "-"
        )  # Lower all and convert underscores to dashes


# Function to convert the TypeScript object to PostCSS format
def convert_to_postcss(ts_data):
    light_colors = ts_data["schemes"]["light"]
    dark_colors = ts_data["schemes"]["dark"]

    # List of color keys to process
    color_keys = [
        "primary",
        "onPrimary",
        "primaryContainer",
        "onPrimaryContainer",
        "secondary",
        "onSecondary",
        "secondaryContainer",
        "onSecondaryContainer",
        "tertiary",
        "onTertiary",
        "tertiaryContainer",
        "onTertiaryContainer",
        "surface",
        "onSurface",
        "surfaceVariant",
        "onSurfaceVariant",
        "background",
        "onBackground",
        "outline",
        "outlineVariant",
        "error",
        "onError",
        "errorContainer",
        "onErrorContainer",
        "success",
        "onSuccess",
        "successContainer",
        "onSuccessContainer",
    ]

    # For light theme
    light_color_mapping = {}
    for key in color_keys:
        if key in light_colors:
            light_color_mapping[key] = light_colors[key]

    # For dark theme
    dark_color_mapping = {}
    for key in color_keys:
        if key in dark_colors:
            dark_color_mapping[key] = dark_colors[key]

    # Start building the PostCSS output
    postcss_lines = []
    postcss_lines.append("@tailwind base;")
    postcss_lines.append("@tailwind components;")
    postcss_lines.append("@tailwind utilities;")
    postcss_lines.append("")
    postcss_lines.append("@layer base {")
    postcss_lines.append("\t* {")
    postcss_lines.append("\t\tmin-width: 0;")
    postcss_lines.append("\t\t@apply border-border;")
    postcss_lines.append("\t}")
    postcss_lines.append("\tbody {")
    postcss_lines.append("\t\t@apply bg-background text-foreground;")
    postcss_lines.append("\t\tfont-feature-settings: 'rlig' 1, 'calt' 1;")
    postcss_lines.append("\t}")
    postcss_lines.append("}")
    postcss_lines.append("")
    postcss_lines.append("@layer base {")
    postcss_lines.append("\t:root {")

    # Define variables from light theme
    for key, hex_value in light_color_mapping.items():
        rgb_value = hex_to_rgb(hex_value)
        var_name = f"--color-{camel_to_kebab_case(key)}"
        postcss_lines.append(
            f"\t\t{var_name}: {rgb_value[0]}, {rgb_value[1]}, {rgb_value[2]};"
        )

    postcss_lines.append("\t}")
    postcss_lines.append("")
    postcss_lines.append("\t.dark {")
    # Define variables from dark theme
    for key, hex_value in dark_color_mapping.items():
        rgb_value = hex_to_rgb(hex_value)
        var_name = f"--color-{camel_to_kebab_case(key)}"
        postcss_lines.append(
            f"\t\t{var_name}: {rgb_value[0]}, {rgb_value[1]}, {rgb_value[2]};"
        )
    postcss_lines.append("\t}")
    postcss_lines.append("}")

    return "\n".join(postcss_lines)


# Main function to read input and generate output
def main():
    parser = argparse.ArgumentParser(
        description="Convert TypeScript-style object to Tailwind CSS/PostCSS."
    )
    parser.add_argument(
        "ts_data",
        type=str,
        help="JSON string or path to the JSON file containing the TypeScript object data.",
    )

    args = parser.parse_args()

    # Check if ts_data is a JSON file path or JSON string
    try:
        with open(args.ts_data, "r") as f:
            md3_ts_data = json.load(f)
    except FileNotFoundError:
        # If it's not a file, treat it as a JSON string
        md3_ts_data = json.loads(args.ts_data)

    # Convert TypeScript data to PostCSS
    postcss_output = convert_to_postcss(md3_ts_data)

    # Print the output
    print(postcss_output)


if __name__ == "__main__":
    main()
