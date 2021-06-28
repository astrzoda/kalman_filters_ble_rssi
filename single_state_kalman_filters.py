import pandas as pd
import matplotlib.pyplot as plt


class SingleStateKalmanFilter:
    def __init__(self, current_estimate, estimate_error, measurement_error):
        self.current_estimate = current_estimate
        self.estimate_error = estimate_error
        self.measurement_error = measurement_error

    @property
    def kalman_gain(self):
        return self.estimate_error / (self.estimate_error +
                                      self.measurement_error)

    @property
    def measurement(self):
        return self.measurement

    @measurement.setter
    def measurement(self, new_measurement):
        self.current_estimate = self.current_estimate + \
                                self.kalman_gain*(new_measurement - self.current_estimate)
        self.estimate_error = (1 - self.kalman_gain) * self.estimate_error


if __name__ == '__main__':
    df = pd.read_csv("measurements/concatenated_BLE_data.csv", sep=';')
    data = df[(df["advertiser"] == "huawei")]["Rssi"]

    kalman = SingleStateKalmanFilter(current_estimate=-127, estimate_error=6,
                                     measurement_error=10)
    estimated = []
    for rssi in data:
        kalman.measurement = rssi
        estimated.append(kalman.current_estimate)
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.scatter(data.index, data, marker='x', s=12, c='k')
    ax.scatter(data.index, estimated, s=1, c='red')
    plt.show()

