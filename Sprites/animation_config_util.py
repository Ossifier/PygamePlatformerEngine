import json


def create_file():
    config_file_name = input('Enter the name of your sprite_sheet: ') + '_config.json'
    print(f'File Name: {config_file_name}')
    with open(config_file_name, 'x') as n_file:
        json.dump({}, n_file)

    return config_file_name


def append_new_data(new_data, file_path):
    with open(file_path, 'r+') as file:
        file_data = json.load(file)
        file_data.update(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=2)


def build_config():
    json_data = {"animation states": {}}
    frame_num_list = []

    state_names = input('Please enter the list of state names separated by spaces: ').split()

    for index in range(len(state_names)):
        frame_num = int(input(f'# of frames in {state_names[index].upper()}: '))
        frame_num_list.append(frame_num)
        json_data["animation states"][state_names[index]] = {"framelist": []}

    print(f'\nSTATE LIST: {state_names}')
    print(f'NUMBER OF FRAMES: {frame_num_list}\n')

    # Build Configuration File #

    # Auto Configure Frames (For Sheets where Sprite Size is Static) #
    auto_configure = input('Automatically configure animations (All Sprites Same Size)? Y/N: ').upper()

    if auto_configure == 'Y':
        x_au, y_au = input(f'Sprite sheet start position (x, y): ').split()
        w_au, h_au = input(f'Sprite dimensions (w, h): ').split()
        x_au, y_au, w_au, h_au = int(x_au), int(y_au), int(w_au), int(h_au)

        for index in range(len(state_names)):

            for i in range(frame_num_list[index]):
                json_data["animation states"][state_names[index]]["framelist"].append(
                    {"frame": {"x": w_au * i, "y": h_au * index, "w": w_au, "h": h_au},
                     "rotated": False,                                                  # Currently Unused
                     "trimmed": False,                                                  # Currently Unused
                     "spriteSourceSize": {"x": 0, "y": 0, "w": 0, "h": 0},              # Currently Unused
                     "sourceSize": {"w": 0, "h": 0}}                                    # Currently Unused
                )

    else:
        manual_configure = input('Manually configure animations (Not All Sprites Same Size)? Y/N: ').upper()

    # Configure Each Frame Independently (For Sheets where Sprite Size is Dynamic) #
        if manual_configure == 'Y':
            for index in range(len(state_names)):

                for i in range(frame_num_list[index]):
                    x_fr, y_fr = input(f'{state_names[index].upper()} frame {i} sheet position (x, y): ').split()
                    w_fr, h_fr = input(f'{state_names[index].upper()} frame {i} dimensions: (w, h): ').split()
                    x_fr, y_fr, w_fr, h_fr = int(x_fr), int(y_fr), int(w_fr), int(h_fr)

                    json_data["animation states"][state_names[index]]["framelist"].append(
                        {"frame": {"x": x_fr, "y": y_fr, "w": w_fr, "h": h_fr},
                         "rotated": False,                                              # Currently Unused
                         "trimmed": False,                                              # Currently Unused
                         "spriteSourceSize": {"x": 0, "y": 0, "w": 0, "h": 0},          # Currently Unused
                         "sourceSize": {"w": 0, "h": 0}}                                # Currently Unused
                    )

    return json_data


if __name__ == '__main__':
    config_name = create_file()
    config_data = build_config()

    append_new_data(config_data, config_name)

    print('\nOperations Complete.')
