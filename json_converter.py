import json
import numpy as np


class JsonData:

    def __init__(self, file_path):
        self.file_path = file_path
        with open(self.file_path) as json_file:
            data = json.load(json_file)
            cost_map = np.array(data['cost'])
            mesh_grid = np.array([data['mesh_grid'][0], data['mesh_grid'][1]])
            path = []
            for i in range(0, len(data['t'])):
                point = [data['path']['waypoints'][i][0], data['path']['waypoints'][i][1],
                         data['t'][i], data['path']['heading'][i], data['path']['throttle'][i]]
                path.append(point)

            self.cost_map = cost_map
            self.mesh_grid = mesh_grid
            self.data = data
            self.path = path
            self.time = [t for (x, y, t, psi, throttle) in path]
            self.waypoints = [[x, y] for (x, y, t, psi, throttle) in path]
            self.heading = [psi for (x, y, t, psi, throttle) in path]
            self.throttle = [throttle for (x, y, t, psi, throttle) in path]
            self.t_step = data['t'][1] - data['t'][0]

    def get_path_information(self):
        return self.waypoints, self.heading, self.throttle, self.t_step, self.path


def main():
    pass


if __name__ == '__main__':
    main()
