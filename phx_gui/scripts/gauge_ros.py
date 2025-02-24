#!/usr/bin/env python
__author__ = 'manuelviermetz'

from PyQt4 import uic, QtCore, QtGui
import pyqtgraph
import time
import numpy as np
from goompy import GooMPy

# import ROS
import rospy
from phx_arduino_uart_bridge.msg import Servo
from phx_arduino_uart_bridge.msg import LED
from phx_arduino_uart_bridge.msg import LEDstrip
from phx_arduino_uart_bridge.msg import Altitude
from phx_arduino_uart_bridge.msg import PID
from phx_arduino_uart_bridge.msg import PID_cleanflight
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Joy
from sensor_msgs.msg import Image

# generate .py from .ui via pyuic4 gui_v0.ui -o gui_v0.py
from gui_v1 import Ui_MainWindow


class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtGui.QMainWindow.__init__(self, *args, **kwargs)
        self.keysPressed = []
        self.keyHits = []
        self.mouseClicks = []

    def mousePressEvent(self, ev):
        # print ev.button()
        # print self.view.ItemTransformOriginPointChange
        # print ev.x(), ev.y(), ev.pos()
        ev.accept()
        self.mouseClicks.append([ev.x(), ev.y(), ev.pos(), ev.button()])

    def keyPressEvent(self, ev):
        print ev.key(), QtCore.Qt.Key_Up
        ev.accept()
        if ev.key() not in self.keyHits:
            self.keyHits.append(ev.key())
        if ev.isAutoRepeat():
            return
        self.keysPressed.append(ev.key())

    def keyReleaseEvent(self, ev):
        # ev.accept()
        if ev.isAutoRepeat():
            return
        if ev.key() in self.keysPressed:
            self.keysPressed.remove(ev.key())
        else:
            print "key hit of", ev.key(), "not detected"

app = QtGui.QApplication([])
#win = PyQt4.uic.loadUi('gui_v0.ui')
##win = QtGui.QMainWindow()
win = MainWindow()
ui_win = Ui_MainWindow()
ui_win.setupUi(win)


win.setWindowTitle('gauge GUI - made for ROS')
ui_win.statusbar.showMessage("starting up...")

##########################################################################################
# init tabs left
##########################################################################################
# text output # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
ui_win.textBrowser.setText('test text')

# gps tab # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
gps_data = [[], []]  # [[lon], [lat]]
gps_geo_cycle_data = None
gps_positions = {}
gps_altitudes = {}

ui_win.graphicsView_gps.plotItem.showGrid(x=True, y=True, alpha=0.2)
gps_qtgraph_plot = ui_win.graphicsView_gps.plotItem.plot()
gps_geo_cycle_qtgraph_plot = ui_win.graphicsView_gps.plotItem.plot()
gps_geo_cycle_qtgraph_plot.setPen(pyqtgraph.mkPen(color=(0, 0, 200)))
# gps_qtgraph_plot.setData([1, 2, 3], [1, 3, 1])

gps_scatter_plot = pyqtgraph.ScatterPlotItem()
gps_scatter_plot.setData(gps_positions.values())
# gps_scatter_plot.setData([{'pos': (11, 42), 'symbol': 'o'}, ...])
ui_win.graphicsView_gps.addItem(gps_scatter_plot)

gps_background_image = pyqtgraph.ImageItem()
ui_win.graphicsView_gps.addItem(gps_background_image)
gps_background_image.setZValue(-1)

update_background_map = False

# background image
def gps_update_map(x, y, image_plot):
    gps_map_coordinate = [x, y]
    gps_map_zoom = 19
    gps_map_type = 'satellite'
    gps_map_resolution = 1200
    gps_map = GooMPy(gps_map_resolution, gps_map_resolution, gps_map_coordinate[0], gps_map_coordinate[1], gps_map_zoom, gps_map_type)
    gps_map_tile = gps_map.bigimage
    gps_map_corner_upper_left = gps_map.northwest
    gps_map_corner_lower_right = gps_map.southeast
    gps_map_width = (gps_map_corner_lower_right[1] - gps_map_corner_upper_left[1]) * 4 / 3
    gps_map_height = (gps_map_corner_upper_left[0] - gps_map_corner_lower_right[0]) * 4 / 3
    gps_map_aspect_ratio = gps_map_width / gps_map_height
    gps_map_array = np.array(gps_map_tile.resize((int(gps_map_resolution * gps_map_aspect_ratio), gps_map_resolution)))
    gps_map_array = np.swapaxes(gps_map_array[::-1, :], 0, 1)
    gps_map_effective_size = gps_map_height / gps_map_resolution
    image_plot.setScale(gps_map_effective_size)
    image_plot.setImage(gps_map_array)
    image_plot.setX(gps_map_corner_upper_left[1] - gps_map_width / 8)
    image_plot.setY(gps_map_corner_upper_left[0] - gps_map_height + gps_map_height / 8)
    image_plot.update()

#gps_update_map(48.2660393944, 11.6712039642, gps_background_image)
#gps_update_map(48.2659424, 11.6711544, gps_background_image)

def calc_geo_distance(lon0, lat0, lon1, lat1):
    earth_radius = 6371000                          # metre
    lat_0 = 2. * np.pi * (lat0 / 360.)              # rad
    lat_1 = 2. * np.pi * (lat1 / 360.)              # rad
    d_phi = 2. * np.pi * ((lat1 - lat0) / 360.)     # rad
    d_lamda = 2. * np.pi * ((lon1 - lon0) / 360.)   # rad
    a = np.sin(d_phi/2) * np.sin(d_phi / 2) + np.cos(lat_0) * np.cos(lat_1) *  np.sin(d_lamda / 2) * np.sin(d_lamda / 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    d = earth_radius * c                            # meter
    return d


def generate_geo_circle(est_lon, est_lat, diameter):
    approximate_scale_lon_to_meter = calc_geo_distance(est_lon, est_lat, est_lon + 0.00001, est_lat) / 0.00001
    approximate_scale_lat_to_meter = calc_geo_distance(est_lon, est_lat, est_lon, est_lat + 0.00001) / 0.00001
    diameter_x = diameter / approximate_scale_lon_to_meter
    diameter_y = diameter / approximate_scale_lat_to_meter
    t = np.linspace(0, 2 * np.pi, 20)
    x = np.sin(t) * 0.5 * diameter_x
    y = np.cos(t) * 0.5 * diameter_y
    return [x, y]

# label = pyqtgraph.TextItem(text='test')
# ui_win.graphicsView_gps.addItem(label)
# label.setPos(11, 42)
# ui_win.graphicsView_gps.removeItem(label)
gps_position_labels = {}


def update_gps_plot(path=True, points=True):
    if path:
        # update gps path
        gps_qtgraph_plot.setData(gps_data[0], gps_data[1])
    if gps_geo_cycle_data:
        if 'phoenix' in gps_positions.keys():
            cur_pos_lon = gps_positions['phoenix']['pos'][0]
            cur_pos_lat = gps_positions['phoenix']['pos'][1]
            gps_geo_cycle_qtgraph_plot.setData(gps_geo_cycle_data[0] + cur_pos_lon, gps_geo_cycle_data[1] + cur_pos_lat)
    if points:
        # update gps points
        gps_scatter_plot.setData(gps_positions.values())
        # add labels and update position
        for label in gps_positions.keys():
            if label not in gps_position_labels.keys():
                if label == 'home':
                    color = (255, 255, 0)
                elif label == 'phoenix':
                    color = (0, 0, 255)
                elif label == 'way_point':
                    color = (0, 255, 0)
                else:
                    color = (200, 255, 200)
                text_item = pyqtgraph.TextItem(text=label, color=color)
                ui_win.graphicsView_gps.addItem(text_item)
                gps_position_labels[label] = text_item
            gps_position_labels[label].setPos(gps_positions[label]['pos'][0], gps_positions[label]['pos'][1])
            text_output = str('lon: %02.6f'% gps_positions[label]['pos'][0])
            text_output += str('\nlat: %02.6f'% gps_positions[label]['pos'][1])
            text_output += str('\nalt: %02.6f'% gps_altitudes[label])
            if label == 'home':
                ui_win.gps_position_home_TextBrowser.setText(text_output)
            elif label == 'way_point':
                ui_win.gps_position_way_point_TextBrowser.setText(text_output)
            elif label == 'phoenix':
                ui_win.gps_position_current_TextBrowser.setText(text_output)
        # remove unused labels
        for label in gps_position_labels.keys():
            if label not in gps_positions.keys():
                text_item = gps_position_labels[label]
                ui_win.graphicsView_gps.removeItem(text_item)
                del gps_position_labels[label]


def gps_plot_mouse_clicked(event):
    if ui_win.graphicsView_gps.plotItem.sceneBoundingRect().contains(event.scenePos()):
        mousePoint = ui_win.graphicsView_gps.plotItem.mapToView(event.scenePos())
        button = event.button()         # 1: left   2:right
        x_val = mousePoint.x()
        y_val = mousePoint.y()
        print 'gps_plot_mouse_clicked', x_val, y_val, button
        way_point_msg = NavSatFix()
        way_point_msg.longitude = x_val
        way_point_msg.latitude = y_val
        way_point_msg.altitude = 0              # need to fix this!
        ros_publisher_gps_way_point.publish(way_point_msg)
ui_win.graphicsView_gps.plotItem.scene().sigMouseClicked.connect(gps_plot_mouse_clicked)
# another way of connecting the mouse events in case rateLimit is needed. Take care event will be a list of events
#proxy = pyqtgraph.SignalProxy(ui_win.graphicsView_gps.plotItem.scene().sigMouseClicked, rateLimit=60, slot=gps_plot_mouse_clicked)


def gps_plot_mouse_moved(event):
    if ui_win.graphicsView_gps.plotItem.sceneBoundingRect().contains(event):
        mousePoint = ui_win.graphicsView_gps.plotItem.mapToView(event)
        x_val = mousePoint.x()
        y_val = mousePoint.y()
        #print 'gps_plot_mouse_moved', x_val, y_val
        ui_win.statusbar.showMessage('gps plot mouse lon: ' + str(x_val) + '  \t lat: ' + str(y_val))
ui_win.graphicsView_gps.plotItem.scene().sigMouseMoved.connect(gps_plot_mouse_moved)

# led tab # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def generate_led_strip_msg(color_r, color_g, color_b):
    LEDstrip_msg = LEDstrip()
    color_r = int(color_r.value())
    color_g = int(color_g.value())
    color_b = int(color_b.value())
    LEDstrip_msg.led_0_r = color_r; LEDstrip_msg.led_0_g = color_g; LEDstrip_msg.led_0_b = color_b
    LEDstrip_msg.led_1_r = color_r; LEDstrip_msg.led_1_g = color_g; LEDstrip_msg.led_1_b = color_b
    LEDstrip_msg.led_2_r = color_r; LEDstrip_msg.led_2_g = color_g; LEDstrip_msg.led_2_b = color_b
    LEDstrip_msg.led_3_r = color_r; LEDstrip_msg.led_3_g = color_g; LEDstrip_msg.led_3_b = color_b
    LEDstrip_msg.led_4_r = color_r; LEDstrip_msg.led_4_g = color_g; LEDstrip_msg.led_4_b = color_b
    LEDstrip_msg.led_5_r = color_r; LEDstrip_msg.led_5_g = color_g; LEDstrip_msg.led_5_b = color_b
    LEDstrip_msg.led_6_r = color_r; LEDstrip_msg.led_6_g = color_g; LEDstrip_msg.led_6_b = color_b
    LEDstrip_msg.led_7_r = color_r; LEDstrip_msg.led_7_g = color_g; LEDstrip_msg.led_7_b = color_b
    LEDstrip_msg.led_8_r = color_r; LEDstrip_msg.led_8_g = color_g; LEDstrip_msg.led_8_b = color_b
    LEDstrip_msg.led_9_r = color_r; LEDstrip_msg.led_9_g = color_g; LEDstrip_msg.led_9_b = color_b
    return LEDstrip_msg




##########################################################################################
# init right side
##########################################################################################
# parameters # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def set_parameters_lcd(number, val=0):
    if number == 0:
        ui_win.lcdNumber_parameter_00.display(val)
    elif number == 1:
        ui_win.lcdNumber_parameter_01.display(val)
    elif number == 2:
        ui_win.lcdNumber_parameter_02.display(val)
    elif number == 3:
        ui_win.lcdNumber_parameter_03.display(val)
    elif number == 4:
        ui_win.lcdNumber_parameter_04.display(val)
    elif number == 5:
        ui_win.lcdNumber_parameter_05.display(val)
    elif number == 6:
        ui_win.lcdNumber_parameter_06.display(val)
    elif number == 7:
        ui_win.lcdNumber_parameter_07.display(val)
    elif number == 8:
        ui_win.lcdNumber_parameter_08.display(val)
    elif number == 9:
        ui_win.lcdNumber_parameter_09.display(val)
    elif number == 10:
        ui_win.lcdNumber_parameter_10.display(val)
    elif number == 11:
        ui_win.lcdNumber_parameter_11.display(val)
    elif number == 12:
        ui_win.lcdNumber_parameter_12.display(val)
    elif number == 13:
        ui_win.lcdNumber_parameter_13.display(val)
    elif number == 14:
        ui_win.lcdNumber_parameter_14.display(val)
    elif number == 15:
        ui_win.lcdNumber_parameter_15.display(val)
    elif number == 16:
        ui_win.lcdNumber_parameter_16.display(val)
    elif number == 17:
        ui_win.lcdNumber_parameter_17.display(val)
    else:
        print ' -> set_parameters_lcd requested number', number, 'not available'


def set_parameters_slider_limits(number, min=10, max=2000):
    if number == 0:
        ui_win.horizontalSlider_parameter_00.setRange(min, max)
    elif number == 1:
        ui_win.horizontalSlider_parameter_01.setRange(min, max)
    elif number == 2:
        ui_win.horizontalSlider_parameter_02.setRange(min, max)
    elif number == 3:
        ui_win.horizontalSlider_parameter_03.setRange(min, max)
    elif number == 4:
        ui_win.horizontalSlider_parameter_04.setRange(min, max)
    elif number == 5:
        ui_win.horizontalSlider_parameter_05.setRange(min, max)
    elif number == 6:
        ui_win.horizontalSlider_parameter_06.setRange(min, max)
    elif number == 7:
        ui_win.horizontalSlider_parameter_07.setRange(min, max)
    elif number == 8:
        ui_win.horizontalSlider_parameter_08.setRange(min, max)
    elif number == 9:
        ui_win.horizontalSlider_parameter_09.setRange(min, max)
    elif number == 10:
        ui_win.horizontalSlider_parameter_10.setRange(min, max)
    elif number == 11:
        ui_win.horizontalSlider_parameter_11.setRange(min, max)
    elif number == 12:
        ui_win.horizontalSlider_parameter_12.setRange(min, max)
    elif number == 13:
        ui_win.horizontalSlider_parameter_13.setRange(min, max)
    elif number == 14:
        ui_win.horizontalSlider_parameter_14.setRange(min, max)
    elif number == 15:
        ui_win.horizontalSlider_parameter_15.setRange(min, max)
    elif number == 16:
        ui_win.horizontalSlider_parameter_16.setRange(min, max)
    elif number == 17:
        ui_win.horizontalSlider_parameter_17.setRange(min, max)
    else:
        print ' -> set_parameters_slider_limits requested number', number, 'not available'


def set_parameters_slider(number, val, lcd_linked=True):
    if number == 0:
        ui_win.horizontalSlider_parameter_00.setValue(val)
    elif number == 1:
        ui_win.horizontalSlider_parameter_01.setValue(val)
    elif number == 2:
        ui_win.horizontalSlider_parameter_02.setValue(val)
    elif number == 3:
        ui_win.horizontalSlider_parameter_03.setValue(val)
    elif number == 4:
        ui_win.horizontalSlider_parameter_04.setValue(val)
    elif number == 5:
        ui_win.horizontalSlider_parameter_05.setValue(val)
    elif number == 6:
        ui_win.horizontalSlider_parameter_06.setValue(val)
    elif number == 7:
        ui_win.horizontalSlider_parameter_07.setValue(val)
    elif number == 8:
        ui_win.horizontalSlider_parameter_08.setValue(val)
    elif number == 9:
        ui_win.horizontalSlider_parameter_09.setValue(val)
    elif number == 10:
        ui_win.horizontalSlider_parameter_10.setValue(val)
    elif number == 11:
        ui_win.horizontalSlider_parameter_11.setValue(val)
    elif number == 12:
        ui_win.horizontalSlider_parameter_12.setValue(val)
    elif number == 13:
        ui_win.horizontalSlider_parameter_13.setValue(val)
    elif number == 14:
        ui_win.horizontalSlider_parameter_14.setValue(val)
    elif number == 15:
        ui_win.horizontalSlider_parameter_15.setValue(val)
    elif number == 16:
        ui_win.horizontalSlider_parameter_16.setValue(val)
    elif number == 17:
        ui_win.horizontalSlider_parameter_17.setValue(val)
    else:
        print ' -> set_parameters_slider requested number', number, 'not available'
    if lcd_linked:
        set_parameters_lcd(number, val)


def get_parameters_slider(number):
    if number == 0:
        return ui_win.horizontalSlider_parameter_00.value()
    elif number == 1:
        return ui_win.horizontalSlider_parameter_01.value()
    elif number == 2:
        return ui_win.horizontalSlider_parameter_02.value()
    elif number == 3:
        return ui_win.horizontalSlider_parameter_03.value()
    elif number == 4:
        return ui_win.horizontalSlider_parameter_04.value()
    elif number == 5:
        return ui_win.horizontalSlider_parameter_05.value()
    elif number == 6:
        return ui_win.horizontalSlider_parameter_06.value()
    elif number == 7:
        return ui_win.horizontalSlider_parameter_07.value()
    elif number == 8:
        return ui_win.horizontalSlider_parameter_08.value()
    elif number == 9:
        return ui_win.horizontalSlider_parameter_09.value()
    elif number == 10:
        return ui_win.horizontalSlider_parameter_10.value()
    elif number == 11:
        return ui_win.horizontalSlider_parameter_11.value()
    elif number == 12:
        return ui_win.horizontalSlider_parameter_12.value()
    elif number == 13:
        return ui_win.horizontalSlider_parameter_13.value()
    elif number == 14:
        return ui_win.horizontalSlider_parameter_14.value()
    elif number == 15:
        return ui_win.horizontalSlider_parameter_15.value()
    elif number == 16:
        return ui_win.horizontalSlider_parameter_16.value()
    elif number == 17:
        return ui_win.horizontalSlider_parameter_17.value()
    else:
        print ' -> get_parameters_slider requested number', number, 'not available'
        return False

for i in range(0, 18):
    set_parameters_slider_limits(i, 300, 2450)


# flight controller rc # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
record_fc_rc = 600
fc_rc = np.zeros((record_fc_rc, 8), dtype=np.uint16) + 1000

rc_fc_qtgraph_plot_pitch = ui_win.graphicsView_rc_fc.plotItem.plot()
rc_fc_qtgraph_plot_pitch.setPen(pyqtgraph.mkPen(color=(200, 0, 100)))
rc_fc_qtgraph_plot_roll = ui_win.graphicsView_rc_fc.plotItem.plot()
rc_fc_qtgraph_plot_roll.setPen(pyqtgraph.mkPen(color=(255, 0, 0)))
rc_fc_qtgraph_plot_yaw = ui_win.graphicsView_rc_fc.plotItem.plot()
rc_fc_qtgraph_plot_yaw.setPen(pyqtgraph.mkPen(color=(0, 0, 200)))
rc_fc_qtgraph_plot_throttle = ui_win.graphicsView_rc_fc.plotItem.plot()
rc_fc_qtgraph_plot_throttle.setPen(pyqtgraph.mkPen(color=(0, 200, 0)))


def update_fc_remote_control():
    global fc_rc
    ui_win.remote_slider_rc_fc_pitch.setValue(fc_rc[-1, 0])
    ui_win.remote_slider_rc_fc_roll.setValue(fc_rc[-1, 1])
    ui_win.remote_slider_rc_fc_yaw.setValue(fc_rc[-1, 2])
    ui_win.remote_slider_rc_fc_throttle.setValue(fc_rc[-1, 3])
    ui_win.remote_slider_rc_fc_aux1.setValue(fc_rc[-1, 4])
    ui_win.remote_slider_rc_fc_aux2.setValue(fc_rc[-1, 5])
    ui_win.remote_slider_rc_fc_aux3.setValue(fc_rc[-1, 6])
    ui_win.remote_slider_rc_fc_aux4.setValue(fc_rc[-1, 7])

    rc_fc_qtgraph_plot_pitch.setData(np.arange(0, fc_rc.shape[0]), fc_rc[:, 0])
    rc_fc_qtgraph_plot_roll.setData(np.arange(0, fc_rc.shape[0]), fc_rc[:, 1])
    rc_fc_qtgraph_plot_yaw.setData(np.arange(0, fc_rc.shape[0]), fc_rc[:, 2])
    rc_fc_qtgraph_plot_throttle.setData(np.arange(0, fc_rc.shape[0]), fc_rc[:, 3])


# altitude # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
record_altitude = 5000
altitude_dataset_index = {'fc_barometer': 0, 'fc_gps': 1, 'marvic_ir': 2, 'marvic_lidar': 3, 'marvic_baro': 4, 'marvic_sonar': 5, 'marvic_fused': 6}
altitude_dataset = np.zeros((record_altitude, len(altitude_dataset_index), 2)) #, dtype=np.uint16)
altitude_qtgraph_plot_fc_barometer = ui_win.graphicsView_altitude.plotItem.plot()
altitude_qtgraph_plot_fc_barometer.setPen(pyqtgraph.mkPen(color=(200, 0, 200)))
altitude_qtgraph_plot_fc_gps = ui_win.graphicsView_altitude.plotItem.plot()
altitude_qtgraph_plot_fc_gps.setPen(pyqtgraph.mkPen(color=(200, 0, 0)))
altitude_qtgraph_plot_marvic_lidar = ui_win.graphicsView_altitude.plotItem.plot()
altitude_qtgraph_plot_marvic_lidar.setPen(pyqtgraph.mkPen(color=(0, 0, 200)))
altitude_qtgraph_plot_marvic_infra_red = ui_win.graphicsView_altitude.plotItem.plot()
altitude_qtgraph_plot_marvic_infra_red.setPen(pyqtgraph.mkPen(color=(0, 200, 0)))
altitude_qtgraph_plot_marvic_fused = ui_win.graphicsView_altitude.plotItem.plot()
altitude_qtgraph_plot_marvic_fused.setPen(pyqtgraph.mkPen(color=(100, 100, 100)))
# naze baro - lila
# naze gps - red
# lidar - blue
# ir - green
# fused - grey


def update_altitude_plot():
    cur_time = altitude_dataset[:, :, 1].max()
    altitude_qtgraph_plot_fc_barometer.setData(altitude_dataset[:, altitude_dataset_index['fc_barometer'], 1]-cur_time, altitude_dataset[:, altitude_dataset_index['fc_barometer'], 0])
    altitude_qtgraph_plot_fc_gps.setData(altitude_dataset[:, altitude_dataset_index['fc_gps'], 1]-cur_time, altitude_dataset[:, altitude_dataset_index['fc_gps'], 0])
    altitude_qtgraph_plot_marvic_infra_red.setData(altitude_dataset[:, altitude_dataset_index['marvic_ir'], 1]-cur_time, altitude_dataset[:, altitude_dataset_index['marvic_ir'], 0])
    altitude_qtgraph_plot_marvic_lidar.setData(altitude_dataset[:, altitude_dataset_index['marvic_lidar'], 1]-cur_time, altitude_dataset[:, altitude_dataset_index['marvic_lidar'], 0])
    altitude_qtgraph_plot_marvic_fused.setData(altitude_dataset[:, altitude_dataset_index['marvic_fused'], 1]-cur_time, altitude_dataset[:, altitude_dataset_index['marvic_fused'], 0])

# video # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
live_image = np.zeros((480, 640), dtype=np.uint8)
time_of_last_image = 0
video_fps = 0
image_mask = np.zeros((480, 640), dtype=np.uint8)
video_qtgraph_plot = pyqtgraph.ImageView(ui_win.graphicsView_video)
video_auto_range = False
video_auto_level = False
video_auto_histogram_range = False
video_qtgraph_plot.setFixedWidth(611)
video_qtgraph_plot.setFixedHeight(421)
video_qtgraph_plot.setImage(np.swapaxes(live_image, 0, 1), levels=(0, 255), autoHistogramRange=False)

def update_video_mask():
    global image_mask, video_qtgraph_plot
    while len(video_qtgraph_plot.mouse_clicks) > 0:
        click = video_qtgraph_plot.mouse_clicks.pop()
        x0, x1, button = click[1], click[2], click[4]
        if button == 1:
            borders = video_qtgraph_plot.imageItem.sceneBoundingRect()
            if x0 < borders.left() or x0 > borders.right() or x1 < borders.top() or x1 > borders.bottom():
                # click outside the image
                print 'new click outside'
                break
            img_x0 = (x0 - borders.left()) / borders.width()
            img_x1 = (x1 - borders.top()) / borders.height()
            y = int(img_x0 * image_mask.shape[1])
            x = int(img_x1 * image_mask.shape[0])

            print 'new click inside', x, y, button
            image_mask *= 0
            for dx in range(-10, 12):
                image_mask[x + dx, y] = 100
                image_mask[x + dx, y + 1] = 100
            for dy in range(-10, 12):
                image_mask[x, y + dy] = 100
                image_mask[x + 1, y + dy] = 100


def update_video():
    #live_image[0, 0] = 0
    #live_image[-1, -1] = 255
    if ui_win.checkBox_video_active.isChecked():
        if ui_win.checkBox_video_reset_ranges.isChecked():
            video_qtgraph_plot.setImage(np.swapaxes(live_image + image_mask, 0, 1), levels=(0, 255), autoHistogramRange=False)
        else:
            video_qtgraph_plot.setImage(np.swapaxes(live_image + image_mask, 0, 1), autoLevels=video_auto_range, autoRange=video_auto_range, autoHistogramRange=video_auto_histogram_range)
        video_qtgraph_plot.update()

        ui_win.statusbar.showMessage(str("video playing with: " + str(video_fps) + " FPS"))


# pid # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
pid_config_storage_comments_file = 'pid_config_storage_comments.txt'
pid_config_storage_comments = np.loadtxt(pid_config_storage_comments_file, dtype=np.str)
pid_config_storage_file = 'pid_config_storage.txt'
pid_config_storage = np.loadtxt(pid_config_storage_file, dtype=np.uint8)


def pid_config_save(comments, values, comment_file, value_file):
    f = open(comment_file, 'w')
    for line in comments:
        f.write(str(line))
        f.write('\n')
    f.close()
    f = open(value_file, 'w')
    for line in values:
        for integer in line:
            f.write(str(integer))
            f.write('\t')
        f.write('\n')
    f.close()
    print 'pid_config_save done'


def pid_config_storage_comment_update(index):
    ui_win.pid_lineEdit_config_storage.setText(pid_config_storage_comments[index])
    print pid_config_storage_comments[index]


def pid_config_storage_comment_save():
    index = ui_win.spinBox_pid_config_storage.value()
    pid_config_storage[index, 0] = ui_win.pid_spinBox_roll_p.value()
    pid_config_storage[index, 1] = ui_win.pid_spinBox_roll_i.value()
    pid_config_storage[index, 2] = ui_win.pid_spinBox_roll_d.value()
    pid_config_storage[index, 3] = ui_win.pid_spinBox_pitch_p.value()
    pid_config_storage[index, 4] = ui_win.pid_spinBox_pitch_i.value()
    pid_config_storage[index, 5] = ui_win.pid_spinBox_pitch_d.value()
    pid_config_storage[index, 6] = ui_win.pid_spinBox_yaw_p.value()
    pid_config_storage[index, 7] = ui_win.pid_spinBox_yaw_i.value()
    pid_config_storage[index, 8] = ui_win.pid_spinBox_yaw_d.value()
    pid_config_storage[index, 9] = ui_win.pid_spinBox_alt_p.value()
    pid_config_storage[index, 10] = ui_win.pid_spinBox_alt_i.value()
    pid_config_storage[index, 11] = ui_win.pid_spinBox_alt_d.value()
    pid_config_storage[index, 12] = ui_win.pid_spinBox_vel_p.value()
    pid_config_storage[index, 13] = ui_win.pid_spinBox_vel_i.value()
    pid_config_storage[index, 14] = ui_win.pid_spinBox_vel_d.value()
    pid_config_storage[index, 15] = ui_win.pid_spinBox_pos_p.value()
    pid_config_storage[index, 16] = ui_win.pid_spinBox_pos_i.value()
    pid_config_storage[index, 17] = ui_win.pid_spinBox_pos_d.value()
    pid_config_storage[index, 18] = ui_win.pid_spinBox_posrate_p.value()
    pid_config_storage[index, 19] = ui_win.pid_spinBox_posrate_i.value()
    pid_config_storage[index, 20] = ui_win.pid_spinBox_posrate_d.value()
    pid_config_storage[index, 21] = ui_win.pid_spinBox_navrate_p.value()
    pid_config_storage[index, 22] = ui_win.pid_spinBox_navrate_i.value()
    pid_config_storage[index, 23] = ui_win.pid_spinBox_navrate_d.value()
    pid_config_storage[index, 24] = ui_win.pid_spinBox_level_p.value()
    pid_config_storage[index, 25] = ui_win.pid_spinBox_level_i.value()
    pid_config_storage[index, 26] = ui_win.pid_spinBox_level_d.value()
    pid_config_storage[index, 27] = ui_win.pid_spinBox_mag_p.value()
    pid_config_storage[index, 28] = ui_win.pid_spinBox_mag_i.value()
    pid_config_storage[index, 29] = ui_win.pid_spinBox_mag_d.value()

    print ui_win.pid_lineEdit_config_storage.text()
    pid_config_storage_comments[index] = str(ui_win.pid_lineEdit_config_storage.text())
    pid_config_save(pid_config_storage_comments, pid_config_storage, pid_config_storage_comments_file, pid_config_storage_file)


def pid_config_storage_comment_load():
    index = ui_win.spinBox_pid_config_storage.value()
    ui_win.pid_spinBox_roll_p.setValue(pid_config_storage[index, 0])
    ui_win.pid_spinBox_roll_i.setValue(pid_config_storage[index, 1])
    ui_win.pid_spinBox_roll_d.setValue(pid_config_storage[index, 2])
    ui_win.pid_spinBox_pitch_p.setValue(pid_config_storage[index, 3])
    ui_win.pid_spinBox_pitch_i.setValue(pid_config_storage[index, 4])
    ui_win.pid_spinBox_pitch_d.setValue(pid_config_storage[index, 5])
    ui_win.pid_spinBox_yaw_p.setValue(pid_config_storage[index, 6])
    ui_win.pid_spinBox_yaw_i.setValue(pid_config_storage[index, 7])
    ui_win.pid_spinBox_yaw_d.setValue(pid_config_storage[index, 8])
    ui_win.pid_spinBox_alt_p.setValue(pid_config_storage[index, 9])
    ui_win.pid_spinBox_alt_i.setValue(pid_config_storage[index, 10])
    ui_win.pid_spinBox_alt_d.setValue(pid_config_storage[index, 11])
    ui_win.pid_spinBox_vel_p.setValue(pid_config_storage[index, 12])
    ui_win.pid_spinBox_vel_i.setValue(pid_config_storage[index, 13])
    ui_win.pid_spinBox_vel_d.setValue(pid_config_storage[index, 14])
    ui_win.pid_spinBox_pos_p.setValue(pid_config_storage[index, 15])
    ui_win.pid_spinBox_pos_i.setValue(pid_config_storage[index, 16])
    ui_win.pid_spinBox_pos_d.setValue(pid_config_storage[index, 17])
    ui_win.pid_spinBox_posrate_p.setValue(pid_config_storage[index, 18])
    ui_win.pid_spinBox_posrate_i.setValue(pid_config_storage[index, 19])
    ui_win.pid_spinBox_posrate_d.setValue(pid_config_storage[index, 20])
    ui_win.pid_spinBox_navrate_p.setValue(pid_config_storage[index, 21])
    ui_win.pid_spinBox_navrate_i.setValue(pid_config_storage[index, 22])
    ui_win.pid_spinBox_navrate_d.setValue(pid_config_storage[index, 23])
    ui_win.pid_spinBox_level_p.setValue(pid_config_storage[index, 24])
    ui_win.pid_spinBox_level_i.setValue(pid_config_storage[index, 25])
    ui_win.pid_spinBox_level_d.setValue(pid_config_storage[index, 26])
    ui_win.pid_spinBox_mag_p.setValue(pid_config_storage[index, 27])
    ui_win.pid_spinBox_mag_i.setValue(pid_config_storage[index, 28])
    ui_win.pid_spinBox_mag_d.setValue(pid_config_storage[index, 29])

def send_pid_values():
    if ui_win.checkBox_pid_active.isChecked():
        pid_msg = PID_cleanflight()
        pid_msg.roll.p = ui_win.pid_spinBox_roll_p.value()
        pid_msg.roll.i = ui_win.pid_spinBox_roll_i.value()
        pid_msg.roll.d = ui_win.pid_spinBox_roll_d.value()
        pid_msg.pitch.p = ui_win.pid_spinBox_pitch_p.value()
        pid_msg.pitch.i = ui_win.pid_spinBox_pitch_i.value()
        pid_msg.pitch.d = ui_win.pid_spinBox_pitch_d.value()
        pid_msg.yaw.p = ui_win.pid_spinBox_yaw_p.value()
        pid_msg.yaw.i = ui_win.pid_spinBox_yaw_i.value()
        pid_msg.yaw.d = ui_win.pid_spinBox_yaw_d.value()
        pid_msg.alt.p = ui_win.pid_spinBox_alt_p.value()
        pid_msg.alt.i = ui_win.pid_spinBox_alt_i.value()
        pid_msg.alt.d = ui_win.pid_spinBox_alt_d.value()
        pid_msg.vel.p = ui_win.pid_spinBox_vel_p.value()
        pid_msg.vel.i = ui_win.pid_spinBox_vel_i.value()
        pid_msg.vel.d = ui_win.pid_spinBox_vel_d.value()
        pid_msg.pos.p = ui_win.pid_spinBox_pos_p.value()
        pid_msg.pos.i = ui_win.pid_spinBox_pos_i.value()
        pid_msg.pos.d = ui_win.pid_spinBox_pos_d.value()
        pid_msg.posrate.p = ui_win.pid_spinBox_posrate_p.value()
        pid_msg.posrate.i = ui_win.pid_spinBox_posrate_i.value()
        pid_msg.posrate.d = ui_win.pid_spinBox_posrate_d.value()
        pid_msg.navrate.p = ui_win.pid_spinBox_navrate_p.value()
        pid_msg.navrate.i = ui_win.pid_spinBox_navrate_i.value()
        pid_msg.navrate.d = ui_win.pid_spinBox_navrate_d.value()
        pid_msg.level.p = ui_win.pid_spinBox_level_p.value()
        pid_msg.level.i = ui_win.pid_spinBox_level_i.value()
        pid_msg.level.d = ui_win.pid_spinBox_level_d.value()
        pid_msg.mag.p = ui_win.pid_spinBox_mag_p.value()
        pid_msg.mag.i = ui_win.pid_spinBox_mag_i.value()
        pid_msg.mag.d = ui_win.pid_spinBox_mag_d.value()
        ros_publisher_fc_set_pid.publish(pid_msg)
        print 'published ros_publisher_fc_set_pid'
    else:
        print 'not allowed'

##########################################################################################
# init ros callback functions
##########################################################################################
def callback_gps_home(cur_gps_input):
    gps_pos = (cur_gps_input.longitude, cur_gps_input.latitude)
    if 'home' in gps_positions.keys():
        if gps_pos != gps_positions['home']['pos']:
            gps_positions['home']['pos'] = gps_pos
            gps_altitudes['home'] = cur_gps_input.altitude
    else:
        gps_positions['home'] = {'pos': gps_pos, 'symbol': 'o', 'brush': pyqtgraph.mkBrush(color=(255, 255, 0))}
        gps_altitudes['home'] = cur_gps_input.altitude


def callback_gps_way_point(cur_gps_input):
    gps_pos = (cur_gps_input.longitude, cur_gps_input.latitude)
    if 'way_point' in gps_positions.keys():
        if gps_pos != gps_positions['way_point']['pos']:
            gps_positions['way_point']['pos'] = gps_pos
            gps_altitudes['way_point'] = cur_gps_input.altitude
    else:
        gps_positions['way_point'] = {'pos': gps_pos, 'symbol': 'o', 'brush': pyqtgraph.mkBrush(color=(0, 255, 0))}
        gps_altitudes['way_point'] = cur_gps_input.altitude


def callback_gps_position(cur_gps_input):
    global gps_geo_cycle_data, gps_data, gps_positions, altitude_dataset_index
    time_stamp = cur_gps_input.header.stamp.to_nsec() / 1e9
    if len(gps_data[0]) == 0:
        gps_geo_cycle_data = generate_geo_circle(cur_gps_input.longitude, cur_gps_input.latitude, 5)
        gps_data[0].append(cur_gps_input.longitude)
        gps_data[1].append(cur_gps_input.latitude)
    elif ((cur_gps_input.longitude == gps_data[0][-1]) and (cur_gps_input.latitude != gps_data[1][-1])):
        # new position is identical to previous one
        pass
    else:
        gps_data[0].append(cur_gps_input.longitude)
        gps_data[1].append(cur_gps_input.latitude)

    if altitude_dataset_index and 'fc_gps' in altitude_dataset_index.keys():
        index = altitude_dataset_index['fc_gps']
        if np.sum(altitude_dataset[:, index, 1]) == 0:
            altitude_dataset[:, index, 1] = time_stamp
            print 'applying: ', np.mean(altitude_dataset[:, index, 1]), time_stamp
        altitude_dataset[:-1, index, :] = altitude_dataset[1:, index, :]
        altitude_dataset[-1, index, 0] = cur_gps_input.altitude
        altitude_dataset[-1, index, 1] = time_stamp

    gps_pos = (cur_gps_input.longitude, cur_gps_input.latitude)
    if 'phoenix' in gps_positions.keys():
        if gps_pos != gps_positions['phoenix']['pos']:
            gps_positions['phoenix']['pos'] = gps_pos
            gps_altitudes['phoenix'] = cur_gps_input.altitude
    else:
        gps_positions['phoenix'] = {'pos': gps_pos, 'symbol': 'o', 'brush': pyqtgraph.mkBrush(color=(0, 0, 255))}
        gps_altitudes['phoenix'] = cur_gps_input.altitude


def callback_cur_servo_cmd(cur_servo_cmd):
    set_parameters_slider(0, cur_servo_cmd.servo0)
    set_parameters_slider(1, cur_servo_cmd.servo1)
    set_parameters_slider(2, cur_servo_cmd.servo2)
    set_parameters_slider(3, cur_servo_cmd.servo3)
    set_parameters_slider(4, cur_servo_cmd.servo4)
    set_parameters_slider(5, cur_servo_cmd.servo5)
    set_parameters_slider(6, cur_servo_cmd.servo6)
    set_parameters_slider(7, cur_servo_cmd.servo7)
    set_parameters_slider(8, cur_servo_cmd.servo8)
    set_parameters_slider(9, cur_servo_cmd.servo9)
    set_parameters_slider(10, cur_servo_cmd.servo10)
    set_parameters_slider(11, cur_servo_cmd.servo11)
    set_parameters_slider(12, cur_servo_cmd.servo12)
    set_parameters_slider(13, cur_servo_cmd.servo13)
    set_parameters_slider(14, cur_servo_cmd.servo14)
    set_parameters_slider(15, cur_servo_cmd.servo15)
    set_parameters_slider(16, cur_servo_cmd.servo16)
    set_parameters_slider(17, cur_servo_cmd.servo17)
    print ' -> updated sliders from cur_servo_cmd'


def callback_fc_rc(cur_joy_cmd):
    global fc_rc
    fc_rc[:-1, :] = fc_rc[1:, :]
    fc_rc[-1, 0] = cur_joy_cmd.axes[1]          # pitch
    fc_rc[-1, 1] = cur_joy_cmd.axes[0]          # roll
    fc_rc[-1, 2] = cur_joy_cmd.axes[2]          # yaw
    fc_rc[-1, 3] = cur_joy_cmd.axes[3]          # Throttle
    fc_rc[-1, 4] = cur_joy_cmd.buttons[0]       # gps
    fc_rc[-1, 5] = cur_joy_cmd.buttons[1]       #
    fc_rc[-1, 6] = cur_joy_cmd.buttons[2]       #
    fc_rc[-1, 7] = cur_joy_cmd.buttons[3]       # barometer


def callback_fc_altitude(cur_altitude):
    time_stamp = cur_altitude.header.stamp.to_nsec() / 1e9
    index = altitude_dataset_index['fc_barometer']
    if np.sum(altitude_dataset[:, index, 1]) == 0:
        altitude_dataset[:, index, 1] = time_stamp
        print 'applying: ', np.mean(altitude_dataset[:, index, 1]), time_stamp
    altitude_dataset[:-1, index, :] = altitude_dataset[1:, index, :]
    altitude_dataset[-1, index, 0] = cur_altitude.estimated_altitude
    altitude_dataset[-1, index, 1] = time_stamp


def callback_marvic_altitude_fused(cur_altitude):
    time_stamp = cur_altitude.header.stamp.to_nsec() / 1e9
    index = altitude_dataset_index['marvic_fused']
    if np.sum(altitude_dataset[:, index, 1]) == 0:
        altitude_dataset[:, index, 1] = time_stamp
        print 'applying: ', np.mean(altitude_dataset[:, index, 1]), time_stamp
    altitude_dataset[:-1, index, :] = altitude_dataset[1:, index, :]
    altitude_dataset[-1, index, 0] = cur_altitude.estimated_altitude
    altitude_dataset[-1, index, 1] = time_stamp


def callback_marvic_altitude_lidar(cur_altitude):
    time_stamp = cur_altitude.header.stamp.to_nsec() / 1e9
    index = altitude_dataset_index['marvic_lidar']
    if np.sum(altitude_dataset[:, index, 1]) == 0:
        altitude_dataset[:, index, 1] = time_stamp
        print 'applying: ', np.mean(altitude_dataset[:, index, 1]), time_stamp
    altitude_dataset[:-1, index, :] = altitude_dataset[1:, index, :]
    altitude_dataset[-1, index, 0] = cur_altitude.estimated_altitude
    altitude_dataset[-1, index, 1] = time_stamp


def callback_marvic_altitude_infra_red(cur_altitude):
    time_stamp = cur_altitude.header.stamp.to_nsec() / 1e9
    index = altitude_dataset_index['marvic_ir']
    if np.sum(altitude_dataset[:, index, 1]) == 0:
        altitude_dataset[:, index, 1] = time_stamp
        print 'applying: ', np.mean(altitude_dataset[:, index, 1]), time_stamp
    altitude_dataset[:-1, index, :] = altitude_dataset[1:, index, :]
    altitude_dataset[-1, index, 0] = cur_altitude.estimated_altitude
    altitude_dataset[-1, index, 1] = time_stamp


def callback_image_mono(cur_image_mono):
    global live_image, time_of_last_image, video_fps
    live_image = np.reshape(np.fromstring(cur_image_mono.data, np.uint8), (cur_image_mono.height, cur_image_mono.step))
    video_fps = 1. / (time.time() - time_of_last_image)
    time_of_last_image = time.time()


def callback_fc_pid_cleanflight(cur_pid_settings):
    if ui_win.checkBox_pid_update.isChecked():
        ui_win.checkBox_pid_update.setChecked(False)
        ui_win.pid_spinBox_roll_p.setValue(cur_pid_settings.roll.p)
        ui_win.pid_spinBox_roll_i.setValue(cur_pid_settings.roll.i)
        ui_win.pid_spinBox_roll_d.setValue(cur_pid_settings.roll.d)
        ui_win.pid_spinBox_pitch_p.setValue(cur_pid_settings.pitch.p)
        ui_win.pid_spinBox_pitch_i.setValue(cur_pid_settings.pitch.i)
        ui_win.pid_spinBox_pitch_d.setValue(cur_pid_settings.pitch.d)
        ui_win.pid_spinBox_yaw_p.setValue(cur_pid_settings.yaw.p)
        ui_win.pid_spinBox_yaw_i.setValue(cur_pid_settings.yaw.i)
        ui_win.pid_spinBox_yaw_d.setValue(cur_pid_settings.yaw.d)
        ui_win.pid_spinBox_alt_p.setValue(cur_pid_settings.alt.p)
        ui_win.pid_spinBox_alt_i.setValue(cur_pid_settings.alt.i)
        ui_win.pid_spinBox_alt_d.setValue(cur_pid_settings.alt.d)
        ui_win.pid_spinBox_alt_p.setValue(cur_pid_settings.alt.p)
        ui_win.pid_spinBox_alt_i.setValue(cur_pid_settings.alt.i)
        ui_win.pid_spinBox_alt_d.setValue(cur_pid_settings.alt.d)
        ui_win.pid_spinBox_pos_p.setValue(cur_pid_settings.pos.p)
        ui_win.pid_spinBox_pos_i.setValue(cur_pid_settings.pos.i)
        ui_win.pid_spinBox_pos_d.setValue(cur_pid_settings.pos.d)
        ui_win.pid_spinBox_posrate_p.setValue(cur_pid_settings.posrate.p)
        ui_win.pid_spinBox_posrate_i.setValue(cur_pid_settings.posrate.i)
        ui_win.pid_spinBox_posrate_d.setValue(cur_pid_settings.posrate.d)
        ui_win.pid_spinBox_navrate_p.setValue(cur_pid_settings.navrate.p)
        ui_win.pid_spinBox_navrate_i.setValue(cur_pid_settings.navrate.i)
        ui_win.pid_spinBox_navrate_d.setValue(cur_pid_settings.navrate.d)
        ui_win.pid_spinBox_level_p.setValue(cur_pid_settings.level.p)
        ui_win.pid_spinBox_level_i.setValue(cur_pid_settings.level.i)
        ui_win.pid_spinBox_level_d.setValue(cur_pid_settings.level.d)
        ui_win.pid_spinBox_mag_p.setValue(cur_pid_settings.mag.p)
        ui_win.pid_spinBox_mag_i.setValue(cur_pid_settings.mag.i)
        ui_win.pid_spinBox_mag_d.setValue(cur_pid_settings.mag.d)
        print 'updated all pid values in the gui from the latest incoming message'
    else:
        print 'update not requested'

##########################################################################################
# init ros
##########################################################################################
rospy.init_node('gauge_gui')
ros_subscribe_cur_servo_cmd = rospy.Subscriber('/crab/uart_bridge/cur_servo_cmd', Servo, callback_cur_servo_cmd)
ros_subscribe_gps_position = rospy.Subscriber('/phx/gps', NavSatFix, callback_gps_position)
ros_subscribe_gps_way_point = rospy.Subscriber('/phx/fc/gps_way_point', NavSatFix, callback_gps_way_point)
ros_subscribe_gps_home = rospy.Subscriber('/phx/fc/gps_home', NavSatFix, callback_gps_home)
ros_subscribe_fc_rc = rospy.Subscriber('/phx/fc/rc', Joy, callback_fc_rc)
ros_subscribe_fc_altitude = rospy.Subscriber('/phx/fc/altitude', Altitude, callback_fc_altitude)
ros_subscribe_fc_pid_in_use = rospy.Subscriber('/phx/fc/pid_in_use', PID_cleanflight, callback_fc_pid_cleanflight)
ros_subscribe_marvic_altitude = rospy.Subscriber('/phx/marvicAltitude/altitude', Altitude, callback_marvic_altitude_fused)
ros_subscribe_marvic_lidar = rospy.Subscriber('/phx/marvicAltitude/lidar', Altitude, callback_marvic_altitude_lidar)
ros_subscribe_marvic_infra_red = rospy.Subscriber('/phx/marvicAltitude/infra_red', Altitude, callback_marvic_altitude_infra_red)
#ros_subscribe_fc_rc = rospy.Subscriber('/phx/marvicRC/rc_input', Joy, callback_fc_rc)
ros_subscribe_image_mono = rospy.Subscriber('/image_mono', Image, callback_image_mono)
update_interval = 10    # ms
publish_servo = False
publish_led = True
ros_publisher_servo_cmd = rospy.Publisher('/crab/uart_bridge/servo_cmd', Servo, queue_size=1)
ros_publisher_gps_way_point = rospy.Publisher('/phx/gps_way_point', NavSatFix, queue_size=1)
ros_publisher_fc_set_pid = rospy.Publisher('/phx/fc/pid_set', PID_cleanflight, queue_size=1)
publisher_led_strip_last_update = 0
ros_publisher_led_strip_0_cmd = rospy.Publisher('phx/led/led_strip_0', LEDstrip, queue_size=1)
ros_publisher_led_strip_1_cmd = rospy.Publisher('phx/led/led_strip_1', LEDstrip, queue_size=1)
ros_publisher_led_strip_2_cmd = rospy.Publisher('phx/led/led_strip_2', LEDstrip, queue_size=1)
ros_publisher_led_strip_3_cmd = rospy.Publisher('phx/led/led_strip_3', LEDstrip, queue_size=1)


def mainloop():
    #parameters = [get_parameters_slider(i) for i in range(0, 18)]
    #for i in range(0, 18):
    #    set_parameters_lcd(i, parameters[i])
    global publish_servo, publisher_led_strip_last_update, update_background_map, gps_background_image
    if publish_servo:
        publish_servos()

    if publish_led and ui_win.checkBox_led_strip_update_continuous.isChecked():
        if time.time() > publisher_led_strip_last_update + 0.1:
            # update led strips from sliders
            print 'updating LEDs'
            publish_led_strips()
            publisher_led_strip_last_update = time.time()

    print 'mainloop', win.keysPressed

    try:
        update_video_mask()
        update_video()
        update_fc_remote_control()
        update_gps_plot(path=True, points=True)
        update_altitude_plot()
    except:
        print '>>> error in main loop'

    if not update_background_map and gps_positions.has_key('phoenix'):
        print gps_positions['phoenix']['pos'][1], gps_positions['phoenix']['pos'][0]
        gps_update_map(gps_positions['phoenix']['pos'][1], gps_positions['phoenix']['pos'][0], gps_background_image)
        update_background_map = True

#######################################################################################################################
# gui button callbacks
#######################################################################################################################
def publish_led_strips():
    print 'publishing LED strip'
    ros_publisher_led_strip_0_cmd.publish(generate_led_strip_msg(ui_win.horizontalSlider_led_0_r, ui_win.horizontalSlider_led_0_g, ui_win.horizontalSlider_led_0_b))
    ros_publisher_led_strip_1_cmd.publish(generate_led_strip_msg(ui_win.horizontalSlider_led_1_r, ui_win.horizontalSlider_led_1_g, ui_win.horizontalSlider_led_1_b))
    ros_publisher_led_strip_2_cmd.publish(generate_led_strip_msg(ui_win.horizontalSlider_led_2_r, ui_win.horizontalSlider_led_2_g, ui_win.horizontalSlider_led_2_b))
    ros_publisher_led_strip_3_cmd.publish(generate_led_strip_msg(ui_win.horizontalSlider_led_3_r, ui_win.horizontalSlider_led_3_g, ui_win.horizontalSlider_led_3_b))


def publish_servos():
    send_servos_msg = Servo()
    send_servos_msg.servo0 = get_parameters_slider(0)
    send_servos_msg.servo1 = get_parameters_slider(1)
    send_servos_msg.servo2 = get_parameters_slider(2)
    send_servos_msg.servo3 = get_parameters_slider(3)
    send_servos_msg.servo4 = get_parameters_slider(4)
    send_servos_msg.servo5 = get_parameters_slider(5)
    send_servos_msg.servo6 = get_parameters_slider(6)
    send_servos_msg.servo7 = get_parameters_slider(7)
    send_servos_msg.servo8 = get_parameters_slider(8)
    send_servos_msg.servo9 = get_parameters_slider(9)
    send_servos_msg.servo10 = get_parameters_slider(10)
    send_servos_msg.servo11 = get_parameters_slider(11)
    send_servos_msg.servo12 = get_parameters_slider(12)
    send_servos_msg.servo13 = get_parameters_slider(13)
    send_servos_msg.servo14 = get_parameters_slider(14)
    send_servos_msg.servo15 = get_parameters_slider(15)
    send_servos_msg.servo16 = get_parameters_slider(16)
    send_servos_msg.servo17 = get_parameters_slider(17)
    ros_publisher_servo_cmd.publish(send_servos_msg)


def ros_subscription_update():
    global ros_subscribe_image_mono
    if ui_win.checkBox_video_active.isChecked() and ros_subscribe_image_mono.callback == None:
        ros_subscribe_image_mono = rospy.Subscriber('/image_mono', Image, callback_image_mono)
    if not ui_win.checkBox_video_active.isChecked() and ros_subscribe_image_mono.callback != None:
        ros_subscribe_image_mono.unregister()

QtCore.QObject.connect(ui_win.pushButton_led_strip_update, QtCore.SIGNAL('clicked()'), publish_led_strips)
QtCore.QObject.connect(ui_win.checkBox_video_active, QtCore.SIGNAL('stateChanged(int)'), ros_subscription_update)
QtCore.QObject.connect(ui_win.pushButton_pid_set, QtCore.SIGNAL('clicked()'), send_pid_values)
QtCore.QObject.connect(ui_win.spinBox_pid_config_storage, QtCore.SIGNAL('valueChanged(int)'), pid_config_storage_comment_update)
QtCore.QObject.connect(ui_win.pushButton_pid_config_storage_save, QtCore.SIGNAL('clicked()'), pid_config_storage_comment_save)
QtCore.QObject.connect(ui_win.pushButton_pid_config_storage_load, QtCore.SIGNAL('clicked()'), pid_config_storage_comment_load)


ros_subscription_update()


win.show()
# QTimer
timer = QtCore.QTimer()
timer.timeout.connect(mainloop)
interval_ms = update_interval
timer.start(interval_ms)

app.exec_()

print 'end'
timer.stop()

ros_subscribe_cur_servo_cmd.unregister()
ros_subscribe_gps_position.unregister()
ros_subscribe_gps_way_point.unregister()
ros_subscribe_gps_home.unregister()
ros_subscribe_fc_rc.unregister()
ros_subscribe_image_mono.unregister()
ros_subscribe_marvic_infra_red.unregister()
ros_subscribe_marvic_lidar.unregister()
ros_subscribe_marvic_altitude.unregister()
